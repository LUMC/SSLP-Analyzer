from itertools import product
import json
import pkg_resources
import os

def read_haplotypes(population):
    """read_haplotypes
    This function reads the haplotypes.json file and extracts the haplotypes of the supplied population.
    This is then returned as a dictionary.

    :param population: (str) the selected population.
    :return: (dict) sslp's with given haplotypes and their values.
    """
    file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  
    "haplotypes.json")
    with open(file_path, "r") as f:
        haplotypes = json.load(f)
        haplotypes = haplotypes[population]
    return haplotypes

def extract_sslps(selection,haplotypes):
    """extract_sslps
    Extracts the given sslp's and puts these in a list seperated by chromosome.

    :param selection: (list) sorted list of sslp's.
    :param haplotypes: (dict) haplotypes dictonary for selected population.
    :return: (list,list) two list of sslp's and corresponding haplotypes for chromosome 4 & 10 
    """
    chr4_SSLPs, chr10_SSLPs = [],[]
    for nr in set(selection):
        nr = str(nr)
        for chr in haplotypes:
            try:
                if chr == "chr4":
                    chr4_SSLPs += haplotypes[chr][nr]
                elif chr == "chr10":
                    chr10_SSLPs += haplotypes[chr][nr]
            except LookupError as e:
                pass
    return chr4_SSLPs,chr10_SSLPs

def generate_all_combinations(selection,chr4_SSLPs,chr10_SSLPs):
    """generate_all_combinations
    Calculates all possible combinations for the four selected sslp values. 
    Also calculates the likelyhood of this genotype being present.

    :param selection: (list) sorted list of sslp's.
    :param chr4_SSLPs: (list) list of sslp's with corresponding haplotypes for chromosome 4.
    :param chr10_SSLPs: (list) list of sslp's with corresponding haplotypes for chromosome 10.
    :return: (list,float) list of chances for each combination , total chance of permissive genotype being present.
    """
    total_permissive_chance = 0
    permissive_chance = []
    for i,j,k,l in product(chr4_SSLPs, chr4_SSLPs, chr10_SSLPs, chr10_SSLPs):
        nummers = [int(i["haplotype"][1:4]), int(j["haplotype"][1:4]), int(k["haplotype"][1:4]), int(l["haplotype"][1:4])]
        if sorted(nummers) == selection:
            chance = (float(i["%"]) * float(j["%"]) * float(k["%"]) * float(l["%"]))/1000000
            chance_calculation = i["%"] + ' * ' + j["%"] + ' * ' + k["%"] + ' * ' + l["%"] 
            genotype = ['4' + i["haplotype"], '4' + j["haplotype"], '10' + k["haplotype"], '10' + l["haplotype"]]
            permissive = int(i["permissive"]) + int(j["permissive"]) + int(k["permissive"]) + int(l["permissive"]) 
            permissive_chance.append([chance, genotype, chance_calculation, permissive])
            total_permissive_chance += chance
    return permissive_chance,total_permissive_chance

def combine_identical_genotypes(sorted_by_chance):
    """combine_identical_genotypes
    Combines the identical genotypes that are present in the results.

    :param sorted_by_chance: (list) List of results that are present sorted by chance.
    :return: (list) Combined sorted genotypes.
    """
    combined_genotypes = []
    counter = 1
    checker = sorted_by_chance[0]
    for i in range(1, len(sorted_by_chance)):
        if sorted_by_chance[i][0] - checker[0] < 0.000001 and sorted(sorted_by_chance[i][1]) == sorted(checker[1]):
            counter += 1
        else:
            combined_genotypes.append([sorted_by_chance[i-counter][0]*counter, sorted_by_chance[i-counter][1], sorted_by_chance[i-counter][3]])
            counter = 1
            checker = sorted_by_chance[i]
    combined_genotypes.append([sorted_by_chance[i][0]*counter, sorted_by_chance[i][1], sorted_by_chance[i-counter][3]])
    return sorted(combined_genotypes, key = lambda x:x[0], reverse=True)



def predict(selection, population):
    """predict
    Overhead function that collects all variables and executes required functions.

    :param selection: (list) List of sorted sslp values.
    :param population: (str) Selected population by user.
    :return: (list,float) OR (int,int) returns a list with all results and the total chance of a permissive genotype being present
    or returns (1,1) if no results are present.
    """
    haplotypes = read_haplotypes(population)
    chr4_SSLPs, chr10_SSLPs = extract_sslps(selection,haplotypes)
    permissive_chance, total_permissive_chance = generate_all_combinations(selection,chr4_SSLPs,chr10_SSLPs)
    sorted_by_chance = sorted(permissive_chance, key = lambda x:x[0], reverse=True)
    if len(sorted_by_chance) > 0:
        combined_genotypes = combine_identical_genotypes(sorted_by_chance)
        return combined_genotypes, total_permissive_chance
    else:
        return 1, 1

def format_results(combined_genotypes, total_permissive_chance):
    """format_results
    Formats the results in a way that it can be parsed by the webpage.
    Also calculates the likelyhood of this combination being present.

    :param combined_genotypes: (list) Combined sorted genotypes.
    :param total_permissive_chance: (float) total chance of permissive genotype being present.
    :return: (list,int) reformatted results, total likelyhood of permissive genotype. 
    """
    results = []
    for i in combined_genotypes:
        values = [str(val) for val in i[1]]
        percentage = 100 * i[0] / total_permissive_chance
        probability = i[0]
        row = values + [f"{percentage:.1f}", str(i[2]), f"{probability:.1f}"]
        results.append(row)
    total_likelyhood = sum([100*i[0]/total_permissive_chance for i in combined_genotypes if i[2] > 0])
    return results, total_likelyhood

def haplotype(selection, population):
    """haplotype
    Starter overhead function that initiates predict method. 
    
    :param selection: (list) List of sorted sslp values.
    :param population: (str) Selected population by user.
    :return: results,total permissive likelyhood, OR 1,1 if no results present.
    """
    combined_genotypes, total_permissive_chance = predict(selection, population)
    if combined_genotypes != 1:
        results, total_likelyhood = format_results(combined_genotypes, total_permissive_chance)
        return results, total_likelyhood
    return 1,1
