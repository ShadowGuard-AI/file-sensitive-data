![Banner](banner.png)

# file-sensitive-data

A command line scanner that searches a file, or a directory tree, for text patterns that look like sensitive data. By default it looks for US social security numbers in `NNN-NN-NNNN` form and Visa style card numbers starting with 4 (13 or 16 digits). Results are reported through the logging output; there is no separate report file.

## Requirements

- Python 3.10 or later
- No third party packages. The tool uses only the Python standard library.

## Install

There is no package to install. Clone the repository and run `main.py` directly:

```bash
git clone https://github.com/ShadowGuardAI/file-sensitive-data.git
cd file-sensitive-data
```

## Usage

```
python3 main.py [-h] [--patterns PATTERN [PATTERN ...]] [--recursive] filepath
```

- `filepath`: path to the single file or directory to scan (required, one path only)
- `--patterns PATTERN [PATTERN ...]`: one or more regular expressions to search for, space separated. Overrides the default SSN and card patterns.
- `--recursive`: required to scan a directory. Without it, passing a directory is an error and the tool exits with status 1.
- `-h`: show help and exit

A path that does not exist also exits with status 1.

## Examples

```bash
# Scan a single file with the default patterns
python3 main.py file.txt

# Scan a directory tree
python3 main.py directory/ --recursive

# Scan with a custom pattern
python3 main.py file.txt --patterns 'clean'
```

For a file containing `SSN 123-45-6789 and card 4111111111111111`, the output includes:

```
INFO - Sensitive data found in file.txt: ['123-45-6789', '4111111111111111']
```

For a file with no matches:

```
INFO - No sensitive data found in file.txt.
```

## Limitations

- Pattern matching only. It can miss sensitive data in other formats (for example card numbers from issuers that do not start with 4, numbers written with spaces, or encoded data) and can flag harmless numbers that happen to match. Use it alongside other security measures.
- Files are read as UTF-8 text with undecodable bytes ignored.
- Directory scans without `--recursive` are refused, and multiple file paths are not accepted in one run.

## License

GNU General Public License v3.0. See the `LICENSE` file.
