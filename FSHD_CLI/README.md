


# Haplotype Predictor

This Python script allows you to predict genotypes from Short Sequence Length Polymorphisms (SSLPs) values for Facioscapulohumeral muscular dystrophy (FSHD) analysis. It requires a selection of SSLPs and the region from where the sample is derived.
Requirements

    Python 3.x
    argparse library

## Script Description

The script uses pre-defined haplotypes for prediction. A haplotype is a group of genes within an organism that was inherited together from a single parent. This script uses haplotypes of certain populations (European, African, Asian) to predict the genotypes from the provided SSLP values.

You can also provide an optional input JSON file that contains the haplotypes. If no file is provided, the script uses default haplotypes.
Usage

shell

```bash
python haplotype_predictor.py -s <SSLP1 SSLP2 SSLP3 SSLP4> -p <population>
```
## Parameters
1.  **-h/--help**: Displays help message.
2.  **-s/--selection** (required): Integer values representing the SSLP selection. It must always be a length of 4 SSLP's. Example: `-s 159 161 163 166`.
3.  **-p/--population** (required): The region the sample is from. Choose from: African, Asian, European.
4.  **-H/--haplotypes**: Display the list of all possible haplotypes.
5.  **-n/--top**: Display top N results. If not specified, all results are displayed.
6.  **-a/--add**: Specify a json file containing haplotypes which will be added to the database.
7.  **-o/--output**: Specify the output file where the results will be written.
8.  **-sep/--separator**: Choose a separator for the output file. For a tab, enter 't'. Default is comma ','.

## Example

### shell

```bash
Python haplotype_predictor.py -s 159 161 163 166 -p European -n 10
```

This command will predict the genotypes for SSLP values 159 161 163 166 from the European region and display the top 10 results.
Output

The script outputs a table with the columns:
 - chr4_1
 - chr4_2
 - chr10_1
 - chr10_2
 - Probability(%)
 - Permutation
 - Incidence(%)

It also calculates and displays the Total Likelihood value at the end. If the -o/--output argument is used, the results will be written to the specified file instead of printing on the console.

If no results are found for the given selection and region, a relevant message is displayed.
Note

Make sure to use the correct SSLP values and region. Incorrect values can lead to unexpected results or errors.

