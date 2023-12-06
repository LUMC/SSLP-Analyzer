import json

def convert(filename):
    with open(filename,'r') as infile:
        j_list = json.load(infile)
    result_dict = {}
    for chr_num, haplo in zip(["chr4", "chr10"], j_list):
        chr_dict = {}
        for sslp,info in haplo.items():
            sslp_list = []
            for sslp_value in info:
                sslp_dict = {}
                sslp_value = sslp_value.split("|")
                sslp_dict["haplotype"],sslp_dict["%"],sslp_dict["permissive"] = sslp_value[0],sslp_value[1],sslp_value[2]
                sslp_list.append(sslp_dict)
            chr_dict[sslp] = sslp_list
        result_dict[chr_num] = chr_dict
            
        
    with open(filename,"w") as outfile:
        outfile.write(json.dumps(result_dict,indent=4))

def main(filename):
    try:
        convert(filename)
    except AttributeError:
        print("File already converted!")
    else:
        print("File sucessfully converted!")


if __name__ == '__main__':
    main("ethnicity/African.json")