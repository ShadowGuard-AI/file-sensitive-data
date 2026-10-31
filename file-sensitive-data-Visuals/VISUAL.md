# file-sensitive-data, drawn out

I made these five pictures because the whole tool is one small file,
main.py, and its shape is easier to show than to describe. Everything
in them comes from that file: setup_argparse, scan_file, and main.

## The visuals

- [architecture.svg](architecture.svg): the system shape. One entry
  point at the top, the two helpers under it, and main() in the middle
  picking between a single file scan and a recursive directory scan.
  Logging lines are the only output.
- [data-flow.svg](data-flow.svg): what happens inside scan_file, left
  to right. A file is read as UTF-8 text, re.findall runs once per
  pattern, and a plain list of matched strings comes out.
- [flowchart.svg](flowchart.svg): a run, followed as decisions. The
  path must exist, a directory needs --recursive, and both failures
  exit with status 1.
- [product-map.svg](product-map.svg): the product in one frame: who it
  serves, what goes in, what comes out, and where it stops.
- [statistics.svg](statistics.svg): the numbers from the table below,
  drawn as bars on paper: lines by kind, with the file and commit
  counts noted under them.

Each sheet also ships as a PNG beside its SVG (architecture.png,
flowchart.png, and so on): the same drawing, finished as a photograph
of the paper page.

Every sheet here is drawn to look like what it is: a page sketched by
hand on paper, and each one is signed GK somewhere in the drawing,
never twice in the same place, because that is what I do with a page
I made.

## Written product map

What it is: a command line scanner that searches a file, or a
directory tree, for text patterns that look like sensitive data. By
default it looks for US social security numbers in NNN-NN-NNNN form
and Visa style card numbers starting with 4, at 13 or 16 digits.

Who it serves: me, checking a file or a folder before I share it, and
anyone doing the same first pass by hand.

Capabilities, grouped:

- Scanning: scan_file reads one file as UTF-8 text with undecodable
  bytes ignored, runs every pattern with re.findall, and returns the
  matches as one list.
- Choosing targets: one file path per run, or a directory tree walked
  with rglob when --recursive is set. A directory without the flag is
  refused, and a path that does not exist exits with status 1.
- Patterns: the two defaults above, replaced as a set by one or more
  --patterns regular expressions when I supply my own.
- Reporting: logging output only. A found line lists the matches for
  that file; a clean file gets a line saying no sensitive data was
  found. No report file is written.

Inputs: one file or directory path, plus the optional --patterns and
--recursive flags. Outputs: the logging lines described above, on the
terminal.

Boundaries, what it does NOT do: pattern matching only. It can miss
sensitive data in other formats (card numbers from issuers that do
not start with 4, numbers written with spaces, encoded data) and it
can flag harmless numbers that happen to match. It does not change,
move, or delete anything it scans, and it does not try to judge
whether a match is a real secret.

## Statistics, with citations

Counted 2026-10-30, from the clone this folder ships in, at the
commit before this visuals work (9356655).

| Number | Value | How it was counted, and from what |
|---|---|---|
| Files in the repo | 5 | git ls-files in the clone, counted 2026-10-30 |
| Python lines | 84 | Line count over the 1 tracked .py file (main.py), binary and image files excluded, 2026-10-30 |
| Markdown lines | 67 | Line count over the 1 tracked .md file (README.md), same method, 2026-10-30 |
| License text lines | 674 | Line count over the 1 tracked file with no extension (LICENSE), same method, 2026-10-30 |
| Commits | 6 | git log in the clone, counted 2026-10-30 |
| First commit | 2025-01-02 | git log, oldest entry, 2026-10-30 |
| Last commit before this one | 2026-10-30 | git log, newest entry, 2026-10-30 |
| Tests | 0 test files, no suite to run | File listing of the clone: no test file is tracked, counted 2026-10-30. No pass is claimed. I smoke ran the CLI instead: python3 main.py on a sample file holding an SSN and a card number printed both matches and exited 0, and a missing path exited 1, run 2026-10-30 |
| Languages (API) | Python 2,565 bytes | GitHub API, GET /repos/ShadowGuard-AI/file-sensitive-data/languages, read 2026-10-30 |
| Repo size (API) | 69 KB | GitHub API, GET /repos/ShadowGuard-AI/file-sensitive-data, size field, read 2026-10-30 |
| Stars / forks (API) | 1 / 0 | Same API response, read 2026-10-30 |

External statistics: none. No outside number says anything honest
about this repo, so the repo's own numbers are the whole table.

## Roadmap summary

Done: the scanner working as the README describes, with the exit
codes for bad paths fixed. Working now: nothing in flight. Next, if
I return to it: a small test file for scan_file, since the repo has
none. The full roadmap, with the Later and Not planned sections, is
in [ROADMAP.md](ROADMAP.md).
