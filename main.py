import re
import logging
from pathlib import Path
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def setup_argparse():
    """
    Set up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(
        description="Scan files for sensitive information patterns."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the file or directory to scan."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        nargs='+',
        default=[r"\b\d{3}-\d{2}-\d{4}\b", r"\b4[0-9]{12}(?:[0-9]{3})?\b"],
        help="List of regex patterns to scan for (default: SSN and credit card patterns)."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan directories."
    )
    return parser

def scan_file(file_path, patterns):
    """
    Scan a single file for sensitive information based on provided patterns.
    """
    try:
        matches = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            logging.info(f"Scanning file: {file_path}")
            content = file.read()
            for pattern in patterns:
                matches.extend(re.findall(pattern, content))
        return matches
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

def main():
    """
    Main function to handle file scanning.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    target_path = Path(args.filepath)
    patterns = args.patterns

    if not target_path.exists():
        logging.error("The specified path does not exist.")
        return

    if target_path.is_file():
        matches = scan_file(target_path, patterns)
        if matches:
            logging.info(f"Sensitive data found in {target_path}: {matches}")
        else:
            logging.info(f"No sensitive data found in {target_path}.")
    elif target_path.is_dir() and args.recursive:
        logging.info(f"Scanning directory: {target_path} recursively.")
        for file in target_path.rglob("*"):
            if file.is_file():
                matches = scan_file(file, patterns)
                if matches:
                    logging.info(f"Sensitive data found in {file}: {matches}")
    else:
        logging.error("Invalid option. Use --recursive to scan directories.")

if __name__ == "__main__":
    main()