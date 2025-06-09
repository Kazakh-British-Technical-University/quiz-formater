import subprocess
import os
import configparser

def generate_pdf(tex_path: str, config: configparser.ConfigParser) -> str:
    """
    Generate PDF from LaTeX file using Tectonic
    
    Args:
        tex_path: Path to the LaTeX file
        config: Configuration object containing Tectonic settings
    
    Returns:
        Path to the generated PDF file
    """
    # Get output directory from config
    output_dir = config['TECTONIC']['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    # Build tectonic command
    cmd = ['tectonic', tex_path, f'--outdir={output_dir}']
    
    try:
        subprocess.run(cmd, check=True)
        pdf_path = os.path.join(output_dir, os.path.basename(tex_path).replace('.tex', '.pdf'))
        print(f"PDF generated at {pdf_path}")
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")
        return None 