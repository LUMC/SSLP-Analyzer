
import argparse
from argparse import RawTextHelpFormatter
from itertools import product
import sys
import json



def get_ethnicity(ethnicity):
    """Fetches the ethnicity data from the supplied 
    ethnicity. And returns this as a dcitonary.
    :param ethnicity: Full ethnicity name
    :return: haplotype dictonary for specified ethnicity
    """
    with open(f"ethnicity/{ethnicity}.json","r") as file:
        haplo_dict = json.load(file)
        print(f"Using haplotypes from file: ethnicity/{ethnicity}.json")
    return haplo_dict

def predict(p_selection, p_region, input_type):
    """
    haplotypes = [[EU4, EU10], [AF4, AF10], [AS4, AS10]]
    """
    
    ethnicity_haplotypes = get_ethnicity(p_region)
    
    
    reeksvier, reekstien, kansenreeks = [],[],[]
    totaalkans = 0
    for nr in set(p_selection):
        nr = str(nr)
        for chr in ethnicity_haplotypes:
            # print(chr)
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
        if sorted(nummers) == p_selection: #checken of ze wel uniek zijn (of de nummers kloppen met het voorbeeld)                   
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


def haplo(): # Currently broken
    unique_haplotypes = set()
    for haplotype in haplotypes:
        for haplotype_name in ([set(haplotype.keys()) for haplotype in haplotype]):
            unique_haplotypes.update(haplotype_name)
    haplotype_string = ", ".join(map(str, sorted(unique_haplotypes)))
    return haplotype_string

def run(args):
    p_selection = sorted(args.selection)
    p_ethnicity = args.ethnicity
    separator = {'t': '\t', ',': ',', '|': '|', ';': ';', ' ': ' '}.get(args.separator)
    result, totaalkans = predict(p_selection, p_ethnicity, args.input)
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
        print(f"No results found for this selection {' '.join(str(i) for i in p_selection)} for ethnicity {p_ethnicity}!\n"
              f"For more information use the -h option 'python haplotype.py -h'.")
        

def get_abbrivations():
    """Fetches the abbrivations from abbrivations.json
    Returns this data as different objects
    :return: 
    abbr_dict: dict: Dictonary which maps abbriviations to full names
    options: list: List which contains all abrivations and full names
    option_string: str: String which says what abbrivations are possible and what they stand
    """
    with open("abbreviations.json","r") as file:
        abbr_dict = json.load(file)
        options = list(abbr_dict.keys()) + list(abbr_dict.values())
        option_string = ""
        for k,v in abbr_dict.items():
            option_string += f"{k} ({v}) "
    return abbr_dict, options, option_string
        

       
def main():
    parser = argparse.ArgumentParser(description="Predict genotypes from SSLP values for FSHD analysis", formatter_class=RawTextHelpFormatter)
    group1 = parser.add_argument_group('required arguments')
    group1.add_argument("-s", "--selection", nargs="+", type=int, required=False, metavar="SSLP",
                    help="Integer values representing the SSLP selection.\n"
                         "It must always be a length of 4 SSLP's.\n"
                         "Example: -s 159 161 163 166.")
    ethnicity_full, options, option_string = get_abbrivations()
    group1.add_argument("-e", "--ethnicity", choices=options, required=False, metavar="ETHNICITY", 
                        help="The ethnicity of the patient.")
    group2 = parser.add_argument_group('optional arguments')
    group2.add_argument("-H", "--haplotypes",  action="store_true", 
                        help="Display the list of all possible haplotypes.")
    group2.add_argument("-a", "--abbriviations",  action="store_true", 
                    help="Display the list of all possible abbriviations.")
    group2.add_argument("-n", "--top", type=int, metavar="N", 
                        help="Display top N results. If not specified, all results are displayed.")
    group2.add_argument("-i", "--input", type=str, metavar="INPUT FILE",
                        help="Path to the input JSON file containing haplotypes.")
    group2.add_argument("-o", "--output", type=str, metavar="OUTPUT FILE",
                        help="Specify the output file where the results will be written.")
    group2.add_argument("-sep", "--separator", type=str, choices=[",", "t", "|", ";", " "], metavar="SEPARATOR",
                        help="Choose a separator for the output file.\n"
                        "For a tab, enter 't'.\n"
                        "Default is comma ','.", default=",")

    args = parser.parse_args()
    if args.selection:
        if len(args.selection) !=  4:
            parser.error(f"You must have a input of 4 SSLP's. The length of your input is {len(args.selection)} SSLP's.")
    
    args.ethnicity = ethnicity_full.get(args.ethnicity, args.ethnicity)

    if args.input:
        with open(args.input, 'r') as f:
            haplotypes = json.load(f)
        
    if args.haplotypes: # Currently broken
        haplotype_options = haplo()
        print(f"List of all possible haplotypes: {haplotype_options}.", end="")
        sys.exit()

    if args.abbriviations:
        print(f"The possible abbrivations are: {option_string}", end="")
        sys.exit()


    if args.selection is None or args.ethnicity is None:
        parser.error("the following arguments are required: -s/--selection, -r/--region")

    run(args)
if __name__ == "__main__":
    main()

