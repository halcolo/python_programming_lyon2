import sys

def print_progress_bar(index, total, label):
    """
    Print a progress bar to the console.
    
    Parameters:
        index (int): The current index.
        total (int): The total number of iterations.
        label (str): The label to display.
    """
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()