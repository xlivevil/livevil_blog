from netdisk.models import Files
from django.shortcuts import render
from ibm_oss import get_buckets, delete_item, get_item, upload_large_file,


def home(request):
    files = Files.object.all()
    context = {'files': files}
    return render(request, 'files.html', context)
