from django.shortcuts import render,redirect
from json import load,dumps
from django.urls import reverse

def home_view(request):
    return render(request, 'homepage.html')



def haplotype_saver(request, population, haplotypes):
    POST_value = dict(request.POST)
    new_population_name = POST_value.get("new_population")[0]
    save_dict = {}
    for pack in zip(POST_value.get("haplo"), POST_value.get("chr"), POST_value.get("SSLP"), POST_value.get("percent"), POST_value.get("perm")):
        if all(pack):
            haplo, chr, sslp, percent, perm = pack
            if chr not in save_dict:
                save_dict[chr] = {}
            if sslp not in save_dict[chr]:
                save_dict[chr][sslp] = [{
                    "haplotype": haplo,
                    "%": percent,
                    "permissive": perm
                }]
            else:
                save_dict[chr][sslp].append({
                    "haplotype": haplo,
                    "%": percent,
                    "permissive": perm
                })
    if population != new_population_name:
        del haplotypes[population]
        haplotypes[new_population_name] = save_dict
        population = new_population_name
    else:
        haplotypes[population] = save_dict
    return haplotypes, population
            

def data_editor_view(request,population):
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)
    edit_mode = False
    if request.method == "POST":
        if "edit" in request.POST:
            edit_mode = True
        elif "done" in request.POST:
            haplotypes, population = haplotype_saver(request,population,haplotypes)
            edit_mode = False
    try:
        pop_dict = haplotypes[population]
    except KeyError:
        return redirect("data_editor",population="European")
    
    parsed_haplotypes = []
    for chr,chrdict in pop_dict.items():
        for SSLP,haplolist in chrdict.items():
            for haplodict in haplolist:
                d = {"haplo":haplodict["haplotype"], "chr":chr,"SSLP":SSLP,"percent":haplodict["%"],"perm": haplodict["permissive"]}
                parsed_haplotypes.append(d)
    if edit_mode:
        parsed_haplotypes.append({"haplo":"", "chr":"","SSLP":"","percent":"","perm": ""})
    
    # print(parsed_haplotypes[0])
    return render(request, 'editpage.html',{
        "population":population,
        "table_data":parsed_haplotypes,
        "population_options": haplotypes.keys(),
        "edit_mode":edit_mode
        })


def feed_view(request):
    return render(request, 'login.html')

