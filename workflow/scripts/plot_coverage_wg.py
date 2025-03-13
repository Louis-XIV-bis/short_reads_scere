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
    and plot the genome-wide coverage distribution for each sample.
    """
    if len(sys.argv) != 3:
        print("Usage: python plot_genomewide_coverage.py <input_file> <sample_name>")
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

    # Compute coverage for each chromosome
    genome_coverage = []
    chromosome_labels = []
    for chrom in chromosomes:
        chrom_data = data[data['chromosome'] == chrom]
        coverage = compute_coverage(chrom_data['coverage'].values)
        genome_coverage.extend(coverage)
        chromosome_labels.extend([chrom] * len(coverage))

    # Plot genome-wide coverage distribution
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(genome_coverage, label='Coverage')
    ax.set_title(f'Genome-wide Coverage Distribution - {sample_name}')
    ax.set_xlabel('Genome Position (1kb windows)')
    ax.set_ylabel('Coverage')
    ax.set_ylim(0, 300)  # Set y-axis limits

    # Add vertical lines and text labels to separate chromosomes
    chrom_positions = [i for i, x in enumerate(chromosome_labels[:-1]) if x != chromosome_labels[i + 1]]
    for pos in chrom_positions:
        ax.axvline(x=pos, color='grey', linestyle='--', linewidth=0.5)
    
    # Add chromosome names on top
    for i, chrom in enumerate(chromosomes):
        if i == 0:
            start_pos = 0
        else:
            start_pos = chrom_positions[i-1] + 1
        end_pos = chrom_positions[i] if i < len(chrom_positions) else len(genome_coverage) - 1
        mid_pos = (start_pos + end_pos) // 2
        chrom_label = chr_names.get(chrom, chrom)  # Replace chromosome name using the dictionary
        ax.text(mid_pos, 285, chrom_label, ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'coverage_gw_{sample_name}.png')
    plt.show()

if __name__ == "__main__":
    main()