import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "combine_txt.log"

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("combiner")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    fh = RotatingFileHandler(LOG_FILE, maxBytes=512_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.handlers.clear()
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def combine_txt_files(directory: str, output_filename: str = "combined_output.txt") -> None:
    logger = setup_logging()
    logger.info(f"Starting combine in: {directory}")
    combined_lines = []

    processed = 0
    read_errors = 0
    total_bytes = 0

    try:
        filenames = os.listdir(directory)
    except Exception as e:
        logger.exception(f"Failed to list directory '{directory}': {e}")
        return

    for filename in filenames:
        if filename.endswith(".txt") and filename != output_filename:
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    combined_lines.append(content)
                    processed += 1
                    total_bytes += len(content.encode("utf-8", errors="ignore"))
                    logger.debug(f"Added file: {filepath}")
            except Exception as e:
                read_errors += 1
                logger.exception(f"Failed to read {filename}: {e}")

    output_path = os.path.join(".", output_filename)
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(combined_lines))
        logger.info(f"Combined file saved to: {output_path}")
    except Exception as e:
        logger.exception(f"Failed to write output file: {e}")
        return

    logger.info(
        f"Summary — files processed: {processed}, read errors: {read_errors}, "
        f"bytes written (pre-UTF8 join): {total_bytes}"
    )

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), "input")
    combine_txt_files(input_directory)
