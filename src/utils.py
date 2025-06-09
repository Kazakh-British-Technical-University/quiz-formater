import os, re

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

def format_title(path: str) -> str:
    # Remove file extension and split by hyphens or underscores
    basename = os.path.basename(path)
    base_name = os.path.splitext(basename)[0]
    words = re.split(r'[-_]', base_name)
    
    # Capitalize each word
    capitalized_words = [word.capitalize() for word in words]
    
    # Join with spaces
    return ' '.join(capitalized_words)