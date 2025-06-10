import os
import platform
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Build executable for the current platform."""
    system = platform.system().lower()
    
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Clean previous builds
    for path in ['build', 'dist']:
        if os.path.exists(path):
            subprocess.run(['rm', '-rf', path], check=True)
    
    # Install PyInstaller if not already installed
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Create PyInstaller spec
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.ini', '.'),
        ('templates/test.tex', 'templates'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='quiz-converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('quiz-converter.spec', 'w') as f:
        f.write(spec_content)
    
    # Build executable
    subprocess.run(['pyinstaller', 'quiz-converter.spec'], check=True)
    
    # Clean up intermediate files
    dist_dir = Path('dist/quiz-converter')
    for file in dist_dir.glob('*.whl'):
        file.unlink()
    for file in dist_dir.glob('*.spec'):
        file.unlink()
    
    print(f"✅ Executable built successfully in dist/quiz-converter{'.exe' if system == 'windows' else ''}")
    print("📄 Template and config files are bundled with the executable")

if __name__ == '__main__':
    build_executable() 