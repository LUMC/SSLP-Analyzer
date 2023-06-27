from django.shortcuts import render, HttpResponse
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from .utils import haplotype
import json
import re
from django.contrib import messages


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


def data_editor_view(request):
    return render(request, 'editpage.html')

