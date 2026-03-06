# TXTs-to-TXT

Scans a specified directory for all `.txt` files, reads their contents and combines them into a single output file named `combined_output.txt`.

## Overview

As this application processes the `.txt` files, the program uses a structured logging system which prints informational messages to the console and writes detailed logs to a rotating log file for debugging and auditing. It tracks the number of files processed, any read errors encountered and the total number of bytes collected before writing the final combined result. The logging system ensures logs do not grow indefinitely by rotating them once they reach a specified size. In the end, the script outputs a summary of the operation, providing visibility into how many files were successfully merged and whether any errors occurred.
