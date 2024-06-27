# Breast Models STL Conversion

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
### Create and activate a Conda environment:
If you don't have Conda installed, you can install Miniconda or Anaconda as they come with Conda included.

Create and activate the environment using the provided `environment.yml` file:
```
conda env create -f environment.yml
conda activate mha_to_stl_env
```

## Usage
To run this script, navigate to the directory containing the script after setting up your environment. You can simply run `convert.py` using Python and pass the required and optional parameters as arguments. Here is how you can structure the usage instructions including the flags:

```
# Basic usage with mandatory arguments
python convert.py --input_dir INPUT_DIR --output_dir OUTPUT_DIR

# Full usage with all optional arguments specifying start and end exams with crawling
python convert.py --input_dir INPUT_DIR --output_dir OUTPUT_DIR --base_url BASE_URL --start_exam START_EXAM --end_exam END_EXAM --smooth --relaxation_factor 0.25 --lump_tissues

# Full usage with all optional arguments specifying start and end exams without crawling (files exist locally in input folder)
python convert.py --input_dir INPUT_DIR --output_dir OUTPUT_DIR --start_exam START_EXAM --end_exam END_EXAM --smooth --relaxation_factor 0.25 --lump_tissues --no_download

# Full usage with all optional arguments specifying specific exams to crawl convert
python convert.py --input_dir INPUT_DIR --output_dir OUTPUT_DIR --base_url BASE_URL --smooth --relaxation_factor 0.25 --lump_tissues --exam_names "Exam_01,Exam_02"

# Full usage with all optional arguments specifying specific exams to convert
python convert.py --input_dir INPUT_DIR --output_dir OUTPUT_DIR --smooth --relaxation_factor 0.25 --lump_tissues --exam_names "Exam_01,Exam_02" --no_download
```

### Flags and Options
Each option and flag has a specific purpose, as outlined below:

- `--input_dir`: Directory to store downloaded MHA files. This is a mandatory argument.
- `--output_dir`: Directory to store converted STL files. This is a mandatory argument.
- `--base_url` (Optional): URL of the GitHub repository where the MHA files are hosted. Default value is https://github.com/acpelicano/breast_models_repository.
- `--start_exam` (Optional): Specifies the starting exam number to download and process. Default value is 1.
- `--end_exam` (Optional): Specifies the ending exam number to download and process. Default value is 55.
- `--smooth` (Optional): Enables smoothing of the STL files during conversion. This is a boolean flag. Default value is True.
- `--relaxation_factor` (Optional): Sets the relaxation factor for smoothing. Higher values increase smoothing. Default value is 0.25.
- `--lump_tissues` (Optional): When set, groups similar tissue types together during conversion. Default value is True.
- `--no_download` (Optional): When set, MHA files are not downloaded from the GitHub repository and only MHA files in the input directory are converted. Every segmented scan should be in its own subdirectory. Default value is False.
- `--exam_names` (Optional): When set, the script only processes the exams with specified exam names. It is a string containing a comma-separated list of file names, e.g. "Exam_01,Exam_02,Exam_03". By default, this option is not used.
