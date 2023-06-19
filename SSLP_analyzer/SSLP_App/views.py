from django.shortcuts import render
import pandas as pd
from pathlib import Path
import os.path
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes


def home_view(request):
    print(request.POST)
    data = []
    data1 = [
        ['4A161', '4B163', '10A166', '10A166', 92.034, 1, 19.121],
        ['4A161', '4A163', '10A166', '10A166', 2.518, 2, 0.523],
        ['4B161', '4B163', '10A166', '10A166', 1.643, 0, 0.341],
        ['4A161', '4B163', '10A166', '10A166H', 1.283, 2, 0.266],
        ['4B163', '4A166', '10B161T', '10A166', 1.104, 0, 0.229],
        ['4B163', '4A166H', '10B161T', '10A166', 0.978, 1, 0.203],
        ['4B163', '4B166', '10A166', '10B161T', 0.251, 0, 0.052],
        ['4B161', '4A163', '10A166', '10A166', 0.045, 1, 0.009],
        ['4A161', '4A163', '10A166', '10A166H', 0.035, 3, 0.007],
        ['4A163', '4A166', '10B161T', '10A166', 0.030, 1, 0.006],
        ['4A163', '4A166H', '10B161T', '10A166', 0.027, 2, 0.006],
        ['4B161', '4B163', '10A166H', '10A166', 0.023, 1, 0.005],
        ['4B163', '4A166', '10B161T', '10A166H', 0.008, 1, 0.002],
        ['4A163', '4B166', '10B161T', '10A166', 0.007, 1, 0.001],
        ['4B163', '4A166H', '10B161T', '10A166H', 0.007, 2, 0.001],
        ['4A161', '4B163', '10A166H', '10A166H', 0.004, 3, 0.001],
        ['4B163', '4B166', '10B161T', '10A166H', 0.002, 1, 0.000],
        ['4B161', '4A163', '10A166H', '10A166', 0.001, 2, 0.000],
        ['4A163', '4A166', '10B161T', '10A166H', 0.000, 2, 0.000],
        ['4A163', '4A166H', '10B161T', '10A166H', 0.000, 3, 0.000],
        ['4A161', '4A163', '10A166H', '10A166H', 0.000, 4, 0.000],
        ['4B161', '4B163', '10A166H', '10A166H', 0.000, 2, 0.000],
        ['4A163', '4B166', '10A166H', '10B161T', 0.000, 2, 0.000],
        ['4A163', '4B161', '10A166H', '10A166H', 0.000, 2, 0.000]]

    if request.POST.get('export_button'):
        try:
            response = downloadfile(request, "tempfile")
            return response
        except FileNotFoundError:
            message = 'No results to export'
    if request.POST.get('save'):
        return render(request, 'homepage.html', {
            'data': data1,
            'saved_results': ['result 1', 'result 2', 'result 3']
        })
    if request.POST.get('change_result_submit'):
        return render(request, 'homepage.html', {
            'data': data1,
            'saved_results': ['result 1', 'result 2']
        })
    return render(request, 'homepage.html', {
        'data': data,
        'saved_results': ['result 1', 'result 2']
    })


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
