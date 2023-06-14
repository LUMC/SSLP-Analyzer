from django.shortcuts import render,redirect
from json import load
from django.urls import reverse

def home_view(request):
    return render(request, 'homepage.html')

def data_editor_view(request,population):
    edit_mode = False
    if request.method == "POST":
        if "edit" in request.POST:
            edit_mode = True
    print(population)
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)
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
                
    return render(request, 'editpage.html',{
        "population":population,
        "table_data":parsed_haplotypes,
        "population_options": haplotypes.keys(),
        "edit_mode":edit_mode
        })

def feed_view(request):
    return render(request, 'login.html')

