from django.shortcuts import render,redirect,HttpResponse
from json import load, loads, dumps
from django.urls import reverse
from django.http import FileResponse
from django import forms
from .utils import xslx_parser, json_parser , export_xslx
from django.contrib import messages
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from .utils import haplotype
import json
import re
from django.contrib import messages

class UploadFileForm(forms.Form):
    file = forms.FileField(), HttpResponse

def check_SSLP(data, new_SSLP):
    """
    This function takes the saved data, and checks if a name is already
    the saved data. If the name is already in saved data a False is returned,
    otherwise True is returned.
    :param data: The dictionary with saved data.
    :param new_SSLP: The name of the to be added SSLPs.
    :return: A boolean with true for name not in saved, and false for
    name in saved.
    """
    for key in data:
        if new_SSLP == data[key]['SSLPS']:
            return False
    return True


def get_new_key(dict_data, base_name):
    """
    This function takes the dictionary with saved results and the
    name that is to be added, and checks how many times the name is in
    dict_data. To the name a string is added with a number one higher than
    the amount of times the name is in dict_data.
    :param dict_data: The dictionary with saved data.
    :param base_name: The name of the to be added SSLPs.
    :return: The name of the SSLPs with a number behind it.
    """
    i = 2
    new_name = base_name
    while new_name in dict_data:
        new_name = f"{base_name}({i})"
        i += 1
    return new_name


def export_home_view(request):
    """
    This function takes the saved data currently in session, writes it away
    to a file, this file can then be downloaded.
    :param request: The web request.
    :return: The response that is to be shown to the user. This
    response triggers a download.
    """
    combinations = request.session.get('combinations', {})

    starting_header = ["position", "SSLP-1", "SSLP-2", "SSLP-3",
                       "SSLP-4", "population",
                       "Total likelihood permissive genotype"]
    repeating_header = ["chr4_1", "chr4_2", "chr10_1", "chr10_2",
                        "probability(%)", "permissive alleles",
                        "population incidence"]
    save_string = ""
    max_len = 0
    """this forloop goes through all saved data, creates the results
    and writes it away to the corresponding file. The results of one table 
    end up in one line of the file."""
    for key, values in combinations.items():
        id = key
        sslp = values['SSLPS']
        population = values['Population']
        table_haplotype_filled, total_perc = haplotype(sorted(sslp),
                                                       population)
        if table_haplotype_filled != 1:
            haplotype_table = table_haplotype_filled
            entry_list = [id] + sslp
            entry_list.append(population)
            entry_list.append(total_perc)
            for entry in haplotype_table:
                entry_list += entry
            if len(entry_list) > max_len:
                max_len = len(entry_list) - len(starting_header)
            save_string += ";".join(map(str, entry_list)) + "\n"
    headers_needed = max_len // len(repeating_header)
    header = starting_header + repeating_header * headers_needed
    header_str = ";".join(header) + "\n"
    return_results = header_str + save_string
    content = return_results.replace(".", ",")
    filename = "result.csv"
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filename)
    return response


