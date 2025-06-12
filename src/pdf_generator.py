import subprocess
import os
import configparser

def generate_pdf(tex_path: str, config: configparser.ConfigParser, engine: str = 'tectonic') -> str:
    """
    Generate PDF from LaTeX file using specified LaTeX engine
    
    Args:
        tex_path: Path to the LaTeX file
        config: Configuration object containing engine settings
        engine: LaTeX engine to use ('tectonic' or 'miktex')
    
    Returns:
        Path to the generated PDF file
    """
    # Get output directory from config
    output_dir = config['DEFAULT']['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    # Build command based on engine
    if engine == 'tectonic':
        cmd = ['tectonic', tex_path, f'--outdir={output_dir}']
    elif engine == 'miktex':  # miktex
        cmd = ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', tex_path]
    else:
        raise ValueError(f"Unsupported LaTeX engine: {engine}. Please use 'tectonic' or 'miktex'.")
        
    try:
        subprocess.run(cmd, check=True)
        pdf_path = os.path.join(output_dir, os.path.basename(tex_path).replace('.tex', '.pdf'))
        print(f"PDF generated at {pdf_path}")
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")
    return None 