from pathlib import Path
from typing import Final

root: Final = Path(__file__).resolve().parents[2]
c_source: Final = root / "src" / "c"
build: Final = root / "build"
data: Final = root / "data"
plots: Final = root / "plots"
