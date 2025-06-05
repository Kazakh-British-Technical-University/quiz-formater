from src.io_handler import read_questions, save_questions
from src.question_ops import generate_exam_variants
from src.latex_generator import render_latex_with_jinja
from src.pdf_generator import compile_pdf_from_tex_string
import typer

app = typer.Typer()

@app.command()
def create_exam(input_path: str, num_variants: int = 2):
    df = read_questions(input_path)
    variants = generate_exam_variants(df, num_variants)

    for name, v_df in variants.items():
        tex_path = f"data/output/tex/exam_sheet_{name}.tex"

        save_questions(v_df, f"data/output/csv/{name}.csv") # CSV
        rendered_tex = render_latex_with_jinja(v_df, "templates/exam_template.tex", tex_path, name)
        # compile_pdf_from_tex_string(rendered_tex, tex_path)

    typer.echo("✅ Exams and LaTeX files created.")
    

if __name__ == "__main__":
    app()
