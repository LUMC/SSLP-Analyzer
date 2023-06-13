import sys
import json
import shutil
import argparse
import pkg_resources
import questionary
from questionary import Style
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

def get_abbrivations():
    """Fetches the abbrivations from abbrivations.json
    Returns this data as different objects
    :return: 
    abbr_dict: dict: Dictonary which maps abbriviations to full names
    options: list: List which contains all abrivations and full names
    option_string: str: String which says what abbrivations are possible and what they stand
    """
    with open(pkg_resources.resource_filename(__name__, "abbreviations.json"), "r") as file:
        abbr_dict = json.load(file)
        options = list(abbr_dict.keys()) + list(abbr_dict.values())
        option_string = ""
        for k, v in abbr_dict.items():
            option_string += f"{k} ({v}) "
        return abbr_dict, options, option_string


def get_ethnicity(ethnicity):
    """Fetches the ethnicity data from the supplied 
    ethnicity. And returns this as a dcitonary.
    :param ethnicity: Full ethnicity name
    :return: haplotype dictonary for specified ethnicity
    """
    with open(pkg_resources.resource_filename(__name__, f"ethnicity/{ethnicity}.json"), "r") as file:
        haplo_dict = json.load(file)
        print(f"Using haplotypes from file: ethnicity/{ethnicity}.json")
    return haplo_dict

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
        args.abbriviations,
        args.list_datasets and args.selection, 
        args.selection and args.ethnicity, 
        args.haplotypes and args.ethnicity,
        args.selection and args.input,
        args.add and args.input and args.file_abbreviation,
    ]
    return not any(valid_combinations)
    

def to_ethnicity(new_file):
    """
    Function to copy a new "ethnicity.json" file to the "ethnicity" directory in current package.

    Args:
        new_file (str): A string representing the file path of the given json file.
    """
    source = Path(new_file)
    destination_dir = Path(pkg_resources.resource_filename(__name__, "ethnicity"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source), destination_dir)

def print_table(row):
    print(f"{row[0]:<10}{row[1]:<10}{row[2]:<10}{row[3]:<10}{row[4]:<15}{row[5]:<15}{row[6]:<15}")


def write_table(row, separator, filename):
    with open(filename, 'a') as outfile:
        outfile.write(f"{separator.join(row)}\n")

def print_header():
    print(f"{'chr4_A':<10}{'chr4_B':<10}{'chr10_A':<10}{'chr10_B':<10}{'Probability(%)':<15}{'Permutation':<15}{'Incidence(%)':<15}")

def result_table(result, totaalkans, amount, separator, write=False, filename=None):
    """_summary_

    :param result: _description_
    :param totaalkans: _description_
    :param amount: _description_
    :param separator: _description_
    :param write: _description_, defaults to False
    :param filename: _description_, defaults to None
    """
    if write:
        header = ['chr4_A', 'chr4_B', 'chr10_A', 'chr10_B', 'Probability(%)', 'Permutation', 'Incidence(%)']
        with open(filename, 'w') as outfile:
            outfile.write(f"{separator.join(header)}\n" )
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
    with open(pkg_resources.resource_filename(__name__, f"ethnicity/{args.ethnicity}.json"), "r") as filename:
        haplotypes = json.load(filename)
    haplotype_nums = list(haplotypes["chr4"].keys()) + list(haplotypes["chr10"])
    unique_haplotypes = sorted(list(set(haplotype_nums)))
    return (", ".join(unique_haplotypes))


