from pathlib import Path
from contextlib import contextmanager
from contextlib import ExitStack
#partie 1 avec with

class TempFileWriter:
    def __enter__(self):
        self.filepath = Path("temp.txt")
        self.f = self.filepath.open("w")
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        self.filepath.unlink()

with TempFileWriter() as f:
    f.write("Contenu temporaire\n")

# partie 2 avec  Utilisation de contextlib.contextmanager
@contextmanager
def temp_file():
    path = Path("temp.txt")
    f = path.open("w")
    try:
        yield f
    finally:
        f.close()
        path.unlink()

with temp_file() as f:
    f.write("Autre test\n")

# utulisation multuple resource avec ExitStack

paths = ["a.txt", "b.txt", "c.txt"]
with ExitStack() as stack:
    files = [stack.enter_context(open(p, "w")) for p in paths]
    for f in files:
        f.write("test\n")