"""
Runs a performance test against different cross_matcher algorithms by
invoking them with different catalogue sizes, recording the execution
time and plotting execution time.
"""
import argparse
import sys
import matplotlib.pyplot as plt
from src.my_time import time_it
from src.astro import cross_matcher, kd_tree
import src.utils.utils as utils

if __name__ == "__main__":

    print("[INFO] Script started successfully")

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-b",
        "--bss_path",
        type=str,
        default="./cats/bss.dat",
        help="file path to bss catalogue data",
    )
    ap.add_argument(
        "-s",
        "--super_path",
        type=str,
        default="./cats/super.csv",
        help="file path to SuperCosmos catalogue data",
    )
    ap.add_argument(
        "-o",
        "--output_path",
        type=str,
        default="./figs/output.png",
        help="file path to output figure",
    )
    args = vars(ap.parse_args())

    try:
        cats = {
            "bss_cat": utils.import_dat(args.get("bss_path")),
            "super_cat": utils.import_csv(args.get("super_path")),
        }
    except FileNotFoundError:
        print("[ERR] Catalogues not found at filepath.")
        sys.exit()

    print("[INFO] Loaded catalogue data")
    print("[INFO] Starting timing comparison")

    # Time each method for different number of elements in catalogues
    naive_cross_matcher_times = time_it.time_method(
        cross_matcher.naive_crossmatch, **cats
    )
    numpy_cross_matcher_times = time_it.time_method(
        cross_matcher.numpy_crossmatch, **cats
    )
    kd_cross_matcher_times = time_it.time_method(kd_tree.KD_crossmatch, **cats)

    print("[INFO] Plotting results")

    # Plot the results
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    labels = naive_cross_matcher_times.keys()
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Size of each catalogue")
    ax.set_ylabel("Best time [ms]")

    ax.bar(
        range(len(labels)),
        naive_cross_matcher_times.values(),
        color="green",
        alpha=0.4,
        label="Naive",
    )
    ax.bar(
        range(len(labels)),
        numpy_cross_matcher_times.values(),
        color="red",
        alpha=0.4,
        label="Numpy",
    )
    ax.bar(
        range(len(labels)),
        # Multiply kd tree times up by a factor of 100 so we can actually see them on the graph!
        {k: v * 100 for k, v in kd_cross_matcher_times.items()}.values(),
        color="blue",
        alpha=0.4,
        label="KD Tree * 100",
    )

    plt.legend()

    out_path = args.get("output_path")
    print(f"[INFO] Saving figure to {out_path}")
    plt.savefig(out_path)