def predict(args):
    """
    haplotypes = [[EU4, EU10], [AF4, AF10], [AS4, AS10]]
    """
    if args.input:
        with open(args.input, 'r') as f:
            ethnicity_haplotypes = json.load(f)
    elif args.hidden_dataset is not None:
        ethnicity_haplotypes = args.hidden_dataset
    else:
        ethnicity_haplotypes = get_ethnicity(args.ethnicity)
    
    reeksvier, reekstien, kansenreeks = [],[],[]
    totaalkans = 0
    for nr in set(args.selection):
        nr = str(nr)
        for chr in ethnicity_haplotypes:
            try:
                if chr == "chr4":
                    reeksvier += ethnicity_haplotypes[chr][nr]
                elif chr == "chr10":
                    reekstien += ethnicity_haplotypes[chr][nr]
            except LookupError as e:
                pass

    #-> alle mogelijkheden genereren
    for i,j,k,l in product(reeksvier, reeksvier, reekstien, reekstien):
        nummers = [int(i["haplotype"][1:4]), int(j["haplotype"][1:4]), int(k["haplotype"][1:4]), int(l["haplotype"][1:4])]
        if sorted(nummers) == args.selection: #checken of ze wel uniek zijn (of de nummers kloppen met het voorbeeld)                   
            kans = (float(i["%"]) * float(j["%"]) * float(k["%"]) * float(l["%"]))/1000000
            berekening = i["%"] + ' * ' + j["%"] + ' * ' + k["%"] + ' * ' + l["%"] 
            genotype = ['4' + i["haplotype"], '4' + j["haplotype"], '10' + k["haplotype"], '10' + l["haplotype"]]
            p = int(i["permissive"]) + int(j["permissive"]) + int(k["permissive"]) + int(l["permissive"]) 
            kansenreeks.append([kans, genotype, berekening, p])
            totaalkans += kans
    #-> einde alle mogelijkheden genereren
    gesorteerd = sorted(kansenreeks, key = lambda x:x[0], reverse=True)
    #-> identieke genotypes bij elkaar optellen
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
            ingeklapt.append([gesorteerd[i-teller][0]*teller, gesorteerd[i-teller][1], gesorteerd[i-teller][3]])
            teller = 1
            checker = gesorteerd[i]
    ingeklapt.append([gesorteerd[i][0]*teller, gesorteerd[i][1], gesorteerd[i-teller][3]])
    #-> einde identieke genotypes bij elkaar optellen        

    ingeklapt = sorted(ingeklapt, key = lambda x:x[0], reverse=True)

    return ingeklapt, totaalkans


def other_options(args, option_string):
    if args.haplotypes and args.ethnicity:
        haplotype_options = haplo(args)
        print(f"List of all possible haplotypes: {haplotype_options}.", end="")
        sys.exit()

    if args.abbriviations:
        print(f"The possible abbrivations are: {option_string}", end="")
        sys.exit()
    
    if args.list_datasets:
        ethnicity_directory = Path(pkg_resources.resource_filename(__name__, "ethnicity"))
        dataset_dict = {file.name: file for file in ethnicity_directory.iterdir()} 
        selected_dataset = questionary.select(
            "Select a dataset",
            choices=list(dataset_dict.keys()),
            style=custom_style,
            pointer="❯",
            use_jk_keys=True,
            show_selected=True,
            qmark=""
        ).ask() 
        with open(dataset_dict[selected_dataset]) as dataset:
            args.hidden_dataset = json.load(dataset)
    if args.add and args.input and args.file_abbreviation:
        to_ethnicity(args.input)
        with open(pkg_resources.resource_filename(__name__, "abbreviations.json"), "r+") as file:
            abbr_dict = json.load(file)
            full_name = Path(args.input).name.split('.')[0]
            abbr_dict[args.file_abbreviation] = full_name
        with open(pkg_resources.resource_filename(__name__, "abbreviations.json"), "w") as new_file: 
            new_file.write(json.dumps(abbr_dict, indent=4))
        sys.exit()
    

def run(args):
    args.selection = sorted(args.selection)
    separator = {'t': '\t', ',': ',', '|': '|', ';': ';', ' ': ' '}.get(args.separator)
    result, totaalkans = predict(args)
    if result != 1 and totaalkans != 1:
        tot_perm = [100*i[0]/totaalkans for i in result if i[2] > 0]
        output = args.output is not None
        filename = args.output if output else None
        if args.top:
            result_table(result, totaalkans, args.top, separator, output, filename)
        else:
            result_table(result, totaalkans, len(result), separator, output, filename)
        if output:
            with open(args.output, 'a') as output_file:
                output_file.write(f"Total Likelihood: {sum(tot_perm):.1f}")
        else:
            print(f"Total Likelihood: {sum(tot_perm):.1f}")
    else:
        print(f"No results found for this selection {' '.join(str(i) for i in args.selection)} for ethnicity {args.ethnicity}!\n"
              f"For more information use the -h option 'python haplotype.py -h'.")
        
