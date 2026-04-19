<img width="2816" height="1536" alt="file_organizer" src="https://github.com/user-attachments/assets/2902294e-1cf5-4d55-91e6-3de85af3725b" />

Setup guide

Below is a detailed step-by-step installation and usage guide in English for the script. Python’s standard library already includes modules such as os, shutil, and argparse, so no third-party packages are required for this script.

Overview
This script helps you process files in one or more directories by scanning them, optionally filtering them by file type, renaming them with a customizable pattern, and sorting them into output folders. It is built with Python standard-library tools commonly used for file automation, including os.walk() for directory traversal and shutil.move() / shutil.copy2() for file operations.

Requirements
You need Python 3 installed on your computer. The script uses built-in Python modules only, so you do not need to install any external dependencies with pip.

Step 1: Install Python
Download and install Python 3 from the official Python website if it is not already installed on your machine. The standard library includes shutil, which provides high-level file operations such as copy, move, and recursive directory handling.

After installation, verify Python from the terminal or command prompt:


python --version
If that does not work, try:


python3 --version

Step 2: Create the script file
Create a new file named:

text
file_organizer.py
Open it in a code editor such as VS Code, Sublime Text, Notepad++, or any text editor you prefer. Paste the full Python code into that file and save it.

Step 3: Open your terminal
Open a terminal window:

On Windows: use Command Prompt, PowerShell, or Windows Terminal.

On macOS: use Terminal.

On Linux: use your preferred terminal emulator.

Then move into the folder where the script is saved:


cd /path/to/your/script/folder
Example:


cd "/Users/yourname/Desktop/python-tools"
or on Windows:


cd "C:\Users\yourname\Desktop\python-tools"

Step 4: Understand the required arguments
The script requires two positional arguments:

source — the folder containing the files you want to process.

output — the folder where the processed files will be copied or moved.

Basic syntax:


python file_organizer.py "SOURCE_FOLDER" "OUTPUT_FOLDER"
Example:


python file_organizer.py "/Users/john/Downloads/messy_files" "/Users/john/Desktop/sorted_files"

Step 5: Start with a safe test run
Before making any real changes, run the script in dry-run mode. A dry run is a recommended safety step for file automation because it shows what the script would do without actually renaming, copying, or moving files.

Example:


python file_organizer.py "/Users/john/Downloads/messy_files" "/Users/john/Desktop/sorted_files" --dry-run
What this does:

scans files,

decides how they would be renamed,

decides where they would be placed,

prints the planned operations,

makes no actual changes.

Step 6: Process files for real
Once the dry run looks correct, run the same command without --dry-run:


python file_organizer.py "/Users/john/Downloads/messy_files" "/Users/john/Desktop/sorted_files"
By default, this will:

process files in the top-level source directory,

copy files rather than move them,

sort them into subfolders by extension,

rename them using this default pattern: {date}_{index}_{original}.

Step 7: Enable recursive scanning
If your source folder contains many nested subfolders, use --recursive. Python commonly uses os.walk() for this kind of recursive directory traversal.

Example:


python file_organizer.py "/Users/john/Downloads/messy_files" "/Users/john/Desktop/sorted_files" --recursive
This will process files in:

the source folder,

all child folders,

all deeper subfolders.

Step 8: Filter by file type
Use --extensions if you want to process only certain file types. This is useful when you want to organize only images, documents, or videos.

Example for images:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --extensions jpg,jpeg,png,webp
Example for documents:


python file_organizer.py "/Users/john/Documents" "/Users/john/Desktop/docs_sorted" --recursive --extensions pdf,docx,txt,xlsx

Step 9: Choose how files are sorted into folders
The --sort-folder option controls how subfolders are created inside the output directory.

Available options:

extension — files are grouped by extension.

date — files are grouped by modification year and month.

first_letter — files are grouped by the first letter of the filename.

none — no subfolders are created.

Examples:

Sort by extension:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --sort-folder extension
Sort by date:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --sort-folder date
Sort by first letter:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --sort-folder first_letter
Disable sorting into subfolders:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --sort-folder none

Step 10: Customize file renaming
The --rename-pattern option lets you define how new filenames are generated. The script supports placeholders built from file metadata and the processing order.

Supported placeholders:

{original} — original filename without extension.

{ext} — file extension without the dot.

{date} — modification date in YYYY-MM-DD format.

{datetime} — modification date and time.

{size} — file size in bytes.

{index} — sequential number with leading zeros.

Example:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --rename-pattern "{index}_{original}"
This may produce names like:

text
0001_report
0002_invoice
0003_photo
Another example:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --rename-pattern "{date}_{original}"
This may produce names like:

text
2026-04-14_report.pdf
2026-04-14_photo.jpg
Step 11: Control processing order
The --order option determines the order in which files are processed before they are renamed. This matters especially if you use {index} in filenames.

Available options:

none — keep original discovery order.

name — sort alphabetically by filename.

mtime — sort by modification time.

ctime — sort by creation/change time.

size — sort by file size.

Example:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --order mtime --rename-pattern "{index}_{original}"

Step 12: Move files instead of copying
By default, the script copies files using shutil.copy2(), which attempts to preserve metadata such as timestamps. If you want to remove files from the source and place them into the output folder instead, use --move, which relies on shutil.move().

Example:


python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/output" --recursive --move
Important note:

copy keeps the original files in place.

move relocates them, so the source folder will lose those files after processing.

Step 13: Understand filename conflict protection
If two processed files would end up with the same final name, the script automatically prevents overwriting by adding suffixes such as _1, _2, and so on. This is important because file operations can otherwise overwrite existing destinations, depending on the function and platform behavior.

Example result:

text
report.pdf
report_1.pdf
report_2.pdf

Step 14: Common real-world examples
Example A: Organize all images from Downloads into folders by extension

python file_organizer.py "/Users/john/Downloads" "/Users/john/Desktop/images_sorted" --recursive --extensions jpg,jpeg,png,gif,webp --sort-folder extension
Example B: Move PDF and DOCX files into date-based folders

python file_organizer.py "/Users/john/Documents" "/Users/john/Desktop/docs_archive" --recursive --extensions pdf,docx --sort-folder date --move
Example C: Rename all files with a clean numeric prefix

python file_organizer.py "/Users/john/Desktop/input" "/Users/john/Desktop/output" --recursive --order name --rename-pattern "{index}_{original}"
Example D: Copy everything into one folder without subfolders

python file_organizer.py "/Users/john/Desktop/input" "/Users/john/Desktop/output" --recursive --sort-folder none

Step 15: Troubleshooting
Problem: “python is not recognized”
This usually means Python is not installed correctly or is not added to your system PATH. Reinstall Python and make sure the installer option for adding Python to PATH is enabled.

Problem: “Source directory does not exist”
Check that the source path is correct and that you used quotes around paths containing spaces.

Correct:


python file_organizer.py "C:\My Files\Input" "C:\My Files\Output"
Problem: Permission denied
Some folders are protected by the operating system, or some files may be in use by another application. Close programs that may be using the files, or run the terminal with sufficient permissions.

Problem: Unexpected renaming results
Run the script again with --dry-run first. Dry runs are a standard safety practice for scripts that rename, move, or delete files because they let you verify behavior before changes are applied.

Step 16: Best practices
Always test with --dry-run first.

Start on a small sample folder before using your full dataset.

Use copy mode first, then switch to move mode only after verification.

Keep a backup of important files before large batch operations.

Use clear rename patterns such as {date}_{index}_{original} to avoid confusion.

🛡️ License 🛡️

See [LICENSE](LICENSE) for details.
