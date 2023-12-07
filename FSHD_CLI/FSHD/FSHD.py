import sys
import json
import shutil
import argparse
import pkg_resources
import questionary
from questionary import Style,confirm
from pathlib import Path
from itertools import product
from argparse import RawTextHelpFormatter

custom_style = Style([
    ('separator', 'fg:#6C6C6C'),
    ('qmark', 'fg:#FF9D00 bold'),  # question mark at the start of the prompt
    ('question', 'fg:#9ad4f5'),  # question text
    ('selected', 'fg:#5F819D'),  # for the selected item
    ('pointer', 'fg:#fff bold'),  # pointer used in select and checkbox prompts
    ('answer', 'fg:#fe2e2e bold'),  # for answer
    ('highlighted', 'fg:#a6e0ff bold'),
])



def get_haplotypes():
    """Loads in haplotypes.json as python dictonary

    :return: .json file as dictonary
    """
    with open(pkg_resources.resource_filename(__name__, "haplotypes.json"), "r") as file:
        haplo_dict = json.load(file)
    return haplo_dict


def predict(args):
    """
    Prediction function (Algorithm written by Jan Oliehoek)
    Does the statistical calculations which detirmine the percentages
    haplotypes = [[EU4, EU10], [AF4, AF10], [AS4, AS10]]
    """
    if args.list_datasets:
        haplotypes = get_haplotypes()[args.population]
    else:
        haplotypes = get_haplotypes()[args.population]

    reeksvier, reekstien, kansenreeks = [], [], []
    totaalkans = 0
    for nr in set(args.selection):
        nr = str(nr)
        for chr in haplotypes:
            try:
                if chr == "chr4":
                    reeksvier += haplotypes[chr][nr]
                elif chr == "chr10":
                    reekstien += haplotypes[chr][nr]
            except LookupError as e:
                pass

    # -> alle mogelijkheden genereren
    for i, j, k, l in product(reeksvier, reeksvier, reekstien, reekstien):
        nummers = [int(i["haplotype"][1:4]), int(j["haplotype"][1:4]), int(
            k["haplotype"][1:4]), int(l["haplotype"][1:4])]
        # checken of ze wel uniek zijn (of de nummers kloppen met het voorbeeld)
        if sorted(nummers) == args.selection:
            kans = (float(i["%"]) * float(j["%"]) *
                    float(k["%"]) * float(l["%"]))/1000000
            berekening = i["%"] + ' * ' + j["%"] + \
                ' * ' + k["%"] + ' * ' + l["%"]
            genotype = ['4' + i["haplotype"], '4' + j["haplotype"],
                        '10' + k["haplotype"], '10' + l["haplotype"]]
            p = int(i["permissive"]) + int(j["permissive"]) + \
                int(k["permissive"]) + int(l["permissive"])
            kansenreeks.append([kans, genotype, berekening, p])
            totaalkans += kans
    # -> einde alle mogelijkheden genereren
    gesorteerd = sorted(kansenreeks, key=lambda x: x[0], reverse=True)
    # -> identieke genotypes bij elkaar optellen
    ingeklapt = []
    teller = 1
    try:
        checker = gesorteerd[0]
    except:
        return 1, 1
    for i in range(1, len(gesorteerd)):
        if gesorteerd[i][0] - checker[0] < 0.000001 and sorted(gesorteerd[i][1]) == sorted(checker[1]):
            teller += 1
        else:
            ingeklapt.append([gesorteerd[i-teller][0]*teller,
                             gesorteerd[i-teller][1], gesorteerd[i-teller][3]])
            teller = 1
            checker = gesorteerd[i]
    ingeklapt.append([gesorteerd[i][0]*teller, gesorteerd[i]
                     [1], gesorteerd[i-teller][3]])
    # -> einde identieke genotypes bij elkaar optellen

    ingeklapt = sorted(ingeklapt, key=lambda x: x[0], reverse=True)

    return ingeklapt, totaalkans


def validate_combinations(args):
    """
    Function to check if there is a valid combination of arguments given by the user.

    Args:
        args: (argparse.Namespace): namespace with all the arguments given by the user from the command line.

    Returns:
        bool: boolean to indicate of there is a valid combination of arguments.
        True if there is a valid combination of arguments. False if there is there are no combinations found.
    """
    valid_combinations = [
        args.list_datasets and args.selection,
        args.selection and args.population,
        args.haplotypes and args.population,
        args.haplotypes and args.list_datasets,
        args.add
    ]
    return not any(valid_combinations)


