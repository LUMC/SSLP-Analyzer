from django.shortcuts import render, HttpResponse
import pandas as pd
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from .utils import haplotype
import json
import re


def check_SSLP(data, new_SSLP):
    for key in data:
        if new_SSLP == data[key]['SSLPS']:
            return False
    return True

def get_new_key(dict_data, base_name):
    i = 2
    new_name = base_name
    while new_name in dict_data:
        new_name = f"{base_name}({i})"
        i += 1
    return new_name


def export_home_view(request):
    saved_results_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "files/saved_results.txt")
    with open(saved_results_path, "r") as file:
        saved_results = [[sorted(
            [int(sslp) for sslp in data.split(";")[0].strip("[]").split(",")]),
            data.split(";")[1]] for data in
            file.readline().split(":")[:-1]]
    starting_header = ["position", "population", "SSLP-1", "SSLP-2", "SSLP-3",
                       "SSLP-4", "Total likelihood permissive genotype"]
    repeating_header = ["chr4_1", "chr4_2", "chr10_1", "chr10_2",
                        "probability(%)", "permissive alleles",
                        "population incidence"]
    save_string = ""
    max_len = 0
    for sslp, population in saved_results:
        table_haplotype_filled, total_perc = haplotype(sslp, population)
        if table_haplotype_filled != 1:
            haplotype_table = table_haplotype_filled
            id = "-".join(map(str, sslp))
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
    request.session["ids"] = ""
    switch_title = False
    total_perc, title, saved_results, haplotype_table = "", "", [], []
    all_sslps, populations = list_of_sslps()

    if 'export_button' in request.POST:
        return export_home_view(request)

    elif 'name_save' in request.POST:
        name_result = request.POST.get("name_result")
        last_result = request.session.get('last_result', {})
        combinations = request.session.get('combinations', {})
        key = list(last_result.keys())[0]
        value = last_result[key]
        if name_result in list(combinations.keys()):
            name_result = get_new_key(combinations, name_result)
        combinations[name_result] = value
        request.session["combinations"] = combinations
        table_haplotype_filled, total_perc_int = haplotype(
            sorted(value["SSLPS"]),
            value["Population"])
        haplotype_table = table_haplotype_filled
        total_perc = f'{total_perc_int:.1f}%'
        title = f'{name_result}'
    elif 'change_result_submit' in request.POST:
        chosen_result = request.POST.get('change_result_submit')
        combinations = request.session.get('combinations', {})
        chosen_result_dict = combinations[str(chosen_result)]
        table_haplotype_filled, total_perc_int = haplotype(
            sorted(chosen_result_dict["SSLPS"]),
            chosen_result_dict["Population"])
        title = f'{chosen_result[0]}'
        if table_haplotype_filled == 1 and total_perc_int == 1:
            switch_title = True
            title = "Current selection does not return results"
        haplotype_table = table_haplotype_filled
        total_perc = f'{total_perc_int:.1f}%'
        title = f'{chosen_result}' 
        request.session["last_result"] = {chosen_result:chosen_result_dict} 

    elif "predict" in request.POST:
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
    elif "Upload" in request.POST:
        input_data_file = str(request.FILES['upload'].read())
        input_data_list = input_data_file.split("\\r\\n")
        population_fromfile = input_data_list[1].split(';')[5]
        all_items, all_ids = "", ""
        for line in input_data_list[1:-1]:
            items = line.split(';')[:-1]
            all_ids = f'{all_ids};{items[0]}'
            all_items = f'{all_items}:{[int(x) for x in items[1:]]};{population_fromfile}'

        table, total_like = haplotype(sorted([int(x) for x in items[1:]]),
                                      population_fromfile)
        haplotype_table = table
        title = f'{items[0]}: {items[1:]} {population_fromfile}'
        total_perc = f'{total_like:.1f}%'
        request.session["combinations"] = "-"
        request.session["combinations"] = all_items[1:]
        request.session["ids"] = all_ids.split(';')

    return render(request, 'homepage.html', {
        'Title': title,
        'data': haplotype_table,
        'saved_results': get_saved_results(request),
        'chrom_lengths': all_sslps,
        'populations': populations,
        'likelihood': total_perc,
        'ids': request.session["ids"],
        'switch_title': switch_title
    })


def list_of_sslps():
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "files/haplotypes.json")
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
    combinations = request.session.get('combinations', {})
    if combinations != {}:
        return combinations


def downloadfile(request, filename):
    base_dir = Path(__file__).resolve().parent.parent
    filepath = str(base_dir) + '\\Files\\' + filename
    thefile = filepath
    filename = os.path.basename(thefile)
    chunk_size = 8192
    response = StreamingHttpResponse(
        FileWrapper(open(thefile, 'rb'), chunk_size),
        content_type=mimetypes.guess_type(thefile)[0])
    response['Content-length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response


def data_editor_view(request):
    return render(request, 'editpage.html')


def feed_view(request):
    return render(request, 'login.html')