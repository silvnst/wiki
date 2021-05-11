from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
from random import choice

def index(request):

    entries = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, entry):

    entries = util.list_entries()
    
    if entry.lower() in [x.lower() for x in entries]:

        md = util.get_entry(entry)

        html = markdown2.markdown(md)

        return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "html": html
        })

    else:
        return render(request, "encyclopedia/error.html", {
        "entry": entry
        })    
 
def new(request):
    if request.method == "POST":

        form = request.POST

        formTitle = form['entry-title']

        entries = util.list_entries()

        if formTitle.lower() not in [x.lower() for x in entries]:

            util.save_entry(formTitle, form['entry-text'])

            return HttpResponseRedirect('/wiki/' + formTitle)

        else:
            return render(request, "encyclopedia/new.html", {
                "error_massage": 'This entry already exists!'
            })

    else:
        return render(request, "encyclopedia/new.html")

def edit(request, entry):

    entries = util.list_entries()

    if request.method == "POST":

        form = request.POST

        formTitle = form['entry-title']

        util.save_entry(formTitle, form['entry-text'])

        return HttpResponseRedirect('/wiki/' + formTitle)
        
    else:
        if entry in entries:

            content = util.get_entry(entry)

            return render(request, "encyclopedia/edit.html", {
                    "entry": entry,
                    "content":content
                })

        else:
            return render(request, "encyclopedia/index.html", {
                    "entry": entry,
                })

def random(request):

    entries = util.list_entries()

    random_entry = choice(entries)
    
    return HttpResponseRedirect('/wiki/' + random_entry)

def search(request):

    entries = util.list_entries()

    query = request.GET['q']

    if query in entries:
        
        return HttpResponseRedirect('/wiki/' + query)
    
    else:

        que = []

        for entry in entries:

            if query.lower() in entry.lower():

                que.append(entry)
        
        if que:
            return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "results": que
                })
        
        else: 
            return render(request, "encyclopedia/index.html", {
                    "entries": entries,
                    "error_massage": 'Unfortunately we didn\'t found what you searched for.'
                })