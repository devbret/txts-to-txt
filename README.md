# TXTs-To-TXT

Python utility which merges `.txt` files from an input directory into a single `combined_output.txt` file, while logging progress to the console and a log file.

## Application Overview

Files are processed in alphabetical order, so the combined output is identical and the extension check is case-insensitive. Each file's contents are written beneath a separator line, making it easy to see where each original document begins and every file is guaranteed to end with a newline so no two documents ever run together.

A structured logging system prints messages to the console while writing debug logs to a log file and every run ends with a summary. Files which cannot be read or decoded are skipped and counted, and the exit status reflects the outcome. The core behaviors are covered by an automated test suite running in continuous integration on every push and pull request.

## Basic Setup Instructions

Below are instructions for installing, running and testing this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/) (version 3.10 or newer)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository: `git clone git@github.com:devbret/txts-to-txt.git`

4. Navigate to the repo's directory: `cd txts-to-txt`

5. Place your `.txt` files into the `input` directory of this repo

6. Run the program: `python3 app.py`

7. The results will be saved to `combined_output.txt` at the root of this repo

### Tests

1. Install the tools: `pip install pytest ruff`

2. Run the tests: `pytest`

3. Check linting and formatting: `ruff check . && ruff format --check .`

## Other Considerations

Below you will find information not covered in the installation and use sections above. Including the abilities this repo is intended to demonstrate. As well as an overview of the license this code is made available with. And a way to contact the maintainer with questions, suggestions and collaboration opportunities.

### Abilities Demonstrated

This project repo is intended to demonstrate an ability to do the following:

- Combine all `.txt` files from an input directory into a single `.txt` file

- Log progress, debug details, errors and a final processing summary

- Track how many (1) files are processed, (2) read errors occur and (3) total UTF-8 byte size of combined content

- Cover core behaviors with an automated test suite which runs in continuous integration

### License Information

This repository is distributed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense and sell copies of this software, including as part of proprietary or commercial work. The single condition is the copyright and permission notices contained in the LICENSE file must be included with any copy or substantial portion of the software that you redistribute. The software is provided "as is", without warranty of any kind, and the copyright holder is not liable for any claim or damages arising from its use.

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
