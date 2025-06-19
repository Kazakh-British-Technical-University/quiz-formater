from src.io_handler import read_questions, save_questions
from src.question_ops import generate_exam_variants
from src.latex_generator import render_latex_with_jinja, render_all_variants_answers, render_all_variants_exam
from src.pdf_generator import generate_pdf
import typer
import configparser
import shutil
import os
from pathlib import Path
import sys

from src.utils import format_title

# Default configuration
DEFAULT_CONFIG = {
    'DEFAULT': {
        'input_path': 'data/input/test.csv',
        'output_dir': 'data/output',
        'num_variants': '3',
        'max_questions': '10',
        'should_generate_pdf': 'True',
        'should_generate_csv': 'False',
        'template_path': 'templates/test.tex',
        'answers_template_path': 'templates/answers.tex',
        'engine' : 'tectonic'
    },
}

def get_base_path():
    """Get the base path for the application."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys._MEIPASS)
    else:
        # Running as script
        return Path.cwd()

def get_config():
    """Get configuration from file or use defaults."""
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    
    # Try to read config.ini from the executable's directory
    config_path = get_base_path() / 'config.ini'
    if config_path.exists():
        config.read(config_path)
    
    return config

# Load configuration
config = get_config()

app = typer.Typer()

@app.command()
def create(
    i: str = typer.Option( # Input path to .csv
        default=config['DEFAULT']['input_path'],
        help="Path to the input CSV file"
    ),
    n: int = typer.Option( # Number of exam variants
        default=int(config['DEFAULT']['num_variants']),
        help="Number of exam variants to generate"
    ),
    m: int = typer.Option( # Max questions in variants 
        default=int(config['DEFAULT']['max_questions']),
        help="Maximum number of questions per variant"
    ),
    p: bool = typer.Option( # Generate pdf
        default=config.getboolean('DEFAULT', 'should_generate_pdf', fallback=False),
        help="Whether to generate PDF files from LaTeX"
    ),
    c: bool = typer.Option( # Generate csv
        default=config.getboolean('DEFAULT', 'should_generate_csv', fallback=False),
        help="Whether to generate CSV files with variants"
    ),
    t: str = typer.Option( # Template path
        default=config['DEFAULT']['template_path'],
        help="Path to the LaTeX template file"
    ),
    e: str = typer.Option( # Latex Engine to use
        default=config['DEFAULT']['engine'],
        help="LaTeX engine to use for PDF generation (tectonic/pdflatex)"
    ),
    out: str = typer.Option(
        default="single",
        help="Output mode: 'multiple' (separate files), 'single' (all-in-one), or 'both'",
    )
):
    # Create output directories if they don't exist
    output_dir = Path(config['DEFAULT']['output_dir'])
    for subdir in ['csv', 'pdf', 'tex']:
        (output_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Resolve template paths
    if not os.path.isabs(t):
        t = str(get_base_path() / t)
    answers_template = str(get_base_path() / config['DEFAULT']['answers_template_path'])
    
    df = read_questions(i)
    variants = generate_exam_variants(df, n, m)
    filename = format_title(i)

    # MULTIPLE mode: generate per-variant files
    if out in ["multiple", "both"]:
        for name, v_df in variants.items():
            tex_path = f"{config['DEFAULT']['output_dir']}/tex/{filename}_{name}.tex"
            answers_tex_path = f"{config['DEFAULT']['output_dir']}/tex/{filename}_{name}_answers.tex"

            if c:
                save_questions(v_df, f"{config['DEFAULT']['output_dir']}/csv/{filename}_{name}.csv") 
            
            if p:
                # Generate test variant
                render_latex_with_jinja(v_df, t, tex_path, name)
                generate_pdf(tex_path, config, e)
                # Generate answer sheet
                render_latex_with_jinja(v_df, answers_template, answers_tex_path, name)
                generate_pdf(answers_tex_path, config, e)

    # SINGLE mode: generate all-variants-in-one files
    if out in ["single", "both"] and p:
        all_answers_template = str(get_base_path() / "templates/answers_all_variants.tex")
        all_answers_tex_path = f"{config['DEFAULT']['output_dir']}/tex/{filename}_ALL_VARIANTS_answers.tex"
        render_all_variants_answers(variants, all_answers_template, all_answers_tex_path)
        generate_pdf(all_answers_tex_path, config, e)

        all_exam_template = str(get_base_path() / "templates/variants_all_in_one.tex")
        all_exam_tex_path = f"{config['DEFAULT']['output_dir']}/tex/{filename}_ALL_VARIANTS_exam.tex"
        render_all_variants_exam(variants, all_exam_template, all_exam_tex_path)
        generate_pdf(all_exam_tex_path, config, e)

    typer.echo("✅ Exam variants created successfully")
    if p:
        typer.echo("✅ PDF files generated (including answer sheets).")

@app.command()
def clean(
    d: str = typer.Option(  # Directory type to clean
        default="all",
        help="Directory type to clean (csv/pdf/tex/all)"
    )
):
    """Clean output directories"""
    output_dir = config['DEFAULT']['output_dir']
    dirs = {
        'csv': f"{output_dir}/csv",
        'pdf': f"{output_dir}/pdf",
        'tex': f"{output_dir}/tex"
    }
    
    if d == "all":
        for dir_path in dirs.values():
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                os.makedirs(dir_path)
                typer.echo(f"✅ Cleaned {dir_path}")
    elif d in dirs:
        dir_path = dirs[d]
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
            typer.echo(f"✅ Cleaned {dir_path}")
    else:
        typer.echo(f"❌ Invalid directory type: {d}")
        typer.echo("Available types: csv, pdf, tex, all")

if __name__ == "__main__":
    app()
