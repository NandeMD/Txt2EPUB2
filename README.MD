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

## For the onefile CLI build:
pyinstaller linux_cli_onefile.spec

## For the default CLI build:
pyinstaller linux_cli_dist.spec
```

Note: PyInstaller will create a file named `dist` on the project folder and put the final executable there.


## CLI Usage
```
positional arguments:
  input_folder_path     Path of the folder that contains all the .txt files.
  book_title            The name of the outted epub file.

options:
  -h, --help            show this help message and exit
  -o OUTPATH, --outpath OUTPATH
                        Path to the folder where the files will be extracted
                        to. Defaults to the executable's folder.
  -y, --yesall          Considers all (y/n) answers YES.
```

### Example:
```bash
# Input folder path is: "/home/user1/Desktop/MyBook"
# Generated epub name is: "MyBook"
# Epub file output path is: "/home/user1/Desktop"

./TXT2EPUB_CLI_V1.0.0 /home/user1/Desktop/MyBook MyBook -y -o /home/user1/Desktop
```
