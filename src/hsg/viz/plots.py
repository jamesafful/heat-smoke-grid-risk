import argparse
import pandas as pd
import matplotlib.pyplot as plt
from ..data_paths import OUTPUTS

def demo_plot():
    pm = pd.read_parquet(OUTPUTS / "pm25_sample.parquet")
    pm = pm.sort_values("date")
    plt.figure()
    plt.plot(pm["date"], pm["arithmetic_mean"], marker="o")
    plt.title("Cook County PM2.5 (sample)")
    plt.xlabel("Date")
    plt.ylabel("PM2.5 (ug/m3)")
    plt.tight_layout()
    outpath = OUTPUTS / "pm25_demo.png"
    plt.savefig(outpath)
    print(f"saved {outpath}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()
    if args.sample:
        demo_plot()

if __name__ == "__main__":
    main()
