# Haplotype Predictor

This Python script allows you to predict genotypes from Short Sequence Length
 Polymorphisms (SSLPs) values for Facioscapulohumeral muscular dystrophy (FSHD)
 analysis. It requires a selection of SSLPs and the population to which the
 individual belongs, from which the sample is derived.

## Pip package

This analyser can also be used as a standalone pip package.
It can be installed by navigating to the `FSHD_CLI` directory
 and executing the following command in your environment of choice.

```bash
pip install .
```

The package can then be used as normal by substituting
 `python FSHD.py` with `FSHD`; for example:

```bash
FSHD -s <SSLP1 SSLP2 SSLP3 SSLP4> -p <population>
```

## Requirements

    Python 3.x
    - sys
    - json
    - shutil
    - argparse
    - pkg_resources
    - questionary
    - pathlib
    - itertools

## Description

The script uses pre-defined population-based probabilities for the association
 between haplotypes and SSLP fragment lengths for predictions.
A haplotype is a group of alleles within an organism that was inherited together
 from a single parent.
Currently supported populations are European, African, and Asian.
This script uses the given SSLP fragment lengths and the sample's population to
 predict the most likely haplotypes present in the given sample.

The script also allows you to add new haplotypes to the `haplotypes.json` data
 file, using the CLI interface.

## Usage

```bash
python FSHD.py -s <SSLP1 SSLP2 SSLP3 SSLP4> -p <population>
```

### Parameters

- **-h/--help**:
  Displays help message.
- **-s/--selection** (required):
  Integer values representing the SSLP selection.
  It must always be a length of 4 SSLP's.
  Example: `-s 159 161 163 166`.
- **-p/--population** (required):
  The region the sample is from.
  Choose from: African, Asian, European.
- **-H/--haplotypes**:
  Display the list of all possible haplotypes.
- **-n/--top**:
  Display top N results.
  If not specified, all results are displayed.
- **-a/--add**:
  Specify a json file containing haplotypes which will be added to the database.
- **-o/--output**:
  Specify the output file where the results will be written.
- **-sep/--separator**:
  Choose a separator for the output file.
  For a tab, enter `t`.
  Default is comma (`,`).

### Valid combinations

- **-l, --list_datasets and -s, --selection**:
  This combination allows you to display all datasets available 
   for a given SSLP selection.
  Example usage: -l -s 159 161 163 166.
- **-s, --selection and -p, --population**:
  Use this to run the genotype predictor on the given
   SSLP values for a specific population.
  Example usage: -s 159 161 163 166 -p Asian.
- **-H, --haplotypes and -p, --population**:
  This combination displays all possible haplotypes for a given population.
  Example usage: -H -p Asian.
- **-H, --haplotypes and -l, --list_datasets**:
  Use this combination to display all possible haplotypes and 
   the list of all populations that have a haplotype dataset.
  Example usage: -H -l.
- **-A, --add**:
  Use this argument independently to add new haplotype files to the database.
  Example usage: -A ./new_haplotypes.json.

### Example

```bash
python FSHD.py -s 159 161 163 166 -p European -n 10
```

This command will predict the genotypes for SSLP values 159 161 163 166
 in the European population and display the top 10 results.

## Output

The script outputs a table with the columns:
- chr4_1
- chr4_2
- chr10_1
- chr10_2
- Probability(%)
- Permissive
- Incidence(%)

It also calculates and displays the total Likelihood value at the end.
If the `-o`/`--output` argument is used, the results will be written
 to the specified file instead of printing on the console.

If no results are found for the given selection and population,
 a relevant message is displayed.

## Note

Make sure to use the correct SSLP values and population.
Incorrect values can lead to unexpected results or errors.
