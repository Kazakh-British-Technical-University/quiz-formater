# Quiz Converter

A Python tool for converting quiz questions from CSV format to LaTeX and PDF exam variants.

## Features

- Converts quiz questions from CSV to LaTeX format
- Generates multiple exam variants with randomized questions
- Supports PDF generation from LaTeX files
- Configurable number of variants and questions per variant
- Customizable output formats (CSV, LaTeX, PDF)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/QuizConverter.git
cd QuizConverter
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with default settings:

```bash
python main.py
```

This will:

- Read questions from `data/input/test.csv`
- Generate 3 exam variants
- Create up to 10 questions per variant
- Generate both LaTeX and PDF files

### Command Line Options

You can customize the behavior using command line options:

```bash
python main.py --input-path "path/to/your/input.csv" --num-variants 5 --max-questions 15 --should-generate-pdf
```

Available options:

- `--input-path`: Path to the input CSV file
- `--num-variants`: Number of exam variants to generate
- `--max-questions`: Maximum number of questions per variant
- `--should-generate-pdf`: Whether to generate PDF files (True/False)

### Configuration File

You can also modify the default settings in `config.ini`:

```ini
[DEFAULT]
input_path = data/input/test.csv
output_dir = data/output
num_variants = 3
max_questions = 10
should_generate_pdf = True

[TECTONIC]
output_dir = data/output/pdf
quiet_mode = true
```

## Input Format

The input CSV file should contain the following columns:

- Question text
- Correct answer
- Additional options (if any)

## Output

The tool generates the following files in the `data/output` directory:

- CSV files: `csv/filename_variantX.csv`
- LaTeX files: `tex/filename_variantX.tex`
- PDF files: `pdf/filename_variantX.pdf` (if PDF generation is enabled)

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`
- Tectonic (for PDF generation) - Make sure it's added to your system PATH
