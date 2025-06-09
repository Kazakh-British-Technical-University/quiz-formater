from src.io_handler import read_questions, save_questions
from src.question_ops import generate_exam_variants
from src.latex_generator import render_latex_with_jinja
from src.pdf_generator import generate_pdf
import typer
import configparser

from src.utils import format_title

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

app = typer.Typer()

@app.command()
def create_exam(
    input_path: str = typer.Option(
        default=config['DEFAULT']['input_path'],
        help="Path to the input CSV file"
    ),
    num_variants: int = typer.Option(
        default=int(config['DEFAULT']['num_variants']),
        help="Number of exam variants to generate"
    ),
    max_questions: int = typer.Option(
        default=int(config['DEFAULT']['max_questions']),
        help="Maximum number of questions per variant"
    ),
    should_generate_pdf: bool = typer.Option(
        default=config.getboolean('DEFAULT', 'should_generate_pdf', fallback=False),
        help="Whether to generate PDF files from LaTeX"
    )
):
    df = read_questions(input_path)
    variants = generate_exam_variants(df, num_variants, max_questions)
    filename = format_title(input_path)

    for name, v_df in variants.items():
        tex_path = f"{config['DEFAULT']['output_dir']}/tex/{filename}_{name}.tex"

        save_questions(v_df, f"{config['DEFAULT']['output_dir']}/csv/{filename}_{name}.csv") 
        render_latex_with_jinja(v_df, "templates/exam_template.tex", tex_path, name)
        
        if should_generate_pdf:
            generate_pdf(tex_path, config)

    typer.echo("✅ Exams and LaTeX files created.")
    if should_generate_pdf:
        typer.echo("✅ PDF files generated.")
    

if __name__ == "__main__":
    app()
