# Day 03 — Word frequency

## Objective
Read a file, count words, rank them. Handle a world where the file might not be there.

## Task
Write `wordfreq.py`, invoked as `python wordfreq.py <path>`.

It prints the 10 most frequent words in the file, one per line, formatted `<count> <word>`, most frequent first. Words are case-insensitive and stripped of surrounding punctuation.

Constraints:
- Standard library only, and `collections.Counter` is forbidden — count them yourself.
- On a missing or unreadable file, print a message to stderr and exit non-zero.

## Self-check
1. Ties in frequency are broken alphabetically.
2. An empty file prints nothing and exits 0.
3. A missing file prints a readable error and exits non-zero.
4. A file with fewer than 10 distinct words prints all of them without padding or erroring.
