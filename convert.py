import argparse
from helper_fns import download_and_unzip, batch_process_mha_files, print_ascii_art

def main(input_dir, output_dir, base_url, start_exam, end_exam, dont_smooth, relaxation_factor, dont_lump_tissues, no_download, exam_names):
    # Label dictionary for 'detailed label map' according to repo documentation
    LABELS = {
        -4: 'benign_tumour',
        -3: 'malignant_tumour',
        -2: 'skin',
        -1: 'muscle',
        0: 'background',
        1: 'fibroglandular_low',
        2: 'fibroglandular_median',
        3: 'fibroglandular_high',
        4: 'transition',
        5: 'fat_low',
        6: 'fat_median',
        7: 'fat_high'
    }

    if exam_names:
        specific_exams = [name.strip() for name in exam_names.split(',')]

    # Download data if not skipping download
    if not no_download:
        if exam_names and specific_exams:
            # Download only specific exams
            download_and_unzip(base_url, specific_exams=specific_exams, target_directory=input_dir)
        else:
            # Download a range of exams
            download_and_unzip(base_url, start_exam=start_exam, end_exam=end_exam, target_directory=input_dir)


    lump_tissues = not dont_lump_tissues
    smooth = not dont_smooth

    # Convert MHA files to STL files, adjusting for specific exams if provided
    if exam_names:
        batch_process_mha_files(input_dir, output_dir, LABELS, smooth=smooth, relaxation_factor=relaxation_factor, lump_tissues=lump_tissues, specific_exams=specific_exams)
    else:
        batch_process_mha_files(input_dir, output_dir, LABELS, smooth=smooth, relaxation_factor=relaxation_factor, lump_tissues=lump_tissues, start_exam=start_exam, end_exam=end_exam)

if __name__ == '__main__':
    print_ascii_art()
    parser = argparse.ArgumentParser(description='Script to crawl segmented breast models from GitHub and convert them to STL files.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory to store downloaded or existing MHA files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to store converted STL files')
    parser.add_argument('--base_url', type=str, default='https://github.com/acpelicano/breast_models_repository/raw/main/', help='Base URL for GitHub repository files')
    parser.add_argument('--start_exam', type=int, default=1, help='Starting exam number')
    parser.add_argument('--end_exam', type=int, default=55, help='Ending exam number')
    parser.add_argument('--dont_smooth', action='store_true', help='Disable smoothing of STL files')
    parser.add_argument('--relaxation_factor', type=float, default=0.25, help='Relaxation factor for smoothing')
    parser.add_argument('--dont_lump_tissues', action='store_true', help='Do not group similar tissue types during conversion')
    parser.add_argument('--no_download', action='store_true', help='Skip downloading MHA files and use existing files in the input directory')
    parser.add_argument('--exam_names', type=str, help='Comma-separated list of specific exam names to process (e.g., Exam_01,Exam_02)')

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.base_url, args.start_exam, args.end_exam, args.dont_smooth, args.relaxation_factor, args.dont_lump_tissues, args.no_download, args.exam_names)
