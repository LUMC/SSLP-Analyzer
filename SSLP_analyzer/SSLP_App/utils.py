import pandas as pd
import numpy as np
import re
import json


def haplo_parser(haplotype):
    chromosome, sslp = [int(num) for num in re.findall('\d+', haplotype)][0:2]
    haplo_string = re.sub("^\d+", '', haplotype)
    return haplo_string,chromosome,sslp

def xslx_parser(filename):
    df = pd.read_excel(filename,header=None)
    df_list = np.split(df, df[df.isnull().all(1)].index)
    for i, chrs in enumerate(df_list):
        df_list[i] = chrs.dropna(how='all').reset_index(drop=True)[1:-1].drop(columns=1)
    chr_dict = {"haplotype":[],"chr":[],"SSLP":[],"%":[],"permissive":[]}
    for dfs in df_list:
        for row in dfs.values.tolist():
            raw_haplo, percent, permissive = row
            haplotype, chromosome, sslp = haplo_parser(raw_haplo)
            chr_dict["haplotype"].append(haplotype)
            chr_dict["chr"].append(chromosome)
            chr_dict["SSLP"].append(sslp)
            chr_dict["%"].append(percent.replace(",",".").strip("%"))
            chr_dict["permissive"].append(permissive)
    df = pd.DataFrame(chr_dict)
    df["%"] = df["%"].astype(float)
    df["%"] = df["%"].div(100)
    return  df
        
        
def json_parser(df):
    df_list = df.values.T.tolist()
    result_dict = {}
    for haplo,chr_num,sslp,percent,perm in zip(*df_list):
        chromosome = f"chr{chr_num}"
        if not chromosome in result_dict:
            result_dict[chromosome] = {}
        if sslp not in result_dict[chromosome]:
            result_dict[chromosome][sslp] = []
        result_dict[chromosome][sslp].append({"haplotype":haplo,"%":percent*100,"permissive":perm})
    return json.dumps(result_dict,indent=4)

def export_xslx(population):
    with open("haplotypes.json","r") as file:
        haplotypes = json.load(file)
    save_list = []
    selected_pop = haplotypes[population]
    for chr,sslps in selected_pop.items():
        chr = chr.lstrip("chr")
        save_list.append([f"{chr}q haplotype {population}","","frequency","permissive"])
        for sslp,info in sslps.items():
            for entry in info:
                save_list.append([f"{chr}{entry['haplotype']}",None,entry["%"].replace(".",","),entry["permissive"]])
        save_list.append(["","Not available","",""])
        save_list.append(["","","",""])
    df = pd.DataFrame(save_list)
    df.to_excel(f"{population}.xlsx",header=False,index=False) 
                

            
            
        
def main(filename):
    df = xslx_parser(filename)
    json_string = json_parser(df)
     
        
    
    
if __name__ == "__main__":
    export_xslx("European")
    # main("india.xlsx")