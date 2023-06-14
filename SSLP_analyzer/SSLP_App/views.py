from django.shortcuts import render
from json import load

def home_view(request):
    return render(request, 'homepage.html')

def data_editor_view(request,population):
    print(population)
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)[population]
    parsed_haplotypes = []
    for chr,chrdict in haplotypes.items():
        for SSLP,haplolist in chrdict.items():
            for haplodict in haplolist:
                d = {"haplo":haplodict["haplotype"], "chr":chr,"SSLP":SSLP,"percent":haplodict["%"],"perm":haplodict["permissive"]}
                parsed_haplotypes.append(d)
                
    return render(request, 'editpage.html',{"table":parsed_haplotypes})

def feed_view(request):
    return render(request, 'login.html')

