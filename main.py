import re
import logging
from pathlib import Path
import argparse
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

REDACTED = "[REDACTED]"

DEFAULT_PATTERN_KINDS = {
    r"\b\d{3}-\d{2}-\d{4}\b": "SSN pattern",
    # The card pattern only covers numbers starting with 4, at 13 or 16
    # digits, and there is no Luhn check. Other issuers are invisible to
    # the defaults, and any 4-led digit run of the right length counts,
    # valid card or not.
    r"\b4[0-9]{12}(?:[0-9]{3})?\b": "credit card pattern",
}


def pattern_kind(pattern):
    return DEFAULT_PATTERN_KINDS.get(pattern, f"pattern '{pattern}'")


def compile_patterns(patterns):
    """
    Compile all patterns before any scanning. Raises re.error on an
    invalid pattern, which main turns into exit 1 before any file is read.
    Returns a list of (kind, compiled pattern) pairs.
    """
    compiled = []
    for pattern in patterns:
        compiled.append((pattern_kind(pattern), re.compile(pattern)))
    return compiled


def setup_argparse():
    """
    Set up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(
        description="Scan files for sensitive information patterns. Exit status: 0 on a clean scan of real content, 2 when any match is found, 1 on an error, an invalid pattern, or when nothing was scanned. Matched values are never printed; findings are reported by pattern kind, file, and count only."
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

def scan_file(file_path, compiled_patterns):
    """
    Scan a single file for sensitive information based on provided patterns.

    Returns a dict with per kind counts, a total match count, and the
    number of bytes read, or None on a scan error (a distinct error
    result, never an empty or clean result). Matched values themselves
    are counted only and are never returned or logged.
    """
    try:
        # Undecodable bytes are dropped, not treated as an error, so binary
        # files scan as whatever text survives decoding. A sensitive value with
        # a bad byte inside it can be split by that drop and missed. The byte
        # count in the result is the file's size on disk, not the number of
        # characters that were actually searched.
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            logging.info(f"Scanning file: {file_path}")
            content = file.read()
        counts = {}
        total = 0
        for kind, compiled in compiled_patterns:
            # findall counts non-overlapping matches, and the matched values are
            # counted and discarded in this same expression's result. Nothing
            # downstream ever sees a value, which is the point of this tool: the
            # report carries kinds and counts only.
            found = compiled.findall(content)
            if found:
                counts[kind] = counts.get(kind, 0) + len(found)
                total += len(found)
        return {"counts": counts, "total": total, "bytes": Path(file_path).stat().st_size}
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None


def report_findings(file_path, result):
    parts = "; ".join(f"{kind}: {count} match{'es' if count != 1 else ''} {REDACTED}" for kind, count in result["counts"].items())
    logging.info(f"Sensitive data found in {file_path}: {parts}")


def main():
    """
    Main function to handle file scanning.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    target_path = Path(args.filepath)

    # Compile all patterns before any scanning.
    try:
        compiled_patterns = compile_patterns(args.patterns)
    except re.error as e:
        logging.error(f"Invalid pattern: {e}. No files were scanned.")
        print(f"Invalid pattern: {e}. No files were scanned.")
        sys.exit(1)

    if not target_path.exists():
        logging.error("The specified path does not exist.")
        sys.exit(1)

    files_scanned = 0
    matches_found = 0
    bytes_read = 0
    had_error = False

    if target_path.is_file():
        result = scan_file(target_path, compiled_patterns)
        if result is None:
            had_error = True
            logging.error(f"Failed to scan file: {target_path}")
        else:
            files_scanned += 1
            bytes_read += result["bytes"]
            matches_found += result["total"]
            if result["total"]:
                report_findings(target_path, result)
            else:
                logging.info(f"No sensitive data found in {target_path}.")
    elif target_path.is_dir() and args.recursive:
        logging.info(f"Scanning directory: {target_path} recursively.")
        # rglob reaches hidden files and binary files alike, and follows the
        # directory as it exists at scan time. A file created mid-scan by
        # another process may or may not appear, and a file that vanishes
        # between listing and reading lands in the error count.
        for file in target_path.rglob("*"):
            if file.is_file():
                result = scan_file(file, compiled_patterns)
                if result is None:
                    had_error = True
                    logging.error(f"Failed to scan file: {file}")
                    continue
                files_scanned += 1
                bytes_read += result["bytes"]
                matches_found += result["total"]
                if result["total"]:
                    report_findings(file, result)
    else:
        logging.error("Invalid option. Use --recursive to scan directories.")
        sys.exit(1)

    logging.info(f"Scan summary: files scanned: {files_scanned}, matches found: {matches_found}, bytes read: {bytes_read}")
    print(f"Scan summary: files scanned: {files_scanned}, matches found: {matches_found}, bytes read: {bytes_read}")

    if had_error:
        logging.error("Scan failed for at least one file.")
        sys.exit(1)

    if files_scanned == 0 or bytes_read == 0:
        logging.error("Nothing was scanned: no file content was scanned.")
        print("Nothing was scanned: no file content was scanned.")
        sys.exit(1)

    # Exit 2 is a finding, not a failure: the scan worked and found
    # something. Exit 1 is reserved for errors and for scans that read
    # nothing, and exit 0 means real content was scanned and was clean.
    if matches_found:
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
