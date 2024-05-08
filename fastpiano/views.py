import logging

from django.shortcuts import render
from django.core.cache import cache
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

from fastpiano.data_parser import get_music_list, get_pdf_from_file, get_random_file, append_data
from fastpiano.const import PURPOSE_OPTS, LEVEL_OPTS, DATA_DIR, PDF_DIR, PASSWORD


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
        logger.debug(f"File: {file}")
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
    return render(request, "admin.html", context={"purpose_opts": PURPOSE_OPTS, "level_opts": LEVEL_OPTS})

def add_music(request):
    if request.method == "POST":
        cache.clear()
        filename = None
        name = request.POST.get("name")
        author = request.POST.get("author")
        purpose = request.POST.get("purpose")
        level = request.POST.get("level")
        password = request.POST.get("password")

        if request.FILES['file']:
            file = request.FILES['file']
            if file.name.lower().endswith('.pdf'):
                source = 'pdf'
            else:
                source = 'data'

            if source == 'pdf':
                dir_to_load = PDF_DIR
            elif source == 'data':
                dir_to_load = DATA_DIR

        if password == PASSWORD:    
            fs = FileSystemStorage(location = dir_to_load)
            filename = fs.save(file.name, file)
        else: 
            context = {"message": "Неверный пароль!"}
            return render(request, "add_music.html", context)
        
        context = {"file": filename,
                    "author": author,
                    "name": name,
                    "purpose": purpose,
                    "level": level,
                    "source": source}

        if filename and name and author and purpose and level and source:
            append_data(filename, author, name, purpose, level, source)
            context["message"] = f"""Произведение успешно добавлено!
            Файл: {filename}, название: {name}, автор: {author}, навык {purpose}, уровень {level}"""
            return render(request, "add_music.html", context)
        else:
            context["message"] = """Одно из полей не было заполнено. Произведение не добавлено
            Файл: {filename}, название: {name}, автор: {author}, навык {purpose}, уровень {level}"""
            return render(request, "add_music.html", context)
    else:
        admin(request)