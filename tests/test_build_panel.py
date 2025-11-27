from src.hsg.etl.build_panel_stdlib import build_sample_panel
from src.hsg.data_paths import OUTPUTS

def test_build_sample_panel():
    stats = build_sample_panel()
    assert stats["pm25_rows"] > 0
    assert stats["smoke_rows"] > 0
    assert stats["outage_rows"] > 0
    assert (OUTPUTS / "pm25_sample.csv").exists()
    assert (OUTPUTS / "hms_smoke_sample.csv").exists()
    assert (OUTPUTS / "outages_sample.csv").exists()
