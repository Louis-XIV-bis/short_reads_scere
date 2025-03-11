# Variant calling in budding yeast

Author: Louis Ollivier

## Description

This project is an analysis pipeline using [Snakemake](https://snakemake.readthedocs.io/en/stable/) for variant calling.

The pipeline was developped for [SLURM](https://slurm.schedmd.com/documentation.html) based HPC cluster but can be run on any cluster infrastructure (or locally) if the parameters are changed accordingly.

The main steps of the pipeline are:
- alignment of reads on reference genome with [bwa](http://bio-bwa.sourceforge.net/) and processing of SAM/BAM files with [samtools](https://www.htslib.org/)  
- marking of duplicates with [gatk MarkDuplicatesSpark](https://gatk.broadinstitute.org/hc/en-us/articles/360037224932-MarkDuplicatesSpark)  
- computing the coverage with [bedtools genomecov](https://bedtools.readthedocs.io/en/latest/content/tools/genomecov.html)  
- variant calling with [gatk HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/360037225632-HaplotypeCaller)
- merging per strain gVCF to population VCF with [gatk GenomicsDBImport](https://gatk.broadinstitute.org/hc/en-us/articles/360036883491-GenomicsDBImport) & [gatk GenotypeGVCFs](https://gatk.broadinstitute.org/hc/en-us/articles/360037057852-GenotypeGVCFs)
- filtering sites based on scores with [gatk VariantFiltration](https://gatk.broadinstitute.org/hc/en-us/articles/360037434691-VariantFiltration) and [bcftools](https://samtools.github.io/bcftools/bcftools.html)
- removing repeated regions with [bedtools](https://bedtools.readthedocs.io/en/latest/)  

The pipeline works with **.fastq** files in the **data/** folder as input.

## System requirements

The only requirement is to be on a SLURM HPC cluster (recommended, but local running is possible, commands are also given for that case) and have a working install of [conda](https://www.anaconda.com/download/#linux) and [git](https://git-scm.com/downloads).
All tools necessary to run the pipeline are described in a conda environment file.  

The species specific resources files have to be downloaded manually if not *S. cerevisiae*. 

## Usage 
### Initialization
These commands have to be run only once to setup the pipeline.

#### Create the minimal snakemake environment to run jobs
```
conda env create -f workflow/envs/snakemake.yaml -n your_env_name
```

or load Snakemake version 7.32.4 the way you want (**module load** for instance)

#### If SLURM : create your profile 

In order to run the pipeline on SLURM cluster, you need to create a "profile" file contains information about the resources and other snakemake commands. The profile should be in the folllowing folder: $HOME/.config/snakemake/name_of_profile. You can name the profile the way you want but will need to use that name to run the pipeline. More information [here](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).  

Now, if you need to run the pipeline on a SLURM based cluster (recommended) or on a local computer, follow the according section.

The file used already exist in the **/workflow/profile/** directory. 


```
mkdir $HOME/.config/snakemake/name_of_profile
cp workflow/profile/config_slurm.yaml $HOME/.config/snakemake/name_of_profile/config.yaml
```

You can change the profile file according to your preferences. 


### Running the pipeline

In order to run the pipeline, you need to have **fastq.gz** files stored in a **data/** folder. the names of the fastq files will be used as ID througout the pipeline. For paired-end reads, make sure they are named by : *ID_1.fastq.gz* (and _2)   

Before running any command, make sure to have your conda environment activated, you can use: 
```
conda activate your_env_name 
```

Follow the correct section if you want to run the pipeline on a SLURM HPC cluster (recommended) or on a local computer.   

##### SLURM HPC cluster 

```
nohup snakemake --profile name_of_profile &
```

##### Local computer

```
nohup snakemake --resources mem_mb=64000 --cores 8 &
```

Note: you can change the values for the RAM ad the number of core. You can also create a profile to specify more resources but you'd need to change the script for each rule.