def parser_args():
    """
    Function with all the arguments that are necessary to use the FSHD commandline tool.

    Returns:
        args: argparser.namespace: Parsed command-line arguments.
        parser: ArgumentParser: The ArgumentParser instance for the tool.
        ethnicity_full: dict: Dictonary which maps abbriviations to full names.
        option_string: string: String which says what abbrivations are possible and what they stand 
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
    parser = argparse.ArgumentParser(description=f"{a}\nA tool for predicting genotypes from SSLP values for FSHD analysis. This tool allows users to input specific SSLP selections, specify the ethnicity of the patient, and also provides the ability to add new haplotype files.", formatter_class=RawTextHelpFormatter)
    group1 = parser.add_argument_group('required arguments')
    group1.add_argument("-s", "--selection", nargs="+", type=int, required=False, metavar="SSLP",
                    help="Provide a list of four integer SSLP values. Example usage: -s 159 161 163 166.")
    ethnicity_full, options, option_string = get_abbrivations()
    group1.add_argument("-e", "--ethnicity", choices=options, required=False, metavar="ETHNICITY", 
                        help="Specify the ethnicity of the patient using the abbreviation or full name.\nSee -a/--abbriviations for the full list of options.")
    group2 = parser.add_argument_group('optional arguments')
    group2.add_argument("-H", "--haplotypes",  action="store_true", 
                        help="Use this flag to display a list of all possible haplotypes.")
    group2.add_argument("-a", "--abbriviations",  action="store_true", 
                    help="Use this flag to display a list of all abbreviations that can be used with the -e/--ethnicity option.")
    group2.add_argument("-n", "--top", type=int, metavar="N", 
                        help="Use this option to only display the top N results.\nIf not specified, all results are displayed.")
    group2.add_argument("-i", "--input", type=str, metavar="INPUT FILE",
                        help="Provide the path to a custom input JSON file containing haplotypes.")
    group2.add_argument("-o", "--output", type=str, metavar="OUTPUT FILE",
                        help="Specify the path to an output file where the results will be written.\nIf not specified, results will be printed to the console.")
    group2.add_argument("-sep", "--separator", type=str, choices=[",", "t", "|", ";", " "], default=",", metavar="SEPARATOR",
                        help="Choose a separator for the output file.\nOptions include comma (,), tab (t), pipe (|), semicolon (;), or space ( ). Default is comma ','.")
    group2.add_argument("-A", "--add", action="store_true",
                        help="Use this flag in combination with -i/--input and -Fa/--file_abbreviation to add a new haplotype file.")
    group2.add_argument("-Fa", "--file_abbreviation", type=str, metavar="FILE ABBREVIATION",
                        help="When adding a new haplotype file, specify the abbreviation to be associated with this file.")
    group2.add_argument("-l", "--list_datasets", action="store_true",
                        help="Shows a list of all the haplotype datasets available in the ethnicity directory.")
    
    args = parser.parse_args()
    return args, parser,  ethnicity_full, option_string
    

       
def main():
    args, parser, ethnicity_full, option_string = parser_args()
    args.ethnicity = ethnicity_full.get(args.ethnicity, args.ethnicity)
    args.hidden_dataset = None
    if args.selection and len(args.selection) !=  4:
        parser.error(f"You must have a input of 4 SSLP's. The length of your input is {len(args.selection)} SSLP's.")
    if validate_combinations(args):
        parser.error("Invalid combination of arguments. You must provide one of the following combinations:\n"
                     "-a/--abbriviations\n"
                     "-s/--selection and -e/--ethnicity\n"
                     "-s/--selection and -l/--list_datasets\n"
                     "-s/--selection and -i/--input\n"
                     "-h/--haplotypes and -e/--ethnicity\n"
                     "-h/--haplotypes and -i/--input\n"
                     "-A/--add, -i/--input, and -Fa/--file_abbreviation\n"
                     "-s/--selection, -e/--ethnicity, and -n/--top")
    other_options(args, option_string)
    run(args)
if __name__ == "__main__":
    main()


