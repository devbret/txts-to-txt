import logging
import sys
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = "combine_txt.log"
OUTPUT_FILENAME = "combined_output.txt"

EXIT_OK = 0
EXIT_FAILURE = 1
EXIT_PARTIAL = 2

logger = logging.getLogger("combiner")


@dataclass(frozen=True)
class CombineResult:
    succeeded: bool
    processed: int = 0
    read_errors: int = 0


def setup_logging() -> None:
    if logger.handlers:
        return

    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    fh = RotatingFileHandler(LOG_FILE, maxBytes=512_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(ch)
    logger.addHandler(fh)


def combine_txt_files(
    directory: str | Path, output_filename: str = OUTPUT_FILENAME
) -> CombineResult:
    logger.info("Starting combine in: %s", directory)

    processed = 0
    read_errors = 0
    total_bytes = 0

    try:
        entries = sorted(Path(directory).iterdir())
    except OSError:
        logger.exception("Failed to list directory '%s'", directory)
        return CombineResult(succeeded=False)

    txt_files = [
        path
        for path in entries
        if path.is_file() and path.suffix.lower() == ".txt" and path.name != output_filename
    ]
    if not txt_files:
        logger.warning("No .txt files found in: %s", directory)

    output_path = Path(output_filename)
    try:
        with open(output_path, "w", encoding="utf-8") as output_file:
            for path in txt_files:
                try:
                    content = path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    read_errors += 1
                    logger.exception("Failed to read %s", path.name)
                    continue
                if content and not content.endswith("\n"):
                    content += "\n"
                output_file.write(f"--- {path.name} ---\n")
                output_file.write(content)
                processed += 1
                total_bytes += len(content.encode("utf-8"))
                logger.debug("Added file: %s", path)
    except OSError:
        logger.exception("Failed to write output file")
        return CombineResult(succeeded=False, processed=processed, read_errors=read_errors)

    logger.info("Combined file saved to: %s", output_path)
    logger.info(
        "Summary - files processed: %d, read errors: %d, "
        "content bytes written (excluding separators): %d",
        processed,
        read_errors,
        total_bytes,
    )
    return CombineResult(succeeded=True, processed=processed, read_errors=read_errors)


def main() -> int:
    setup_logging()
    result = combine_txt_files(Path.cwd() / "input")
    if not result.succeeded:
        return EXIT_FAILURE
    if result.read_errors:
        logger.warning(
            "Completed with %d read error(s); exiting with status %d",
            result.read_errors,
            EXIT_PARTIAL,
        )
        return EXIT_PARTIAL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
