from src.io_handler import read_questions, save_questions
from src.question_ops import generate_exam_variants
from src.latex_generator import render_latex_with_jinja
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
        'template_path': 'templates/test.tex'
    },
    'TECTONIC': {
        'output_dir': 'data/output/pdf',
        'quiet_mode': 'true'
    }
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
    t: str = typer.Option( # Template path
        default=config['DEFAULT']['template_path'],
        help="Path to the LaTeX template file"
    )
):
    # Create output directories if they don't exist
    output_dir = Path(config['DEFAULT']['output_dir'])
    for subdir in ['csv', 'pdf', 'tex']:
        (output_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Resolve template path
    if not os.path.isabs(t):
        t = str(get_base_path() / t)
    
    df = read_questions(i)
    variants = generate_exam_variants(df, n, m)
    filename = format_title(i)

    for name, v_df in variants.items():
        tex_path = f"{config['DEFAULT']['output_dir']}/tex/{filename}_{name}.tex"

        save_questions(v_df, f"{config['DEFAULT']['output_dir']}/csv/{filename}_{name}.csv") 
        
        if p:
            render_latex_with_jinja(v_df, t, tex_path, name)
            generate_pdf(tex_path, config)

    typer.echo("✅ Exams and LaTeX files created.")
    if p:
        typer.echo("✅ PDF files generated.")

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
