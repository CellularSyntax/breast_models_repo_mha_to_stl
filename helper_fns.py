import os
import requests
import zipfile
import numpy as np
import SimpleITK as sitk
import vtk
from vtk.util.numpy_support import numpy_to_vtk
from tqdm import tqdm

def download_and_unzip(base_url, target_directory, start_exam=1, end_exam=55, specific_exams=None):
    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Generate list of exam names to process
    if specific_exams:
        exams_to_process = specific_exams
    else:
        exams_to_process = [f"Exam_{i:02}" for i in range(start_exam, end_exam + 1)]

    # Loop through each exam name
    with tqdm(total=len(exams_to_process), desc="Processing Exams", unit="Exam", position=1) as pbar:
        for exam_name in exams_to_process:
            tqdm.write(f"Downloading {exam_name}...")
            # URL point to the raw content on GitHub for downloading
            url = f"{base_url}/{exam_name}/Label_map_detailed.zip"
            response = requests.get(url, stream=True)

            # Check if the download was successful
            if response.status_code == 200:
                zip_path = os.path.join(target_directory, f"{exam_name}.zip")
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192

                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        f.write(chunk)

                if total_size != 0:
                    tqdm.write("ERROR, something went wrong")

                tqdm.write(f"Downloaded {zip_path}")

                # Unzip the file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    extract_path = os.path.join(target_directory, exam_name)
                    zip_ref.extractall(extract_path)
                    tqdm.write(f"Extracted to {extract_path}")

                # Remove the zip file after extraction
                os.remove(zip_path)
                tqdm.write(f"Deleted {zip_path}")
            else:
                tqdm.write(f"Failed to download {url}. Status code: {response.status_code}")
        
            pbar.update(1)

# Convert .mha files to .stl files using VTK
def mha_to_stl_vtk_no_lump(input_filename, output_dir, label_dict, smooth=False, relaxation_factor=0.1):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the .mha file
    image = sitk.ReadImage(input_filename)
    array = sitk.GetArrayFromImage(image)

    # Unique labels in the image
    labels = np.unique(array)
    tqdm.write("Found labels:", labels)

    # Process each label
    for label in labels:
        if label in label_dict and label_dict[label] != 'background':  # Skip the background
            tqdm.write(f"Processing label: {label} ({label_dict[label]})")

            # Extract the region using the label
            label_map = (array == label).astype(np.uint8)

            # Convert numpy array to VTK array
            vtk_data = numpy_to_vtk(num_array=label_map.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)

            # Create VTK image data
            vtk_image = vtk.vtkImageData()
            vtk_image.SetSpacing(image.GetSpacing())
            vtk_image.SetOrigin(image.GetOrigin())
            vtk_image.SetDimensions(image.GetSize())
            vtk_image.GetPointData().SetScalars(vtk_data)

            # Extract the surface using marching cubes
            contour = vtk.vtkMarchingCubes()
            contour.SetInputData(vtk_image)
            contour.SetValue(0, 0.5)  # Surface threshold
            contour.Update()

            # Create STL writer
            stl_writer = vtk.vtkSTLWriter()

            # Optionally, smooth the mesh (experimental)
            if smooth:
                smoothFilter = vtk.vtkSmoothPolyDataFilter()
                smoothFilter.SetInputData(contour.GetOutput())
                smoothFilter.SetNumberOfIterations(15)
                smoothFilter.SetRelaxationFactor(relaxation_factor)
                smoothFilter.FeatureEdgeSmoothingOff()
                smoothFilter.BoundarySmoothingOn()
                smoothFilter.Update()
                stl_writer.SetInputData(smoothFilter.GetOutput())
            else:
                stl_writer.SetInputData(contour.GetOutput())
                
            stl_writer.SetFileTypeToBinary()

            # Define file name based on label dictionary
            stl_filename = os.path.join(output_dir, f"{label_dict[label]}.stl")
            stl_writer.SetFileName(stl_filename)
            stl_writer.Write()
            tqdm.write(f"Saved: {stl_filename}")

# Convert .mha files to .stl files using VTK
def mha_to_stl_vtk_lump(input_filename, output_dir, label_dict, smooth=False, relaxation_factor=0.1, lump_tissues=True):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the .mha file
    image = sitk.ReadImage(input_filename)
    array = sitk.GetArrayFromImage(image)

    # Define label groups if lumping is enabled
    grouped_labels = {}
    if lump_tissues:
        grouped_labels = {
            'fat': [5, 6, 7],  # label ids for fat_low, fat_median, fat_high
            'fibroglandular': [1, 2, 3],  # label ids for fibroglandular_low, fibroglandular_median, fibroglandular_high
        }

    # Process groupwise if lumping is enabled
    if lump_tissues:
        for group_name, label_ids in grouped_labels.items():
            group_mask = np.isin(array, label_ids).astype(np.uint8)

            # Skip if no data for the group
            if np.sum(group_mask) == 0:
                tqdm.write(f"No data found for group: {group_name}")
                continue

            tqdm.write(f"Processing group: {group_name}")
            process_label_group(group_mask, group_name, image, output_dir, smooth, relaxation_factor)

    # Process individual labels
    for label, name in label_dict.items():
        if label == 0 and name == 'background':
            continue

        # If lumping is enabled and the label is in one of the groups, skip...
        if lump_tissues and any(label in group for group in grouped_labels.values()):
            continue

        label_mask = (array == label).astype(np.uint8)
        if np.sum(label_mask) == 0:
            tqdm.write(f"No data found for label: {name}")
            continue

        tqdm.write(f"Processing label: {name} (Label ID: {label})")
        process_label_group(label_mask, name, image, output_dir, smooth, relaxation_factor)

