from jinja2 import Environment, FileSystemLoader
import os
from .utils import escape_latex, format_title

def render_latex_with_jinja(df, template_path, output_path, variant_id=1):
    questions = []
    for _, row in df.iterrows():
        for item in row:
            if item == item:
                print(item)

        option_keys = sorted(
            (key for key in row.keys() if key.startswith("Option ") and row[key] == row[key]),
            key=lambda k: int(k.split(" ")[1]) if k.split(" ")[1].isdigit() else k.split(" ")[1]
        )

        options = [escape_latex(row[key]) for key in option_keys]

        questions.append({
            "text": escape_latex(row["Question Text"]),
            "options": options,
            "answer": escape_latex(row["answer"]) if "answer" in row else ""
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

def render_all_variants_answers(variants_dict, template_path, output_path):
    """
    Render a LaTeX file with answers for all variants, each on a new page.
    variants_dict: dict of {variant_id: DataFrame}
    template_path: path to the Jinja2 LaTeX template
    output_path: where to write the .tex file
    """
    all_variants = []
    for variant_id, df in variants_dict.items():
        questions = []
        for _, row in df.iterrows():
            questions.append({
                "text": escape_latex(row["Question Text"]),
                "options": [escape_latex(row["Option A"]), escape_latex(row["Option B"]), escape_latex(row["Option C"]), escape_latex(row["Option D"])],
                "answer": escape_latex(row["answer"]) if "answer" in row else ""
            })
        all_variants.append({
            "variant_id": variant_id,
            "questions": questions
        })

    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Use the output filename as the quiz title
    title = format_title(output_path)

    rendered = template.render(
        title=title,
        variants=all_variants
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"All-variants answers LaTeX generated at {output_path}")
    return rendered

def render_all_variants_exam(variants_dict, template_path, output_path, variant_spacing="20pt"):
    """
    Render a LaTeX file with all exam variants, each on a new page, with tweakable spacing.
    variants_dict: dict of {variant_id: DataFrame}
    template_path: path to the Jinja2 LaTeX template
    output_path: where to write the .tex file
    variant_spacing: vertical space (LaTeX length, e.g., '20pt') between variants
    """
    all_variants = []
    for variant_id, df in variants_dict.items():
        questions = []
        for _, row in df.iterrows():
            questions.append({
                "text": escape_latex(row["Question Text"]),
                "options": [escape_latex(row["Option A"]), escape_latex(row["Option B"]), escape_latex(row["Option C"]), escape_latex(row["Option D"])],
                "answer": escape_latex(row["answer"]) if "answer" in row else ""
            })
        all_variants.append({
            "variant_id": variant_id,
            "questions": questions
        })

    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Use the output filename as the quiz title
    title = format_title(output_path)

    rendered = template.render(
        title=title,
        variants=all_variants,
        VariantSpacing=variant_spacing
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"All-variants exam LaTeX generated at {output_path}")
    return rendered
