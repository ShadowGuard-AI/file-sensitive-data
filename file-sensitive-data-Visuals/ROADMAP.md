# file-sensitive-data roadmap

Written 2026-10-30 from the repo as it stands. No dates on the future
items, because I do not know when I will be back in this code, and a
date I invent here would be a small lie in a public file.

## Done

- The scanner itself: setup_argparse, scan_file, and main in one
  standard library file, main.py.
- Default patterns for SSN numbers in NNN-NN-NNNN form and Visa style
  card numbers starting with 4, at 13 or 16 digits.
- A --patterns option that replaces the defaults with my own regular
  expressions, and a --recursive option for directory trees.
- Exit codes that match the README: a missing path and a directory
  without --recursive both exit with status 1 (fixed 2026-10-30).
- First version of these visuals.

## Working now

- Nothing in flight. The repo is in a working state as of the
  2026-10-30 campaigns. I found no TODO or FIXME notes in the code.

## Next

- A small test file for scan_file and for the two exit paths in main.
  The repo has no tests at all, and that is the one gap I know about
  and admit here. The CLI behaviour itself I checked by hand on
  2026-10-30 with a sample file.

## Later

- Nothing honest to put here yet. I have not kept a list of patterns
  I want to add, and I will not invent one for this page.

## Not planned

- Writing report files. The logging output is the report, and a
  second output shape would need a reason I do not have.
- Judging whether a match is a real secret. The tool reports pattern
  matches; calling them confirmed secrets would overstate what a
  regex can know.
