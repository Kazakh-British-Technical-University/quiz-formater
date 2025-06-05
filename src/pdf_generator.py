import os
import pdflatex

def compile_pdf_from_tex_string(rendered_tex: str, output_path: str):
    """
    Compiles LaTeX content (as a string) into a PDF and saves it next to the output_path.
    """
    working_dir = os.path.dirname(output_path) or "."
    
    # First write the LaTeX content to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_tex)
    
    # Then compile it using PDFLaTeX
    pdf_obj = pdflatex.PDFLaTeX.from_texfile(output_path)
    pdf, log, completed_process = pdf_obj.create_pdf()

    output_pdf_path = os.path.splitext(output_path)[0] + ".pdf"
    with open(output_pdf_path, "wb") as f:
        f.write(pdf)

    print(f"📄 PDF compiled at {output_pdf_path}")
