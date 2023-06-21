from django.shortcuts import render
import pandas as pd
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from .utils import haplotype
import json


def home_view(request):
    total_perc, title, saved_results, haplotype_table = "", "", [], []
    all_sslps, populations = list_of_sslps()

    if 'export_button' in request.POST:
        try:
            response = downloadfile(request, "tempfile")
            return response
        except FileNotFoundError:
            message = 'No results to export'
    elif 'save' in request.POST:
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "files/current_haplotypes.txt")
        with open(file_path, "r") as file:
            current = file.readline()
        saved_results_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "files/saved_results.txt")

        with open(saved_results_path, "r") as file:
            saved_results_check = file.readline().split(":")
        if f'{current}:' not in saved_results_check:
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
    print(saved_results)
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
