from jinja2 import Environment, FileSystemLoader
import os
from .utils import escape_latex, format_title

def render_latex_with_jinja(df, template_path, output_path, variant_id=1):
    questions = []
    for _, row in df.iterrows():
        questions.append({
            "text": escape_latex(row["Question Text"]),
            "options": [escape_latex(row["Option A"]), escape_latex(row["Option B"]), escape_latex(row["Option C"]), escape_latex(row["Option D"])]
        })

    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Get the base filename from the output path and format it as title
    title = format_title(output_path)

    rendered = template.render(
        title=title,
        questions=questions,
        variant_id=variant_id
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"LaTeX generated at {output_path}")
    return rendered
