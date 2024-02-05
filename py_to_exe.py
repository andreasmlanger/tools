"""
Converts PY to EXE and saves to 'Downloads' directory
Required version: pyinstaller==5.13.2 (Version 6 causes Windows firewall to abort the conversion!)
To be included files need to be in a folder 'data' in the PY file directory
Hidden import modules need to be in a folder '.hidden-imports' in the PY file directory
"""

import os
import stat
import sys
import subprocess
import shutil


CONSOLE = False
SAME_DIRECTORY_FILES_TO_PACK = ('.json', '.env', '.emails')  # these also go into the exe


def clean_up(path_):
    for folder in ['build', 'dist', os.path.join(path_, '__pycache__')]:
        while os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except OSError as e:
                os.chmod(e.filename, stat.S_IWRITE)  # change 'read-only' permission


pyinstaller = sys.executable.replace('python.exe', 'Scripts\\pyinstaller.exe')
if not os.path.isfile(pyinstaller):
    sys.exit('pyinstaller module not found')
downloads_dir = (os.environ['USERPROFILE'] + '\\Downloads').replace('\\', '\\\\')

path = input('\033[94m' + 'Enter path of PY file to be converted to EXE:\n')

py_files = [file for file in os.listdir(path) if file.endswith('.py')]

if len(py_files) == 0:
    sys.exit('No PY files found.')
elif len(py_files) == 1:
    print('\033[93m' + py_files[0] + ' \033[94m' + 'was found')
    py_file = py_files[0]
else:
    print('The following PY files were found:')
    for i in range(len(py_files)):
        print('\033[94m' + '(' + '\033[93m' + str(i) + '\033[94m' + ') ' + '\033[93m' + py_files[i])
    nr = input('\033[94m' + 'Enter index of PY file that should be converted to EXE:\n')
    if not nr.isnumeric() or int(nr) not in list(range(len(py_files))):
        sys.exit('Invalid index.')
    py_file = py_files[int(nr)]

spec_file = path + '\\' + py_file.replace('.py', '.spec')
data_folder = path + '\\' + 'data'
additional_files = [f for f in os.listdir(path) if f.endswith(SAME_DIRECTORY_FILES_TO_PACK)]
hidden_imports_folder = path + '\\' + '.hidden-imports'
icon_file = path + '\\' + 'data' + '\\' + 'icon.ico'

app_name = input('\033[94m' + '\n\nEnter name of application:\n')

if app_name == '':
    app_name = py_file[:-3]

# Create spec file
with open(spec_file, 'w') as f:
    f.writelines("import PyInstaller.config\nPyInstaller.config.CONF['distpath'] = '" + downloads_dir + "'\n\n")
    f.writelines("block_cipher = None\n\n\na = Analysis(['" + py_file + "'],\npathex=[],\nbinaries=[],\ndatas=[")

    if os.path.exists(data_folder):
        f.writelines("('data\\\\', 'data'),")
    for file in additional_files:
        f.writelines(f"('{file}', '.'),")
    if os.path.exists(hidden_imports_folder):
        f.writelines("('.hidden-imports\\\\', '.')")

    f.writelines("],\nhiddenimports=[],\nhookspath=[],\nruntime_hooks=[],\nexcludes=[],\n")
    f.writelines("win_no_prefer_redirects=False,\nwin_private_assemblies=False,\ncipher=block_cipher)\n\n")
    f.writelines("pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)\n")
    f.writelines("exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, name='" + app_name + "', ")
    f.writelines("debug=False, strip=False, upx=True, runtime_tmpdir=None, console=" + str(CONSOLE))

    if os.path.exists(icon_file):
        f.writelines(", icon='data\\\\icon.ico')")
    else:
        print("No icon found. If you would like to add an icon, copy a file 'icon.ico' into a folder called 'data'.")
        f.writelines(")")

clean_up(path)
subprocess.call([pyinstaller, spec_file])
clean_up(path)

print('\033[36m' + 'PY successfully converted to EXE!')
