import os
import stat
import tempfile
from pathlib import Path


TEXT = """Dear Judge,

Thank you for giving this contest more than a glance. Reading through stack after stack of submissions, weighing small turns of phrase, and staying sharp through long hours of comparing entries takes real patience. It is quiet, demanding work, and it rarely gets the credit it deserves. Thank you for reading carefully and taking each entry seriously, no matter how brief or ambitious. Knowing someone truly listened to what we put on the page means more than any ranking. I hope a few lines brought a real smile, and that you get a good rest once the final call is in.

With warmest thanks,
A grateful entrant"""


def main():
    if len(TEXT) != 623 or not 1 <= len(TEXT) <= 1000 or not TEXT.strip() or "\r" in TEXT:
        raise ValueError("Entry does not meet the text requirements")

    expected = (TEXT + "\n").encode("utf-8")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    entry = output_dir / "entry.txt"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output_dir, delete=False) as file:
            temporary = Path(file.name)
            file.write(expected)
        os.replace(temporary, entry)
        entry.chmod(0o644)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    if entry.read_bytes() != expected:
        raise IOError("Entry failed byte-for-byte verification")
    if stat.S_IMODE(entry.stat().st_mode) != 0o644:
        raise IOError("Entry permissions are not 0644")


if __name__ == "__main__":
    main()
