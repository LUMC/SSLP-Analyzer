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
    """
    The function generates a nested dictionary for the selected population,
    containing information for chromosome 4 and 10 along with the corresponding SSLPS,
    including their haplotype, percentage, and permissive state. It also checks to determine
    if the name of the population has been modified and if necessary, updates it accordingly.


    Args:
        request (django.http.HttpRequest): The request object that carries all 
        the information from a client to the server. It is used in this
        particular case to access the new population name and all the 
        values from all the different input fields.
        population (str): A string containing the name of the population 
        that currently is viewed.
        haplotypes (dict): A nested dictionary containing the chromosomes, 
        haplotypes and their corresponding values for this population.

    Returns:
        haplotypes: A dictionary containing new or updated information about the chromosomes, 
        haplotypes and their corresponding values for this population.  
    """
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
            
def haplotype_uploader(request):
    """
    This function processes an XSLX file that has been uploaded by the user and 
    converts it to a JSON file by utilizing the specialized XSLX_parser and 
    JSON_parser functions. These functions return a dictionary containing 
    values such as chromosome, SSLP, haplotype, percentage, and permissive 
    state in the correct format. The content from the dictionary is
    written to a JSON file called "haplotypes.json" after it. 

    Args:
        request (django.http.HttpRequest): The request object that carries all 
        the information from a client to the server. It is used in this
        particular case to access the uploaded file and any other form of data.

    Returns:
        django.http.HttpResponseRedirect: A redirect response object which 
        can be used to redirect the user to another page.
    """
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


def haplotype_downloader(population):
    """
    Download the selected haplotype file from the chosen population. 
    It uses the export_xslx to convert it to the appropriate excel format.

    Args:
        population (str): A string containing the name of the population that 
        currently is viewed.

    Returns:
        django.http.FileResponse: A FileResponse object which serves the content of the requested 
            file ("result.xslx") to the client for download.
    """
    export_xslx(population)
    return FileResponse(open("result.xlsx", "rb"), filename=f"{population}.xlsx", as_attachment=True)

def data_editor_view(request, population):
    """
    This function is responsible for checking the information from the POST 
    request such as "edit", "done", "new_population", and "Download" to 
    perform various operations on the data such as modifying the haplotype 
    data, saving the changes, uploading a new population's data, or 
    downloading the data for a population. It also overwrites
    some variables if necessary such as editmode if the user is a superuser.
    

    Args:
        request (django.http.HttpRequest): The request object that carries all 
        the information from a client to the server. It is used in this
        particular case to check which button is clicked.
        population (str): A string containing the name of the population 
        that currently is viewed.

    Returns:
         (django.http.HttpResponseRedirect): A HttpResponse object with the 
         context data necessary for rendering the 'editpage.html' template. 
         If the population does not exist, it will return to the default value.
         In our case, the first population in the "haplotypes.json" file.
    """
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)
    edit_mode = False
    if request.method == "POST":
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
                return haplotype_uploader(request)
        elif "Download" in request.POST:
            return haplotype_downloader(population)
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
    
    return render(request, 'editpage.html',{
        "population":population,
        "table_data":parsed_haplotypes,
        "population_options": haplotypes.keys(),
        "edit_mode":edit_mode,
        "form": UploadFileForm()
        })


def feed_view(request):
    return render(request, 'login.html')