def to_population(new_file):
    """Adds a new population to the haplotypes.json file. 
    Prompts the users if a population is already present.

    :param new_file: _description_
    """
    with open(pkg_resources.resource_filename(__name__, new_file), "r") as file:
        new_haplo_dict = json.load(file)
    reconstructed_haplotypes = get_haplotypes()
    
    for population, haplotype in new_haplo_dict.items():
        if population in reconstructed_haplotypes:
            response = confirm(f"The population {population} is already present. Do you wish to overwrite it?",
                               style=custom_style,
                               qmark="").ask()
            if response:
                reconstructed_haplotypes[population] = haplotype
        else:
            print(population)
            reconstructed_haplotypes[population] = haplotype
            

    with open(pkg_resources.resource_filename(__name__, "haplotypes.json"), "w") as file:
        file.write(json.dumps(reconstructed_haplotypes,indent=4))
    
    


def print_table(row):
    """Prints the table to the standard output

    :param row: the row that needs printing
    """
    print(
        f"{row[0]:<10}{row[1]:<10}{row[2]:<10}{row[3]:<10}{row[4]:<15}{row[5]:<15}{row[6]:<15}")


def write_table(row, separator, filename):
    """Saves table to file
    Saves table in append mode
    :param row: row specified
    :param separator: character to use as seperator
    :param filename: name of file
    """
    with open(filename, 'a') as outfile:
        outfile.write(f"{separator.join(row)}\n")


def print_header():
    """Print the header of the table to the standard output
    
    """
    print(f"{'chr4_1':<10}{'chr4_1':<10}{'chr10_1':<10}{'chr10_2':<10}{'Probability(%)':<15}{'Permissive':<15}{'Incidence(%)':<15}")


def result_table(result, totaalkans, amount, separator, write=False, filename=None):
    """_summary_
    Format the results into a neatly formatted table. 
    :param result: _description_
    :param totaalkans: _description_
    :param amount: _description_
    :param separator: _description_
    :param write: _description_, defaults to False
    :param filename: _description_, defaults to None
    """
    if write:
        header = ['chr4_1', 'chr4_1', 'chr10_1', 'chr10_2',
                  'Probability(%)', 'Permissive', 'Incidence(%)']
        with open(filename, 'w') as outfile:
            outfile.write(f"{separator.join(header)}\n")
    else:
        print_header()
    for i in result[:amount]:
        values = [str(val) for val in i[1]]
        percentage = 100 * i[0] / totaalkans
        probability = i[0]
        row = values + [f"{percentage:.3f}", str(i[2]), f"{probability:.3f}"]
        if write:
            write_table(row, separator, filename)
        else:
            print_table(row)


def haplo(args):
    """haplo
    Gets all the unique SSLP values from the supplied population.
    :param args: argparser documentation
    :return: Unique comma seperated string of unique haplotypes
    """
    haplotypes = get_haplotypes()
    haplotype_nums = list(
        haplotypes[args.population]["chr4"].keys()) + list(haplotypes[args.population]["chr10"])
    unique_haplotypes = sorted(list(set(haplotype_nums)))
    return (", ".join(unique_haplotypes))


def other_options(args):
    """Function which allows the datasets to be selected using questonary. 
    Furthermore adds the support for printing the haplotypes for a specific population.
    Also calls the to_population() method if the users wishes to add haplotypes to the database\
    :param args: argparse object 
    """
    if args.list_datasets:
        selected_dataset = questionary.select(
            "Select a dataset",
            choices=get_haplotypes().keys(),
            style=custom_style,
            pointer="❯",
            use_jk_keys=True,
            show_selected=True,
            qmark=""
        ).ask()
        args.population = selected_dataset
        
    if args.haplotypes and args.population:
        haplotype_options = haplo(args)
        print(f"List of all possible haplotypes: {haplotype_options}.", end="")
        sys.exit()
    if args.add:
        to_population(args.add)
        sys.exit()


