import pandas as pd, pathlib

def test_panel_has_core_columns():
    p = pathlib.Path("outputs")
    any_panel = sorted(p.glob("panel_*_2020-09-06_2020-09-12.parquet"))
    assert any_panel, "No pilot panel found"
    df = pd.read_parquet(any_panel[0])
    cols = set(["fips","date","pm25_mean","share_light","share_moderate","share_heavy",
                "cust_out_peak","cust_out_sum","total_customers","event_any"])
    assert cols.issubset(df.columns)
    assert len(df) > 0
