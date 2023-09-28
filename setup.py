from cx_Freeze import setup, Executable

base = None    

executables = [Executable("opcclient.py", base=base)]

packages = ["time","sys","argparse","opcua"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}  

setup(
    name = "opcclient",
    options = options,
    version = "1.0",
    description = 'console client for opc servers',
    executables = executables
) 