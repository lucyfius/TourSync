import PyInstaller.__main__
import os
import shutil

def build_exe():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Build the executable
    PyInstaller.__main__.run([
        'client/gui.py',  # your main script
        '--onefile',      # create a single executable
        '--windowed',     # prevent console window from appearing
        '--name=TourScheduler',  # name of your executable
        '--add-data=.env;.',  # include .env file
        # Add icon if you have one:
        # '--icon=path/to/icon.ico',
    ])
    
    print("Build complete! Executable is in the 'dist' folder")

if __name__ == "__main__":
    build_exe() 