import sys
import time


def time_func(func, *args):
    """
    Wrapper to time a function with time.perf_counter()

    Args:
        func (function): The name of the function being timed
        args (tuple): Arguments to pass to func

    Returns:
        (float): Time taken to execute the function
    """
    t0 = time.perf_counter()
    func(*args)
    return time.perf_counter() - t0


def time_method(func, **cats):
    """
    Performance tests a given function by timing the function for
    varying input data sizes.

    Args:
        func (function): The method to performance test
        cats (dict): Kwargs to pass to funcfunc

    Returns:
        dict(int: float): Dictionary where keys are the number of
                          elements in each input catalogue and values
                          are the time taken to execute the function
                          for the corresponding catalogues
    """
    max_dist = 40 / 3600

    bss_cat = cats.get("bss_cat")
    super_cat = cats.get("super_cat")

    if not (bss_cat or super_cat):
        print("[ERR] There is an issue with the imported catalogues.")
        sys.exit()

    # Time function for different input data sizes (given by the key)
    data = {
        50: time_func(func, bss_cat[:50], super_cat[:50], max_dist),
        100: time_func(func, bss_cat[:100], super_cat[:100], max_dist),
        150: time_func(func, bss_cat[:150], super_cat[:150], max_dist),
        200: time_func(func, bss_cat[:200], super_cat[:200], max_dist),
        250: time_func(func, bss_cat[:250], super_cat[:250], max_dist),
        300: time_func(func, bss_cat[:300], super_cat[:300], max_dist),
    }
    return data
