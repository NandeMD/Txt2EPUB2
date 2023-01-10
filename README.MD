# Txt2EPUB2

A really simlpe EPUB2 file creation script to convert multiple TXT files to a single EPUB2 book.

## How to use?
```bash
# Install requirements
pip install -r requirements.txt

# Run
python3 main.py
```


## Build
### On Linux
```bash
# First, create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

## For the onefile  build:
pyinstaller linux_onefile.spec

## For the default build:
pyinstaller linux_dist.spec
```

Note: PyInstaller will create a file named `dist` on the project folder and put the final executable there.