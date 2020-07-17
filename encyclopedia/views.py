from django.shortcuts import render

from . import util
from django.http import Http404
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):

    page = util.get_entry(title)

    if page == None:
        raise Http404("Wiki entry does not exist.")

    md = markdown.Markdown()
    page = md.convert(page)

    return render(request, "encyclopedia/wiki.html", {
        "page": page,
        "title": title
    })
