# Question Exam Tool

A Python CLI tool to generate exam variants from an Excel or CSV question bank with LaTeX output support.

## Features

- Group-based question selection
- Filtering and randomization
- LaTeX exam sheet generation
- Multiple variant support

# Requirements

1. Install required Python packages via requirements.txt:
2. Install Tectonic and add to system PATH: https://github.com/tectonic-typesetting/tectonic/releases

## Usage

```bash
python main.py data/input/test.csv --num-variants 3
```

```bash
tectonic data/output/tex/exam_sheet_Variant_1.tex --outdir=data/output/pdf/
```

```
Quiz-formater/
├── main.py                  # Entry point to run the project
├── requirements.txt         # Dependencies
├── README.md
├── config/                  # TODO
│   └── settings.yaml        # Optional settings (e.g., output paths, filters)
├── data/
│   ├── input/
│       ├── test.csv
│   └── output/
│       ├── csv/             # Dataframe of variants
│       ├── tex/             # Latex template of variants
│       ├── pdf/             # Generated PDF from Latex
├── src/
│   ├── __init__.py
│   ├── io_handler.py        # Read/write Excel/CSV
│   ├── question_ops.py      # Filtering, shuffling, tagging, etc.
│   └── latex_generator.py   # Generate LaTeX exam sheet
│   └── pdf_generator.py     # Generate PDF from Latex
└── templates/
    └── exam_template.tex    # Jinja2 LaTeX template
```
