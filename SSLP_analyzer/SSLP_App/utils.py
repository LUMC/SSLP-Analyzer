import pandas as pd
import numpy as np
from os import getcwd
import re


def haplo_parser(haplotype):
    chr,sslp = [int(num) for num in re.findall('\d+', haplotype)]
    haplo_string = re.sub("^\d+", '', haplotype)
    return haplo_string,chr,sslp



def xslx_parser(filename):
    df = pd.read_excel(filename,header=None)
    df_list = np.split(df, df[df.isnull().all(1)].index)
    for i, chrs in enumerate(df_list):
        df_list[i] = chrs.dropna(how='all').reset_index(drop=True)[1:-1].drop(columns=1)
    
    chr_dict = {}
    for chrs in df_list:
        print(chrs.values.tolist())
        break
        
    
    print(df_list[0])
    haplo_parser("10A161S")
        


    # print(df_list)
    
    
if __name__ == "__main__":
    xslx_parser("india.xlsx")