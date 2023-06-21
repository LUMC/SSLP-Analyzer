from django.shortcuts import render
import pandas as pd
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from .utils import haplotype
import json
import re

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
        last_result = request.session.get('last_result')
        combinations = request.session.get('combinations', '')
        if last_result not in combinations:
            combinations += last_result
            request.session["combinations"] = combinations
    elif 'change_result_submit' in request.POST:
        saved_results = get_saved_results(request)
        chosen_result = request.POST.get('change_result_submit').split(';')
        int_list = [int(num) for num in re.findall(r'\d+', chosen_result[0])]
        table_haplotype_filled, total_perc_int = haplotype(sorted(int_list), chosen_result[1]) 
        haplotype_table = table_haplotype_filled
        total_perc = f'{total_perc_int:.1f}%'
        combinations = request.session.get('combinations', '')
        title = f'{chosen_result[0]};{chosen_result[1]}:'

    elif "predict" in request.POST:
        saved_results = get_saved_results(request)
        SSLPs = request.POST.getlist('SSLP_value')
        region = request.POST.get('region')
        last_result = request.session.get('last_result', '')
        last_result =f'{SSLPs};{region}:' 
        request.session["last_result"] = last_result
        if "" not in SSLPs and region != "":
            SSLPs = sorted([int(i) for i in SSLPs])
            table_haplotype_filled, total_perc_int = haplotype(SSLPs, region)
            if table_haplotype_filled != 1:
                haplotype_table = table_haplotype_filled
                total_perc = f'{total_perc_int:.1f}%'
                title=f'{SSLPs} {region}'
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


def get_saved_results(request):
    combinations = request.session.get('combinations', '')
    last_result = request.session.get('last_result', '')
    if combinations != "":
        saved_results = combinations.split(':')
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
