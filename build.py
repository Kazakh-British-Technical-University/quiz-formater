import os
import platform
import subprocess
import sys
from pathlib import Path

def build_executables():
    """Build executables for the current platform."""
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
    
    # Common data files
    datas = [
        ('config.ini', '.'),
        ('templates/test.tex', 'templates'),
    ]
    
    # Build CLI version
    cli_spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas={datas},
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
    name='quiz-converter-cli',
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
    
    # Build GUI version
    gui_spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui_main.py'],
    pathex=[],
    binaries=[],
    datas={datas},
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
    name='quiz-converter-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if '{system}' == 'windows' else None,
)
'''
    
    # Write and build CLI spec
    with open('quiz-converter-cli.spec', 'w') as f:
        f.write(cli_spec_content)
    subprocess.run(['pyinstaller', 'quiz-converter-cli.spec'], check=True)
    
    # Write and build GUI spec
    with open('quiz-converter-gui.spec', 'w') as f:
        f.write(gui_spec_content)
    subprocess.run(['pyinstaller', 'quiz-converter-gui.spec'], check=True)
    
    # Clean up intermediate files
    dist_dir = Path('dist')
    for file in dist_dir.glob('*.whl'):
        file.unlink()
    for file in dist_dir.glob('*.spec'):
        file.unlink()
    
    print("✅ Executables built successfully:")
    print(f"📄 CLI version: dist/quiz-converter-cli{'.exe' if system == 'windows' else ''}")
    print(f"📄 GUI version: dist/quiz-converter-gui{'.exe' if system == 'windows' else ''}")
    print("📄 Template and config files are bundled with the executables")

if __name__ == '__main__':
    build_executables() 