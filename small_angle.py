import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import src.utils.utils as utils

if __name__ == "__main__":

    print("[INFO] Script started successfully")

    max_dist = 40/3600
    
    bss_path = './cats/bss.dat'
    super_path = './cats/super.csv'

    if not os.path.exists(bss_path) or not os.path.exists(super_path):
        print("[ERR] Cannot find catalogue directories.")
        sys.exit()

    bss_cat = utils.import_dat(bss_path)
    super_cat = utils.import_csv(super_path)

    print("[INFO] Loaded catalogue data")


    ## ----------------------------------------------------------------------
    ## ----------- Test small angle approx ----------------------------------
    ## ----------------------------------------------------------------------

    bss_cat = np.radians(bss_cat)

    print('[INFO] Summary of difference in distance between true value and small angle approx:\n')
    print('\tidx \t angular sep. \t\t small angle \t\t euclidean dist. \t diff')
    trues = np.zeros(len(bss_cat)-1)
    smalls = np.zeros(len(bss_cat)-1)
    euclids = np.zeros(len(bss_cat)-1)
    diffs = np.zeros(len(bss_cat)-1)

    diff_idxs = []
    for idx, coords in enumerate(bss_cat[:-1]):
        r1, d1 = coords
        r2, d2 = bss_cat[idx+1]

        # Find the true angular separation in degrees using Haversine formula
        true = utils.angular_dist(r1, d1, r2, d2, radians=True)
        trues[idx] = true
        
        # Find the approximate angular separation in degrees by applying the
        # small angle approximation to the Haversine formula
        small = utils.angular_dist(r1, d1, r2, d2, small=True)
        smalls[idx] = small

        # Find the euclidean distance
        euclid = np.sqrt( np.abs(r2-r1)**2 + np.abs(d2-d1)**2 )
        euclid = np.degrees(euclid)
        euclids[idx] = euclid

        # Show any values where the difference between the true angular separation
        # and euclidean distance isn't ~ 0.
        diffs[idx] = true-euclid
        if (np.round(diffs[idx]) != 0):
            diff_idxs.append(idx)
            print(f'\t{idx} \t {true} \t {small} \t {euclid} \t {diffs[idx]}')

    idx = np.argmax(trues)
    print(f'\t{idx} \t {trues[idx]} \t {smalls[idx]} \t {euclids[idx]} \t {diffs[idx]}')

    
    print(f'\n[INFO] Max true is {np.max(trues)} at index {np.argmax(trues)}')
    print(f'[INFO] Mean diff {np.asarray(diffs).mean()}')
    
    # Plot the results
    print('[INFO] Plotting comparison...')
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.set_xlabel("Catalogue object index")
    ax.set_ylabel("Computed distance")

    xs = np.linspace(0, len(bss_cat)-2, len(bss_cat)-1)

    ax.plot(
        xs,
        trues,
        color="green",
        alpha=0.4,
        label="True",
    )
    ax.plot(
        xs,
        smalls,
        color="blue",
        linestyle='--',
        alpha=0.4,
        label="Small angle",
    )
    ax.plot(
        xs,
        euclids,
        color="red",
        linestyle='--',
        alpha=0.4,
        label="Euclidean",
    )
    
    # Plot range where we saw differences
    plt.xlim([diff_idxs[0]-5, diff_idxs[1]+5])

    plt.legend()
    out_path = './figs/small_angle_approx.png'
    print(f"[INFO] Saving figure to {out_path}")
    plt.savefig(out_path)
    
    print("[INFO] Done")