def process_label_group(mask, name, image, output_dir, smooth, relaxation_factor):
    # Convert numpy array to VTK array
    vtk_data = numpy_to_vtk(num_array=mask.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)

    # Create VTK image data
    vtk_image = vtk.vtkImageData()
    vtk_image.SetSpacing(image.GetSpacing())
    vtk_image.SetOrigin(image.GetOrigin())
    vtk_image.SetDimensions(image.GetSize())
    vtk_image.GetPointData().SetScalars(vtk_data)

    # Extract the surface using marching cubes
    contour = vtk.vtkMarchingCubes()
    contour.SetInputData(vtk_image)
    contour.SetValue(0, 0.5)  # Surface threshold
    contour.Update()

    # Optionally, smooth the mesh
    if smooth:
        smoothFilter = vtk.vtkSmoothPolyDataFilter()
        smoothFilter.SetInputData(contour.GetOutput())
        smoothFilter.SetNumberOfIterations(15)
        smoothFilter.SetRelaxationFactor(relaxation_factor)
        smoothFilter.FeatureEdgeSmoothingOff()
        smoothFilter.BoundarySmoothingOn()
        smoothFilter.Update()
        final_data = smoothFilter.GetOutput()
    else:
        final_data = contour.GetOutput()

    # Create STL writer
    stl_writer = vtk.vtkSTLWriter()
    stl_writer.SetInputData(final_data)
    stl_writer.SetFileTypeToBinary()

    # Write file
    stl_filename = os.path.join(output_dir, f"{name}.stl")
    stl_writer.SetFileName(stl_filename)
    stl_writer.Write()
    tqdm.write(f"Saved: {stl_filename}")

def batch_process_mha_files(input_dir, output_dir, label_dict, smooth=True, relaxation_factor=0.1, lump_tissues=True, start_exam=1, end_exam=55, specific_exams=None):
    # Collect directories to process
    directories_to_process = []
    for subdir, dirs, files in os.walk(input_dir):
        exam_name = os.path.basename(subdir)
        if exam_name.startswith("Exam_"):
            if specific_exams and exam_name in specific_exams:
                directories_to_process.append((subdir, exam_name))
            elif not specific_exams:
                try:
                    exam_number = int(exam_name.split('_')[1])
                    if start_exam <= exam_number <= end_exam:
                        directories_to_process.append((subdir, exam_name))
                except ValueError:
                    continue  # Ignore folders that do not match the expected format

    # Process directories with a progress bar
    with tqdm(total=len(directories_to_process), desc="Processing Directories", unit="dir", position=1) as pbar:
        for subdir, exam_name in directories_to_process:
            for file in os.listdir(subdir):
                if file.endswith('.mha'):
                    input_filename = os.path.join(subdir, file)
                    output_directory = os.path.join(output_dir, exam_name)
                    # Decide which processing function to use based on lump_tissues flag
                    if lump_tissues:
                        mha_to_stl_vtk_lump(input_filename, output_directory, label_dict, smooth, relaxation_factor, lump_tissues)
                    else:
                        mha_to_stl_vtk_no_lump(input_filename, output_directory, label_dict, smooth, relaxation_factor)
            pbar.update(1)
    
    tqdm.write("Processing complete.")

# Print ASCII art
def print_ascii_art():
    ascii_art = r"""
 _____ ______   ___  ___  ________             _________  ________             ________  _________  ___          
|\   _ \  _   \|\  \|\  \|\   __  \           |\___   ___\\   __  \           |\   ____\|\___   ___\\  \         
\ \  \\\__\ \  \ \  \\\  \ \  \|\  \          \|___ \  \_\ \  \|\  \          \ \  \___|\|___ \  \_\ \  \        
 \ \  \\|__| \  \ \   __  \ \   __  \              \ \  \ \ \  \\\  \          \ \_____  \   \ \  \ \ \  \       
  \ \  \    \ \  \ \  \ \  \ \  \ \  \              \ \  \ \ \  \\\  \          \|____|\  \   \ \  \ \ \  \____  
   \ \__\    \ \__\ \__\ \__\ \__\ \__\              \ \__\ \ \_______\           ____\_\  \   \ \__\ \ \_______\
    \|__|     \|__|\|__|\|__|\|__|\|__|               \|__|  \|_______|          |\_________\   \|__|  \|_______|
                                                                                 \|_________|                    
    """
    print(ascii_art)
