from pathlib import Path
import logging

from django.shortcuts import render
from django.core.cache import cache
from django.http import FileResponse

from fastpiano.data_parser import get_music_list, get_pdf_from_file, get_random_file, append_data
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
    return render(request, "play.html", context={"purpose_opts": PURPOSE_OPTS, "level_opts": LEVEL_OPTS})

def show(request):
    if request.method == "POST":
        cache.clear()
        file = request.POST.get("file")
        level = request.POST.get("level")
        purpose = request.POST.get("purpose")
    else:
        file = request.GET.get("file")
        level = request.GET.get("level")
        purpose = request.GET.get("purpose")

    if file:
        pdf_file = get_pdf_from_file(file)
    elif level and purpose:
        logger.debug(f"Purpose: {purpose}, level: {level}")
        pdf_file = get_pdf_from_file(get_random_file(purpose, level))
        if pdf_file == None:
            return render(request, "music_not_found.html", context = {"params":{"purpose": purpose, "level": level}})
    else:
        logger.warning(f"Incorrect request file: {file}, purpose: {purpose}, level: {level}")
        index(request)
    return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')

def admin(request):
    return render(request, "admin.html", context={"purpose_opts": PURPOSE_OPTS, "level_opts": LEVEL_OPTS, "source_opts": SOURCE_OPTS})

def add_music(request):
    if request.method == "POST":
        cache.clear()
        file = request.POST.get("file")
        name = request.POST.get("name")
        author = request.POST.get("author")
        purpose = request.POST.get("purpose")
        level = request.POST.get("level")
        source = request.POST.get("source")
        context = {"file": file,
                    "author": author,
                    "name": name,
                    "purpose": purpose,
                    "level": level,
                    "source": source}
        if file and name and author and purpose and level and source:
            append_data(file, author, name, purpose, level, source)
            context["message"] = "Произведение успешно добавлено!"
            return render(request, "add_music.html", context)
        else:
            context["message"] = "Одно из полей не было заполнено. Произведение не добавлено"
            return render(request, "add_music.html", context)
    else:
        admin(request)