def home_view(request):
    """
    This view creates the homepage, and handles the functionality of almost
    every button.
    :param request: The webrequest
    :return: The information needed for the user to be shown all information
    on the homepage within a render.
    """
    table_haplotype_filled = None
    switch_title = False
    total_perc, title, saved_results, haplotype_table = "", "", [], []
    all_sslps, populations = list_of_sslps()

    if 'export_button' in request.POST:
        return export_home_view(request)

    elif 'name_save' in request.POST:
        """
        This elif statement is executed when the 'name_save' button is pressed in the form. It takes the name
        entered by the user and saves the last result with that name. If the custom name already exists in the saved results,
        a new name is generated using the 'get_new_key' function. You will then see "existing_name(x)". x is a ascending number.
        The function updates the 'combinations' dictionary in the session with the new result and sets it as the current
        combinations. It then calculates the haplotype table and total likelihood for the saved result.
        """
        if request.POST.get("result_check"):
            name_result = request.POST.get("name_result")
            last_result = request.session.get('last_result', {})
            combinations = request.session.get('combinations', {})
            key = list(last_result.keys())[0]
            value = last_result[key]
            title = f'{name_result}' 
            if name_result in list(combinations.keys()):
                name_result = get_new_key(combinations, name_result)
            combinations[name_result] = value
            request.session["combinations"] = combinations
            table_haplotype_filled, total_perc_int = haplotype(
                sorted(value["SSLPS"]),
                value["Population"])
            total_perc = f'{total_perc_int:.1f}%'
            if table_haplotype_filled == 1 and total_perc_int == 1:
                switch_title = True
                total_perc = ""
                title = "Current selection does not return results"
            haplotype_table = table_haplotype_filled
            total_perc = f'{total_perc_int:.1f}%'
            title = f'{name_result}'
        else:
            messages.warning(request,"Empty result cannot be saved.")
    
    elif 'delete_saved' in request.POST:
        """
        When the delete button is pressed next to a saved result,
        combinations is pulled form session. The value corresponding to
        the deleted button that is pressed gets deleted from the saved 
        results and saved results gets put back in to the session. 
        """
        combinations = request.session['combinations']
        chosen_result = request.POST.get('delete_saved')
        del combinations[chosen_result]
        request.session["combinations"] = combinations

    elif 'change_result_submit' in request.POST:
        """
        This function activates when a saved result is clicked, and puts
        the saved result back into the screen. All combinations are requested,
        and the clicked result is pulled from the dictionary. The title
        is set as the name of the clicked result. The results are generated
        and if a result is returned the table gets shown, otherwise a message 
        is shown that tells the user no results were created. The clicked
        result becomes the data in the session last_result. 

        """
        chosen_result = request.POST.get('change_result_submit')
        combinations = request.session.get('combinations', {})
        chosen_result_dict = combinations[str(chosen_result)]
        title = f'{chosen_result}'
        table_haplotype_filled, total_perc_int = haplotype(
            sorted(chosen_result_dict["SSLPS"]),
            chosen_result_dict["Population"])
        total_perc = f'{total_perc_int:.1f}%'
        if table_haplotype_filled == 1 and total_perc_int == 1:
            switch_title = True
            title = "Current selection does not return results"
            total_perc = ""
        haplotype_table = table_haplotype_filled
        request.session["last_result"] = {chosen_result:chosen_result_dict} 

    elif "predict" in request.POST:
        """
        This elif statement is executed when the 'predict' button is pressed in the form. It takes the selected SSLP
        values and population name from the request. It then creates a new result dictionary with the SSLP values and
        population name. The function updates the 'last_result' and 'combinations' dictionaries in the session. If the SSLP values and            population name are not empty, it calculates the haplotype table and total likelihood for the selected
        SSLP values and population.
        """
        SSLPs = request.POST.getlist('SSLP_value')
        population_name = request.POST.get('population_name')
        last_result = request.session.get('last_result', {})
        combinations = request.session.get('combinations', {})
        last_result = {
            "new": {
                "Population": population_name,
                "SSLPS": [int(i) for i in SSLPs],
            }
        }
        request.session["last_result"] = last_result
        if "" not in SSLPs and population_name != "":
            SSLPs = sorted([int(i) for i in SSLPs])
            table_haplotype_filled, total_perc_int = haplotype(SSLPs,
                                                               population_name)
            if table_haplotype_filled != 1:
                haplotype_table = table_haplotype_filled
                total_perc = f'{total_perc_int:.1f}%'
                title = f'{SSLPs} {population_name}'
            else:
                title = "Current selection does not return results"
                switch_title = True
                total_perc = ""
    elif "upload" in request.POST:
        """
        This function handles the creation of results from a file. 
        A file is uploaded and the content of the file is saved in 
        input_data_file. Within a try the data is split into usable parts and
        added to the saved_results in the session(combinations). This part of
        the function is in a try to account for data with incorrect formatting.
        When the user uploads a file with issues, the correct error message
        is shown. If the population is missing or correct the first population
        in the database is used. The for loop at the end of the try adds all
        the data to the saved results. After the loop the first entry gets
        shown on screen.
        """
        input_data_file = str(request.FILES['upload'].read())
        try:
            input_data_list = input_data_file.split("\\r\\n")
            population_fromfile = input_data_list[1].split(';')[-1]
            if population_fromfile == "":
                population_fromfile = populations[0]
                messages.info(request, f"No population was found in file, the default value {population_fromfile} was used instead.")
            elif population_fromfile not in populations:
                population_fromfile = populations[0]
                messages.info(request, f"Population found in file is not currently in database, the default value {population_fromfile} was used instead.")
            combinations = {}
            request.session["combinations"] = {}

            for line in input_data_list[1:-1]:
                items = line.split(';')[:-1]
                id = items[0]
                sslps = [int(x) for x in items[1:]]
                combinations[id] = {'Population': population_fromfile,
                                    'SSLPS': sslps}
            request.session["combinations"] = combinations
            if table_haplotype_filled != 1:
                haplotype_table = table_haplotype_filled
                total_perc = f'{total_perc_int:.1f}%'
                title = f'{SSLPs} {population_fromfile}'
            else:
                title = "Current selection does not return results"
                switch_title = True
                total_perc = ""
        except IndexError:
            messages.warning(request, 'File cannot be uploaded due to the wrong format.')
        except ValueError:
            messages.warning(request, 'One or more lines of file include text where numbers are expected.')
    return render(request, 'homepage.html', {
        'Title': title,
        'data': haplotype_table,
        'saved_results': get_saved_results(request),
        'chrom_lengths': all_sslps,
        'populations': populations,
        'likelihood': total_perc,
        'switch_title': switch_title,
        'result_check': "" if not table_haplotype_filled or table_haplotype_filled == 1 else True 
    })


