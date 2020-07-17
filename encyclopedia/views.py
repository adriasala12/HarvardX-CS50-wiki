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

    title = request.POST['q']
    return HttpResponseRedirect(reverse('wiki', args=(title,)))


def new(request):

    if request.method == 'POST':
        existing_titles = util.list_entries()

        title = request.POST['title']
        text = f"""# {title}
{request.POST['text']}"""

        if title in existing_titles:
            context = {
                "message": "There is already one entry with this title.",
                "title": title,
                "text": request.POST['text']
            }

            return render(request, "encyclopedia/new.html", context)

        util.save_entry(title, text)

        return HttpResponseRedirect(reverse('wiki', args=(title,)))

    return render(request, "encyclopedia/new.html")


def edit(request, title):

    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('wiki', args=(title,)))

    context = {
        "title": title,
        "content": util.get_entry(title)
    }

    return render(request, "encyclopedia/edit.html", context)
