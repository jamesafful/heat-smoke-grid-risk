from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
DATA_SAMPLE = DATA / "sample"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True, parents=True)
