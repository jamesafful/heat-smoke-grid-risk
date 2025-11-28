import subprocess, sys
def test_panel_schema_ok():
    r = subprocess.run(
        ["python","scripts/validate_panel.py","--panel","outputs/panel_3counties_2020-09-06_2020-09-12.parquet"],
        capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
