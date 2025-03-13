import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def compute_coverage(data, window_size=1000):
    """
    Compute the average coverage for 1kb windows.

    Parameters:
    data (numpy array): Array of coverage values.
    window_size (int): Size of the window in base pairs.

    Returns:
    list: List of average coverage values for each window.
    """
    coverage = []
    for i in range(0, len(data), window_size):
        window = data[i:i+window_size]
        coverage.append(np.mean(window))
    return coverage

def main():
    """
    Main function to read coverage data, compute coverage for 1kb windows,
    and plot the coverage for each chromosome.
    """
    if len(sys.argv) != 3:
        print("Usage: python plot_coverage.py <input_file> <sample_name>")
        sys.exit(1)

    input_file = sys.argv[1]
    sample_name = sys.argv[2]

    # Dictionary to replace chromosome names
    chr_names = {
        'ref|NC_001133|': 'chr1',
        'ref|NC_001134|': 'chr2',
        'ref|NC_001135|': 'chr3',
        'ref|NC_001136|': 'chr4',
        'ref|NC_001137|': 'chr5',
        'ref|NC_001138|': 'chr6',
        'ref|NC_001139|': 'chr7',
        'ref|NC_001140|': 'chr8',
        'ref|NC_001141|': 'chr9',
        'ref|NC_001142|': 'chr10',
        'ref|NC_001143|': 'chr11',
        'ref|NC_001144|': 'chr12',
        'ref|NC_001145|': 'chr13',
        'ref|NC_001146|': 'chr14',
        'ref|NC_001147|': 'chr15',
        'ref|NC_001148|': 'chr16',
        'ref|NC_001224|': 'chr_mt',
    }

    # Read the per position coverage data
    data = pd.read_csv(input_file, sep='\t', header=None, names=['chromosome', 'position', 'coverage'])

    # Get unique chromosomes
    chromosomes = data['chromosome'].unique()

    # Plot coverage for each chromosome
    fig, axes = plt.subplots(len(chromosomes), 1, figsize=(10, 5 * len(chromosomes)))

    for i, chrom in enumerate(chromosomes):
        chrom_data = data[data['chromosome'] == chrom]
        coverage = compute_coverage(chrom_data['coverage'].values)
        
        chrom_label = chr_names.get(chrom, chrom)  # Replace chromosome name using the dictionary
        axes[i].plot(coverage)
        axes[i].set_title(f'Chromosome {chrom_label} - {sample_name}')
        axes[i].set_xlabel('1kb Window')
        axes[i].set_ylabel('Coverage')
        axes[i].set_ylim(0, 300)  # Set y-axis limits

    plt.tight_layout()
    plt.savefig(f'coverage_chr_{sample_name}.png')
    plt.show()

if __name__ == "__main__":
    main()