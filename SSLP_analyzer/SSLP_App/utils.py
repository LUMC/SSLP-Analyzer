import pandas as pd
import numpy as np
import re
import json


def haplo_parser(haplotype):
    """halpo_parser
    Parses the haplotype string and extracts the chromosome value and the sslp
    It does this by extracting the first two ints.

    :param haplotype: haplotype string
    :return: (str,int,int) haplotype_string, chromosome , sslp
    """
    chromosome, sslp = [int(num) for num in re.findall('\d+', haplotype)][0:2]
    haplo_string = re.sub("^\d+", '', haplotype)
    return haplo_string,chromosome,sslp

def xslx_parser(filename):
    """xslx_parser
    Reads the supplied xslx file and parses it so it can be saved to haplotypes.json.
    It returns a pandas dataframe which contains the data.
    :param filename: (str) the name of the file to save it as
    :return: df (pd.DataFrame) dataframe with all read in data.
    """
    df = pd.read_excel(filename,header=None)
    df_list = np.split(df, df[df.isnull().all(1)].index)
    for i, chrs in enumerate(df_list):
        df_list[i] = chrs.dropna(how='all').reset_index(drop=True)[1:]
    chr_dict = {"haplotype":[],"chr":[],"SSLP":[],"%":[],"permissive":[]}
    for dfs in df_list:
        for row in dfs.values.tolist():
            raw_haplo, percent, permissive = row
            haplotype, chromosome, sslp = haplo_parser(raw_haplo)
            chr_dict["haplotype"].append(haplotype)
            chr_dict["chr"].append(chromosome)
            chr_dict["SSLP"].append(sslp)
            chr_dict["%"].append(percent)
            chr_dict["permissive"].append(permissive)
    df = pd.DataFrame(chr_dict)
    df["%"] = df["%"].astype(float)
    if max(df["%"]) <= 1:
        df["%"] = df["%"].multiply(100)
    return  df
        
        
def json_parser(df):
    """json_parser
    Takes in a pandas dataframe and converts this to a json string which can be saved 
    to haplotypes.json.

    :param df: (pd.DataFrame) pandas dataframe containing the data
    :return: (str) json.dumps string which is in same format as haplotypes.json
    """
    df_list = df.values.T.tolist()
    result_dict = {}
    for haplo,chr_num,sslp,percent,perm in zip(*df_list):
        chromosome = f"chr{chr_num}"
        if not chromosome in result_dict:
            result_dict[chromosome] = {}
        if sslp not in result_dict[chromosome]:
            result_dict[chromosome][sslp] = []
        result_dict[chromosome][sslp].append({"haplotype":haplo,"%":"{:0.1f}".format(percent),"permissive":str(perm)})
    return json.dumps(result_dict,indent=4)

def export_xslx(population):
    """export_xslx
    Reads the selected population from a file and 
    saves this data to result.xlsx. This is then saved to result.xlsx so it can later be served to the user.

    :param population: (str) the selected population
    """
    with open("haplotypes.json","r") as file:
        haplotypes = json.load(file)
    save_list = []
    selected_pop = haplotypes[population]
    for chr,sslps in selected_pop.items():
        chr = chr.lstrip("chr")
        save_list.append([f"{chr}q haplotype {population}","frequency (%)","permissive"])
        for sslp,info in sslps.items():
            for entry in info:
                save_list.append([f"{chr}{entry['haplotype']}",float(entry["%"]),int(entry["permissive"])])
        save_list.append(["","","",""])
    df = pd.DataFrame(save_list)
    df.to_excel(f"result.xlsx",header=False,index=False) 
    
                

            
            
        
def main(filename):
    df = xslx_parser(filename)
    json_string = json_parser(df)
    print(df)
     
        
    
    
if __name__ == "__main__":
    export_xslx("European")
    # main("india.xlsx")
    