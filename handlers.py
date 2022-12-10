from itertools import zip_longest
from pathlib import PurePath
from collections.abc import Callable


def lines(filename: str, chunksize: int) -> None:
    filename = PurePath(filename)
    with open(filename) as fin:
        for part, group in enumerate(zip_longest(*([iter(fin)] * chunksize))):
            newfile = filename.with_stem(f"line_part_{part}_{filename.stem}")

            with open(newfile, 'w') as fout:
                for j, line in enumerate(group, 1):
                    if line is None:
                        break
                    if j == len(group):
                        fout.write(line.rstrip())
                    else:
                        fout.write(line)


def chars(filename: str, chunksize: int) -> None:
    filename = PurePath(filename)
    groups = []
    with open(filename) as fin:
        c = fin.read(chunksize)
        while c:
            groups.append(c)
            c = fin.read(chunksize)
        for part, group in enumerate(groups, 0):
            newfile = filename.with_stem(f"line_part_{part}_{filename.stem}")
            with open(newfile, 'w') as fout:
                line = 0
                for j, ch in enumerate(group, 1):
                    if ch is None:
                        break
                    if j == len(group) or line == 0:
                        fout.write(ch.rstrip())
                    else:
                        fout.write(ch)
                    line += 1


HANDLERS: dict[str, Callable[[str, int], None]] = {
    "lines": lines,
    "chars": chars
}
