from django.shortcuts import render,HttpResponse
import pandas as pd
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from .utils import haplotype
import json

def export_home_view(request):
    saved_results_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "files/saved_results.txt")
    with open(saved_results_path, "r") as file:
        saved_results = [[sorted([int(sslp) for sslp in data.split(";")[0].strip("[]").split(",")]),data.split(";")[1]] for data in file.readline().split(":")[:-1]]
    starting_header = ["position","population","SSLP-1","SSLP-2","SSLP-3","SSLP-4","Total likelihood permissive genotype"]
    repeating_header = ["chr4_1","chr4_2","chr10_1","chr10_2","probability(%)","permissive alleles","population incidence"]
    save_string = ""
    max_len = 0
    for sslp,population in saved_results:
        table_haplotype_filled, total_perc = haplotype(sslp, population)
        if table_haplotype_filled != 1:
            haplotype_table = table_haplotype_filled
            id = "-".join(map(str,sslp))
            entry_list = [id]+sslp
            entry_list.append(population)
            entry_list.append(total_perc)
            for entry in haplotype_table:
                entry_list += entry
            if len(entry_list) > max_len:
                max_len = len(entry_list) - len(starting_header)
            save_string += ";".join(map(str,entry_list)) + "\n"
    headers_needed = max_len//len(repeating_header)
    header = starting_header + repeating_header*headers_needed
    header_str = ";".join(header) + "\n"
    return_results = header_str + save_string
    content = return_results.replace(".",",")
    filename = "result.csv"
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response
        

def home_view(request):
    total_perc, title, saved_results, haplotype_table = "", "", [], []
    all_sslps, populations = list_of_sslps()

    if 'export_button' in request.POST:
        return export_home_view(request)

    elif 'save' in request.POST:
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "files/current_haplotypes.txt")
        with open(file_path, "r") as file:
            current = file.readline()
        saved_results_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "files/saved_results.txt")
        with open(saved_results_path, "a") as file:
            file.write(current)
        with open(saved_results_path, "r") as file:
            saved_results = file.readline().split(":")
    elif 'change_result_submit' in request.POST:
        saved_results = get_saved_results()
        chosen_result = request.POST.get('change_result_submit').split(';')
        table_haplotype_filled, total_perc_int = haplotype(json.loads(chosen_result[0]), chosen_result[1])
        haplotype_table = table_haplotype_filled
        total_perc = f'{total_perc_int:.1f}%'
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "files/current_haplotypes.txt")

        with open(file_path, "w") as file:
            file.write(f'{chosen_result[0]};{chosen_result[1]}:')
        title = f'{chosen_result[0]};{chosen_result[1]}:'

    elif "predict" in request.POST:
        saved_results = get_saved_results()
        SSLPs = request.POST.getlist('SSLP_value')
        region = request.POST.get('region')
        if "" not in SSLPs and region != "":
            SSLPs = sorted([int(i) for i in SSLPs])
            table_haplotype_filled, total_perc_int = haplotype(SSLPs, region)
            if table_haplotype_filled != 1:
                haplotype_table = table_haplotype_filled
                total_perc = f'{total_perc_int:.1f}%'
                file_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "files/current_haplotypes.txt")
                title=f'{SSLPs} {region}'
                with open(file_path, "w") as file:
                    file.write(f'{SSLPs};{region}:')
            else:
                title = "Current selection does not return results"

    return render(request, 'homepage.html', {
        'Title': title,
        'data': haplotype_table,
        'saved_results': saved_results,
        'chrom_lengths': all_sslps,
        'populations': populations,
        'likelihood': total_perc,

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


def get_saved_results():
    saved_results_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "files/saved_results.txt")
    with open(saved_results_path, "r") as file:
        saved_results = file.readline().split(':')
    return saved_results


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
