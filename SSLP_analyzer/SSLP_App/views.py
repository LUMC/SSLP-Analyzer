from django.shortcuts import render,redirect,HttpResponse
from json import load, loads, dumps
from django.urls import reverse
from django.http import FileResponse
from django import forms
from .utils import xslx_parser, json_parser , export_xslx

class UploadFileForm(forms.Form):
    file = forms.FileField()

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
            
def haplotype_uploader(request,population):
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file_in_memory = request.FILES['file'].read()
        df = xslx_parser(file_in_memory)
        new_population = json_parser(df)
    new_name = request.POST.get("new_population")
    haplotypes[new_name] = loads(new_population)
    with open("haplotypes.json", "w") as newfile:
        newfile.write(dumps(haplotypes, indent=4))
    return redirect("data_editor",population=new_name)


def haplotype_downloader(request, population):
    export_xslx(population)
    return FileResponse(open("result.xlsx", "rb"), filename=f"{population}.xlsx", as_attachment=True)

def data_editor_view(request, population):
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)
    edit_mode = False
    if request.method == "POST":
        print(request.user.is_superuser)
        if "edit" in request.POST:
            if request.user.is_superuser:
                edit_mode = True
        elif "done" in request.POST:
            if request.user.is_superuser:
                haplotypes, population = haplotype_saver(request, population, haplotypes)
                with open("haplotypes.json","w") as file:
                    file.write(dumps(haplotypes,indent=4))
                edit_mode = False
        elif "new_population" in request.POST:
            if request.user.is_superuser:
                return haplotype_uploader(request,population)
        elif "Download" in request.POST:
            return haplotype_downloader(request,population)
    try:
        pop_dict = haplotypes[population]
    except KeyError:
        return redirect("data_editor",population=list(haplotypes.keys())[0])
    
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
        "edit_mode":edit_mode,
        "form": UploadFileForm()
        })


def feed_view(request):
    return render(request, 'login.html')

