from django.contrib.staticfiles import finders
from itertools import product
import json
import pkg_resources
import os


def predict(selection, population):
    """
    haplotypes = [[EU4, EU10], [AF4, AF10], [AS4, AS10]]
    """
    file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # Navigate up two directories from __file__
    "haplotypes.json")
    with open(file_path, "r") as f:
        ethnicity_haplotypes = json.load(f)
        ethnicity_haplotypes = ethnicity_haplotypes[population]
    
    reeksvier, reekstien, kansenreeks = [],[],[]
    totaalkans = 0
    for nr in set(selection):
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
        if sorted(nummers) == selection:
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

def result_table(result, totaalkans):
    """_summary_

    :param result: _description_
    :param totaalkans: _description_
    :param amount: _description_
    :param separator: _description_
    :param write: _description_, defaults to False
    :param filename: _description_, defaults to None
    """
    results = []
    for i in result:
        values = [str(val) for val in i[1]]
        percentage = 100 * i[0] / totaalkans
        probability = i[0]
        row = values + [f"{percentage:.1f}", str(i[2]), f"{probability:.1f}"]
        results.append(row)
    tot_perm = sum([100*i[0]/totaalkans for i in result if i[2] > 0])
    return results, tot_perm

def haplotype(selection, region):
    ingeklapt, totaalkans = predict(selection, region)
    if ingeklapt != 1:
        results, total_like = result_table(ingeklapt, totaalkans)
        return results, total_like
    return 1,1