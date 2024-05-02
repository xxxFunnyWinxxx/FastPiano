from pathlib import Path
import logging

from django.shortcuts import render
from django.core.cache import cache
from django.http import FileResponse

from fastpiano.data_parser import get_music_list, get_pdf_from_file, get_random_file
from fastpiano.const import PURPOSE_OPTS, LEVEL_OPTS, SOURCE_OPTS

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def index(request):
    return render(request, "index.html")

def music_list(request):
    data = get_music_list()
    return render(request, "music_list.html", context={"data": data})

def play(request):
    return render(request, "play.html")

def show(request):
    file = request.GET.get("file")
    level = request.GET.get("level")
    purpose = request.GET.get("purpose")
    if file:
        pdf_file = get_pdf_from_file(file)
    elif level and purpose:
        pdf_file = get_pdf_from_file(get_random_file(purpose, level))
    else:
        logger.warning(f"Incorrect request file: {file}, purpose: {purpose}, level: {level}")
        index(request)
    return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')

def admin(request):
    return render(request, "admin.html", context={"purpose_opts": PURPOSE_OPTS, "level_opts": LEVEL_OPTS, "source_opts": SOURCE_OPTS})