def parser_args():
    """
    Function with all the arguments that are necessary to use the FSHD commandline tool.

    Returns:
        args: argparser.namespace: Parsed command-line arguments.
        parser: ArgumentParser: The ArgumentParser instance for the tool.
_
    """
    a = """

                                                                       ,--,            
                              ,--,                                  ,---.'|            
    ,---,.  .--.--.         ,--.'|    ,---,                ,----..  |   | :      ,---, 
  ,'  .' | /  /    '.    ,--,  | :  .'  .' `\             /   /   \ :   : |   ,`--.' | 
,---.'   ||  :  /`. / ,---.'|  : ',---.'     \     ,---,.|   :     :|   ' :   |   :  : 
|   |   .';  |  |--`  |   | : _' ||   |  .`\  |  ,'  .' |.   |  ;. /;   ; '   :   |  ' 
:   :  :  |  :  ;_    :   : |.'  |:   : |  '  |,---.'   ,.   ; /--` '   | |__ |   :  | 
:   |  |-, \  \    `. |   ' '  ; :|   ' '  ;  :|   |    |;   | ;    |   | :.'|'   '  ; 
|   :  ;/|  `----.   \'   |  .'. |'   | ;  .  |:   :  .' |   : |    '   :    ;|   |  | 
|   |   .'  __ \  \  ||   | :  | '|   | :  |  ':   |.'   .   | '___ |   |  ./ '   :  ; 
'   :  '   /  /`--'  /'   : |  : ;'   : | /  ; `---'     '   ; : .'|;   : ;   |   |  ' 
|   |  |  '--'.     / |   | '  ,/ |   | '` ,/            '   | '/  :|   ,/    '   :  | 
|   :  \    `--'---'  ;   : ;--'  ;   :  .'              |   :    / '---'     ;   |.'  
|   | ,'              |   ,/      |   ,.'                 \   \ .'            '---'    
`----'                '---'       '---'                    `---`                       
                                                                                       

"""
    parser = argparse.ArgumentParser(
        description=f"{a}\nA tool for predicting genotypes from SSLP values for FSHD analysis. This tool allows users to input specific SSLP selections, specify the population of the patient, and also provides the ability to add new haplotype files.", formatter_class=RawTextHelpFormatter)
    group1 = parser.add_argument_group('required arguments')
    group1.add_argument("-s", "--selection", nargs="+", type=int, required=False, metavar="SSLP",
                        help="Provide a list of four integer SSLP values. Example usage: -s 159 161 163 166.")
    group1.add_argument("-p", "--population", choices=get_haplotypes().keys(), required=False, metavar="POPULATION",
                        help="Specify the population of the patient.")
    group2 = parser.add_argument_group('optional arguments')
    group2.add_argument("-H", "--haplotypes",  action="store_true",
                        help="Use this flag to display a list of all possible haplotypes.")
    group2.add_argument("-n", "--top", type=int, metavar="N",
                        help="Use this option to only display the top N results.\nIf not specified, all results are displayed.")
    group2.add_argument("-A", "--add", type=str, metavar="INPUT FILE",
                        help="Use this argument independently to add new haplotype files to the database. Example usage: -A ./new_haplotypes.json.")
    group2.add_argument("-o", "--output", type=str, metavar="OUTPUT FILE",
                        help="Specify the path to an output file where the results will be written.\nIf not specified, results will be printed to the console.")
    group2.add_argument("--separator", type=str, choices=[",", "t", "|", ";", " "], default=",", metavar="SEPARATOR",
                        help="Choose a separator for the output file.\nOptions include comma (,), tab (t), pipe (|), semicolon (;), or space ( ). Default is comma ','.")
    group2.add_argument("-l", "--list_datasets", action="store_true",
                        help="Shows a list of all populations which have a haplotype dataset")

    args = parser.parse_args()
    return args, parser


def run(args):
    """Function which calls the predict method after parsing of arguments
    :param args: _description_
    """
    args.selection = sorted(args.selection)
    separator = {'t': '\t', ',': ',', '|': '|',
                 ';': ';', ' ': ' '}.get(args.separator)
    result, totaalkans = predict(args)
    if result != 1 and totaalkans != 1:
        tot_perm = [100*i[0]/totaalkans for i in result if i[2] > 0]
        output = args.output is not None
        filename = args.output if output else None
        if args.top:
            result_table(result, totaalkans, args.top,
                         separator, output, filename)
        else:
            result_table(result, totaalkans, len(
                result), separator, output, filename)
        if output:
            with open(args.output, 'a') as output_file:
                output_file.write(f"Total Likelihood: {sum(tot_perm):.1f}")
        else:
            print(f"Total Likelihood: {sum(tot_perm):.1f}")
    else:
        print(f"No results found for this selection {' '.join(str(i) for i in args.selection)} for population {args.population}!\n"
              f"For more information use the -h flag.")


def main():
    args, parser = parser_args()
    if args.selection and len(args.selection) != 4:
        parser.error(
            f"You must have a input of 4 SSLP's. The length of your input is {len(args.selection)} SSLP's.")
    if validate_combinations(args):
        parser.error("Invalid combination of arguments. You must provide one of the following combinations:\n"
                     "-s/--selection and -p/--population\n"
                     "-s/--selection and -l/--list_datasets\n"
                     "-s/--selection, -p/--population, and -n/--top\n"
                     "-H/--haplotypes and -p/--population\n"
                     "-H/--haplotypes and -l/--list_datasets\n"
        )
    other_options(args)
    run(args)


if __name__ == "__main__":
    main()
