# TXTs-To-TXT

Scans a specified directory for all `.txt` files, reads their contents and combines them into a single output file named `combined_output.txt`.

## Overview

As this application processes the `.txt` files, the program uses a structured logging system which prints informational messages to the console and writes detailed logs to a rotating log file for debugging and auditing. It tracks the number of files processed, any read errors encountered and the total number of bytes collected before writing the final combined result. The logging system ensures logs do not grow indefinitely by rotating them once they reach a specified size. In the end, the script outputs a summary of the operation, providing visibility into how many files were successfully merged and whether any errors occurred.

## Set Up

Below are instructions for installing and running this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository: `git clone git@github.com:devbret/txts-to-txt.git`

4. Navigate to the repo's directory: `cd txts-to-txt`

5. Create a virtual environment: `python3 -m venv venv`

6. Activate your virtual environment: `source venv/bin/activate`

7. Place your `.TXT` files into the `input` directory of this repo

8. Use the following command to process: `python3 app.py`

9. The results will be returned to you at the root of this repo as a `.TXT` file

10. Exit the virtual environment: `deactivate`

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Combine all `.TXT` files from an input directory into a single `.TXT` file

- Log progress, debug details, errors and a final processing summary to both the console and a rotating log file

- Track how many files were processed, how many read errors occurred and the total UTF-8 byte size of the combined content

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