def list_of_sslps():
    """
        Summary:
            This function reads a JSON file that contains SSLPs and populations data. It extracts the SSLPs and populations
            from the file and returns them as separate lists.
        Returns:
            Two lists: all_sslps and populations.
    """
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "haplotypes.json")
    all_sslps, populations = [], []
    with open(file_path, "r") as file:
        haplotype_file = json.load(file)
        populations = list(haplotype_file.keys())
        for _, pop in haplotype_file.items():
            for _, sslps in pop.items():
                all_sslps.extend((sslps))
    all_sslps = sorted(list(set(all_sslps)))
    return all_sslps, populations


def get_saved_results(request):
    """
        Returns:
            dict: The combinations dictionary containing the saved results.
        Summary:
            This function takes the combinations dictionary from the session, which contains the saved results. If the
            combinations dictionary is not empty, it returns the dictionary.
    """
    combinations = request.session.get('combinations', {})
    if combinations != {}:
        return combinations


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
            
def haplotype_uploader(request,population):
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
        population (str): A string containing the name of the population 
        that currently is viewed.

    Returns:
        django.http.HttpResponseRedirect: A redirect response object which 
        can be used to redirect the user to another page.
    """
    with open("haplotypes.json","r") as file:
        haplotypes = load(file)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file_in_memory = request.FILES['file'].read()
        try:
            df = xslx_parser(file_in_memory)
            new_population = json_parser(df)
            new_name = request.POST.get("new_population")
        except:
            messages.warning(request, f"Invalid file format. Population not added.")
            return redirect("data_editor",population=population)
        else:
            messages.success(request, f"Population {new_name} succesfully added.")
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
        elif "delete" in request.POST:
            if request.user.is_superuser:
                with open("haplotypes.json","r") as file:
                    haplos = load(file)
                del haplos[population]
                with open("haplotypes.json","w") as file:
                    file.write(dumps(haplos,indent=4))
                messages.success(request,f"Population: {population} succesfully deleted.")
                return redirect("data_editor",population=list(haplotypes.keys())[0])
                
        elif "new_population" in request.POST:
            if request.user.is_superuser:
                return haplotype_uploader(request,population)
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
