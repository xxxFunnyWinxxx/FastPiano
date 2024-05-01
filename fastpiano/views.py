from pathlib import Path

from django.shortcuts import render
from django.core.cache import cache

from fastpiano.const import SOURCE_FILE
from fastpiano.data_parser import get_music_list


def index(request):
    return render(request, "index.html")

def music_list(request):
    data = get_music_list(SOURCE_FILE)
    return render(request, "music_list.html", context={"data": data})