# Breast Models MHA to STL Conversion

## Overview
This script automates the extraction and conversion of segmented breast models from MHA (Meta Header) format to STL (Stereolithography) files. It crawls the [Breast Models GitHub Repository](https://github.com/acpelicano/breast_models_repository) containing segmented volumes of breast models, downloads these files, and converts each segmented volume into a separate STL file.

### References
Pelicano, Ana C., et al. "Repository of MRI-derived models of the breast with single and multiple benign and malignant tumors for microwave imaging research." Plos one 19.5 (2024): e0302974.
doi: [https://doi.org/10.1371/journal.pone.0302974](https://doi.org/10.1371/journal.pone.0302974)

## Installation
### Clone the Repository
```
git clone https://github.com/your_username/breast_models_repo_mha_to_stl.git
cd breast_models_repo_mha_to_stl
```
### Create and Activate a Conda Environment:
If you don't have Conda installed, you can install Miniconda or Anaconda as they come with Conda included.

Create and activate the environment using the provided `environment.yml` file:
```
conda env create -f environment.yml
conda activate mha_to_stl_env
```

## Usage
To run this script, navigate to the directory containing the script after setting up your environment. You can simply run `convert.py` using Python and pass the required and optional parameters as arguments. Here is how you can structure the usage instructions including the flags:

```
# Example 1: Basic usage  with mandatory arguments (crawls and converts all exams from the repository, grouping similar tissues and applying smoothing)
python convert.py --input_dir ./mha --output_dir ./stl

# Example 2: Crawl and convert Exams 1 - 20, deactivate smoothing and grouping of similar tissues
python convert.py --input_dir ./mha --output_dir ./stl --start_exam 1 --end_exam 20 --dont_lump_tissues --dont_smooth

# Example 3: Convert locally stored Exams 1 - 5, apply smoothing with a relaxation factor of 0.15
python convert.py --input_dir ./mha --output_dir ./stl --start_exam 1 --end_exam 5 --relaxation_factor 0.15 --no_download

# Example 4: Convert locally stored exams with name Exam_01, Exam_13, and Exam_17, don't group similar tissues and apply smoothing with a relaxation factor of 0.5
python convert.py --input_dir ./mha --output_dir ./stl --exam_names="Exam_01,Exam_13,Exam_17" --relaxation_factor 0.5 --no_download

# Example 5: Crawl and convert Exams 1 and 2 and performs uniform remeshing
python convert.py --input_dir ./mha --output_dir ./stl_ --exam_names "Exam_01,Exam_02" --remesh
```

### Flags and Options
Each option and flag has a specific purpose, as outlined below:

- `--input_dir`: Directory to store downloaded MHA files. This is a mandatory argument.
- `--output_dir`: Directory to store converted STL files. This is a mandatory argument.
- `--base_url` (Optional): URL of the GitHub repository where the MHA files are hosted. Default value is https://github.com/acpelicano/breast_models_repository.
- `--start_exam` (Optional): Specifies the starting exam number to download and process. Default value is 1.
- `--end_exam` (Optional): Specifies the ending exam number to download and process. Default value is 55.
- `--dont_smooth` (Optional): Disables smoothing of the STL files during conversion. Default value is True.
- `--relaxation_factor` (Optional): Sets the relaxation factor for smoothing. Higher values increase smoothing. Default value is 0.25.
- `--dont_lump_tissues` (Optional): When set, similar tissue types are not grouped during conversion. Default value is True.
- `--no_download` (Optional): When set, MHA files are not downloaded from the GitHub repository and only MHA files in the input directory are converted. Every segmented scan should be in its own subdirectory. Default value is False.
- `--exam_names` (Optional): When set, the script only processes the exams with specified exam names. It is a string containing a comma-separated list of file names, e.g. "Exam_01,Exam_02,Exam_03". By default, this option is not used.
- `--remesh` (Optional): Performs mesh simplification and uniform remeshing. By default, this option is not used.
- `--target_reduction` (Optional): Target reduction factor for mesh simplification step in remeshing process. Default value is 0.95.

## Example Exports
### Example 1
This is an example export visualized in ParaView for Exam_02 converted with the command below. 

```
python convert.py --input_dir ./mha --output_dir ./stl --exam_names="Exam_02"
```

Surfaces were smoothed with a relaxation factor of 0.25, and different fat tissues (fat_high, fat_median, fat_low) and fibroglandular tissues (fibroglandular_low, fibroglandular_median, fibroglandular_high) were lumped.

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/skin+malignant_tumor_2.png?raw=true" width="800"/><br/>
  <b>Figure 1.</b> Skin (gray) and malignant tumor (red).<br/><br/>
</p>

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/skin+malignant_tumor+fibroglandular.png?raw=true" width="800"/><br/>
  <b>Figure 2.</b> Skin (gray), malignant tumor (red), and fibroglandular tissue (green).<br/><br/>
</p>

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/skin+malignant_tumor+fibroglandular+fat.png?raw=true" width="800"/><br/>
  <b>Figure 3.</b> Skin (gray), malignant tumor (red), fibroglandular tissue (green), and fat (purple).<br/><br/>
</p>

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/skin+malignant_tumor+fibroglandular+fat+muscle.png?raw=true" width="800"/><br/>
  <b>Figure 4.</b> Skin (gray), malignant tumor (red), fibroglandular tissue (green), fat (purple), and muscle (dark gray -- not visible from that angle).
</p>

### Example 2
This is an example export visualized in ParaView for Exam_02 converted with the command below. Surfaces were smoothed with a relaxation factor of 0.25, and different fat tissues (fat_high, fat_median, fat_low) and fibroglandular tissues (fibroglandular_low, fibroglandular_median, fibroglandular_high) were lumped. Additionally, the mesh was simplified with a target reduction factor of 0.99 and uniformly remeshed.


```
python convert.py --input_dir ./mha --output_dir ./stl_ --exam_names "Exam_02" --remesh --target_reduction=0.99
```

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/remeshed_skin+malignant_tumor_2.png?raw=true" width="800"/><br/>
  <b>Figure 1.</b> Remesehd model. Skin (gray) and malignant tumor (red).<br/><br/>
</p>

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/remeshed_skin+malignant_tumor+fibroglandular.png?raw=true" width="800"/><br/>
  <b>Figure 2.</b> Remesehd model. Skin (gray), malignant tumor (red), and fibroglandular tissue (green).<br/><br/>
</p>

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/remeshed_skin+malignant_tumor+fibroglandulat+fat.png?raw=true" width="800"/><br/>
  <b>Figure 3.</b> Remesehd model. Skin (gray), malignant tumor (red), fibroglandular tissue (green), and fat (purple).<br/><br/>
</p>

<p style="text-align: center;">
  <img src="https://github.com/CellularSyntax/breast_models_repo_mha_to_stl/blob/main/example/remeshed_skin+malginant_tumor+fibroglandular+fat+muscle.png?raw=true" width="800"/><br/>
  <b>Figure 4.</b> Remesehd model. Skin (gray), malignant tumor (red), fibroglandular tissue (green), fat (purple), and muscle (orange).
</p>


