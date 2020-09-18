from django.shortcuts import render
from django import forms
from collections import Counter
import random
from random import choice
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from django.contrib import messages
 
from . import util

class NewTasksForm(forms.Form):
    form = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'search', 'placeholder':'Search Encyclopedia'}))

class NewSearchForm(forms.Form):
    # query = forms.CharField(label="Search Encyclopedia")
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search Wiki', 
            'style': 'width:100%'}))

class EditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'id':'content', 'placeholder':'Content', 'class':'form-control', 'rows':'10'}))
    
class EditedForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'id':'content', 'placeholder':'Content', 'class':'form-control', 'rows':'10'}))

search_form = NewTasksForm()

def index(request):
    # if request.method == "POST":
    #     entries_found = []
    #     entries_all = util.list_entries()
    #     form = NewSearchForm(request.POST)
        
    #     if form.is_valid():
    #         input = form.cleaned_data["search"]
    #         for entry in entries_all:
    #             if input.lower() == entry.lower():
    #                 title = entry
    #                 entry = util.get_entry(title)
    #                 return HttpResponseRedirect(reverse("site", kwargs={'entry': input}))
    #             # Partial matches are displayed in a list
    #             if input.lower() in entry.lower():
    #                 entries_found.append(entry)
    #         # Return list of partial matches
    #         return render(request, "encyclopedia/index.html", {
    #             "results": entries_found,
    #             "input": input,
    #             "form": NewSearchForm()
    #         })
    #         site = util.get_entry(f"{input}")
    #         if site == None:
    #             return render(request, "encyclopedia/error.html")
    #         else:
    #             return HttpResponseRedirect(reverse("site", kwargs={'entry': input}))
    #     else:
    #         return render(request, "encyclopedia/index.html", {
    #             "entries": util.list_entries(),
    #             "form": form
    #         })
    # else:
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        test = util.get_entry(title)
        if test != None:
            messages.error(request, "The entry you are trying to create is already exists!!!")
            return render(request, "encyclopedia/create.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })
        else:
            return render(request, "encyclopedia/create.html", {
            "entries": util.save_entry(title, content)
        })
    else:
        title = ""
        content = ""
        return render(request, "encyclopedia/create.html", {
            "entries": util.list_entries()
        })

def edit(request, title):
    if request.method == "POST":
        edited_form = EditedForm(request.POST)
        if edited_form.is_valid():
            edited_content = edited_form.cleaned_data["content"]
            util.save_entry(title, edited_content)
            return HttpResponseRedirect(reverse("site", kwargs={"entry":title}))

    else:
        entry_content = util.get_entry(title)
        edit_form = EditForm(initial={"content":entry_content})
        return render(request, "encyclopedia/edit.html", {
            "search_form": search_form,
            "title": title,
            "edit_form": edit_form
        })
    
def site(request, entry):
    if util.get_entry(f"{entry}") == None:
        return render(request, "encyclopedia/error.html", {
            "entries": entry,
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "title": entry,
            "entries": markdown2.markdown(util.get_entry(f"{entry}")),
            "entry_raw": entry,
            "form": NewSearchForm()
        })

def randompage(request):
    entries = util.list_entries()
    random_page = choice(entries)
    return HttpResponseRedirect(reverse("site", kwargs={"entry":random_page}))
    # return render(request, "encyclopedia/randompage.html", {
    #     "entries":  random.choice(util.list_entries())
    # })

# Search for wiki entry
def search(request):
    if request.method == "POST":
        entries_found = []  #List of entries that match query
        entries_all = util.list_entries()  #All entries
        form = NewSearchForm(request.POST)  #Gets info from form
        # Check if form fields are valid
        if form.is_valid():
            # Get the query to search entries/pages
            query = form.cleaned_data["query"]
            # Check if any entries/pages match query
            # If exists, redirect to entry/page
            for entry in entries_all:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("site", args=[title]))
                # Partial matches are displayed in a list
                if query.lower() in entry.lower():
                    entries_found.append(entry)
            # Return list of partial matches
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "query": query,
                "form": NewSearchForm()
            })
    # Default values
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": NewSearchForm()
    })
