
import argparse
from argparse import RawTextHelpFormatter
from itertools import product
import sys
import json
haplotypes = [
            [
                {
                    159:['A159|0.1|1'], 161:['A161|39.2|1', 'B161|0.7|0'], 163:['A163|0.9|1', 'B163|32.9|0'],
                    166:['A166|4.4|0', 'A166H|3.9|1', 'B166|1|0'], 168:['A168|0.3|1', 'B168|13.2|0'],
                    170:['A170|0.2|1', 'B170|0.5|0'], 172:['A172|0.2|1', 'B172|0.2|0'], 162:['B162|1.8|0'],
                    174:['B174|0.2|0']
                    },
                {
                    162:['A162|0.2|0'], 164:['A164|4.4|0'], 166:['A166|86.1|0', 'A166H|0.6|1'],
                    176:['A176T|2.5|0'], 180:['A180T|0.5|0'], 161:['B161T|4.6|0']
                    }
            ],
            [
                {
                    157:['A157|1.7|1'], 159:['A159|17.5|1'], 161:['A161|24.2|1', 'B161|0.8|0'], 163:['B163|8.3|0'],
                    166:['A166|3.3|0', 'A166H|19.2|1', 'B166|0.8|0', 'C166H|14.2|1'], 172:['B172|5.8|0']
                    },
             {
                 162:['A162|9.2|0'], 164:['A164|3.3|0'], 166:['A166|77.5|0', 'A166H|3.3|1'],
                 176:['A176T|0.8|0'], 180:['A180T|1.7|0']
                 }
             ],
            [
                {
                    161:['A161|34.3|1'], 163:['A163|0.6|1', 'B163|57.3|0'],
                    166:['A166|0.6|0', 'A166H|2.8|1', 'B166|0.6|0'], 170:['B170|0.6|0']
                    },
             {
                 161:['B161T|8.4|0'], 164:['A164|25.8|0'], 166:['A166|53.9|0', 'A166H|11.8|1']
                 }
             ]
            ]

# with open('haplotypes.json', 'w') as f:
#     json.dump(haplotypes, f, indent=4)

def predict(p_selection, p_region, input_type):
    """
    haplotypes = [[EU4, EU10], [AF4, AF10], [AS4, AS10]]
    """
    regionnr = {'European':0, 'African':1, 'Asian':2}[p_region]
    
    
    
    reeksvier, reekstien, kansenreeks = [],[],[]
    totaalkans = 0
    for nr in set(p_selection):
        if input_type is not None:
            nr = str(nr)
        for i in range(2):
            try:
                if i == 0:
                    reeksvier += haplotypes[regionnr][i][nr]
                else:
                    reekstien += haplotypes[regionnr][i][nr]
            except LookupError as e:
                pass


    #-> alle mogelijkheden genereren
    for i,j,k,l in product(reeksvier, reeksvier, reekstien, reekstien):
        nummers = [int(i.split('|')[0][1:4]), int(j.split('|')[0][1:4]), int(k.split('|')[0][1:4]), int(l.split('|')[0][1:4])]
        if sorted(nummers) == p_selection: #checken of ze wel uniek zijn (of de nummers kloppen met het voorbeeld)                   
            kans = (float(i.split('|')[1]) * float(j.split('|')[1]) * float(k.split('|')[1]) * float(l.split('|')[1]))/1000000
            berekening = i.split('|')[1] + ' * ' + j.split('|')[1] + ' * ' + k.split('|')[1] + ' * ' + l.split('|')[1] 
            genotype = ['4' + i.split('|')[0], '4' + j.split('|')[0], '10' + k.split('|')[0], '10' + l.split('|')[0]]
            p = int(i.split('|')[2]) + int(j.split('|')[2]) + int(k.split('|')[2]) + int(l.split('|')[2]) 
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


def haplo():
    unique_haplotypes = set()
    for haplotype in haplotypes:
        for haplotype_name in ([set(haplotype.keys()) for haplotype in haplotype]):
            unique_haplotypes.update(haplotype_name)
    haplotype_string = ", ".join(map(str, sorted(unique_haplotypes)))
    return haplotype_string

def run(args):
    p_selection = sorted(args.selection)
    p_region = args.region
    separator = {'t': '\t', ',': ',', '|': '|', ';': ';', ' ': ' '}.get(args.separator)
    result, totaalkans = predict(p_selection, p_region, args.input)
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
        print(f"No results found for this selection {' '.join(str(i) for i in p_selection)} in this region {p_region}!\n"
              f"For more information use the -h option 'python haplotype.py -h'.")
def main():
    parser = argparse.ArgumentParser(description="Predict genotypes from SSLP values for FSHD analysis", formatter_class=RawTextHelpFormatter)
    group1 = parser.add_argument_group('required arguments')
    group1.add_argument("-s", "--selection", nargs="+", type=int, required=False, metavar="SSLP",
                    help="Integer values representing the SSLP selection.\n"
                         "It must always be a length of 4 SSLP's.\n"
                         "Example: -s 159 161 163 166.")
    group1.add_argument("-r", "--region", choices=["EU", "AF", "AS", "European", "African", "Asian"], required=False, metavar="REGION", 
                        help="The region the sample is from.\n"
                        "Choose from: EU (European), AF (African), AS (Asian).")
    group2 = parser.add_argument_group('optional arguments')
    group2.add_argument("-H", "--haplotypes",  action="store_true", 
                        help="Display the list of all possible haplotypes.")
    group2.add_argument("-n", "--top", type=int, metavar="N", 
                        help="Display top N results. If not specified, all results are displayed.")
    group2.add_argument("-i", "--input", type=str, metavar="INPUT FILE",
                        help="Path to the input JSON file containing haplotypes.")
    group2.add_argument("-o", "--output", type=str, metavar="OUTPUT FILE",
                        help="Specify the output file where the results will be written.")
    group2.add_argument("-sep", "--separator", type=str, choices=[",", "t", "|", ";", " "], metavar="SEPARATOR",
                        help="Choose a separator for the output file.\n"
                        "For a tab, enter 't'.\n"
                        " Default is comma ','.", default=",")

    args = parser.parse_args()
    if args.selection:
        if len(args.selection) !=  4:
            parser.error(f"You must have a input of 4 SSLP's. The length of your input is {len(args.selection)} SSLP's.")
    
    global haplotypes
    region_full = {"EU": "European", "AF": "African", "AS": "Asian"}
    args.region = region_full.get(args.region, args.region)

    if args.input:
        with open(args.input, 'r') as f:
            haplotypes = json.load(f)
    
    
    if args.haplotypes:
        haplotype_options = haplo()
        print(f"List of all possible haplotypes: {haplotype_options}.")
        sys.exit()

    if args.selection is None or args.region is None:
        parser.error("the following arguments are required: -s/--selection, -r/--region")


    run(args)

if __name__ == "__main__":
    main()

