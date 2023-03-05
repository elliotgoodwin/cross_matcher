"""
Implements and compares the results of different cross matching algorithms.
"""
import os
import sys
import argparse
import time
import numpy as np
import src.utils.utils as utils
from src.astro import cross_matcher, kd_tree


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
        "-d",
        "--max_dist",
        type=float,
        default=40 / 3600,
        help="max distance between catalogue objects to consider a match",
    )
    args = vars(ap.parse_args())

    if not os.path.exists(args.get("bss_path")) or not os.path.exists(
        args.get("super_path")
    ):
        print("[ERR] Cannot find catalogue directories.")
        sys.exit()

    bss_cat = utils.import_dat(args.get("bss_path"))
    super_cat = utils.import_csv(args.get("super_path"))

    print("[INFO] Loaded catalogue data")
    print("[INFO] Start cross matching")

    naive_start_time = time.perf_counter()
    matches, no_matches = cross_matcher.naive_crossmatch(
        bss_cat, super_cat, args.get("max_dist")
    )
    naive_end_time = time.perf_counter()
    print(
        f"[INFO] Naive method found {len(matches)} matches and "
        f"{len(no_matches)} objects with no match"
    )
    print(f"[INFO] Naive method took {naive_end_time-naive_start_time} seconds")

    numpy_start_time = time.perf_counter()
    matches, no_matches = cross_matcher.numpy_crossmatch(
        bss_cat, super_cat, args.get("max_dist")
    )
    numpy_end_time = time.perf_counter()
    print(
        f"[INFO] Numpy method found {len(matches)} matches and "
        f"{len(no_matches)} objects with no match"
    )
    print(f"[INFO] Numpy method took {numpy_end_time-numpy_start_time} seconds")

    kd_start_time = time.perf_counter()
    bss_cat = np.radians(np.asarray(bss_cat))
    super_cat = np.radians(np.asarray(super_cat))
    match_indexes = kd_tree.KD_crossmatch(bss_cat, super_cat, args.get("max_dist"))

    matches, no_matches = kd_tree.process_KD_crossmatch(
        match_indexes, bss_cat, super_cat
    )
    kd_end_time = time.perf_counter()
    print(
        f"[INFO] k-d tree method found {len(matches)} matches and "
        f"{len(no_matches)} objects with no match"
    )
    print(f"[INFO] k-d tree method took {kd_end_time-kd_start_time} seconds")
