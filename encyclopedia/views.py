from django.shortcuts import render
from django.urls import reverse
from . import util
from django.http import Http404, HttpResponseRedirect
import markdown
from django.views.decorators.http import require_http_methods


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

@require_http_methods(['POST'])
def search(request):

    # if request.method == 'POST':
        text = request.POST['q']
        return HttpResponseRedirect(reverse('wiki', args=(text,)))
