from jinja2 import Environment, FileSystemLoader
import pandas as pd
import os
import re

def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        return text
    latex_special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    regex = re.compile('|'.join(re.escape(key) for key in latex_special_chars.keys()))
    return regex.sub(lambda match: latex_special_chars[match.group()], text)


def render_latex_with_jinja(df, template_path, output_path, variant_id=1):
    questions = []
    for _, row in df.iterrows():
        questions.append({
            "text": escape_latex(row["Question Text"]),
            "options": [escape_latex(row["Option A"]), escape_latex(row["Option B"]), escape_latex(row["Option C"]), escape_latex(row["Option D"])]
        })

    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    rendered = template.render(
        title="Exam sheet",
        questions=questions,
        variant_id=escape_latex(variant_id)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"LaTeX generated at {output_path}")
    return rendered
