import random
import markdown2
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from django.urls import reverse

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    if request.GET.get('q', '') != '':
        return search(request)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query = request.GET.get('q', '')
    if query in util.list_entries():
        return article(request, query)
    else:
        matches = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                matches.append(entry)
        return render(request, "encyclopedia/matches.html", {
            "entries": matches
        })

def edit_page(request, article):
    if article in util.list_entries():
        if request.method == "POST":
            form = EditPageForm(request.POST)

            if form.is_valid():
                content = form.cleaned_data["content"]
                util.save_entry(article, content)
                return HttpResponseRedirect(reverse("article", kwargs={"article": article}))
        
        else:
            return render(request, "encyclopedia/edit-page.html", {
                "article": article,
                "form": EditPageForm(initial={"content": util.get_entry(article)})
            })
    else:
        return render(request, "encyclopedia/not-found.html", {
            "article": article
        })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]

            if title in util.list_entries():
                messages.add_message(request, messages.ERROR, f"page with title {title} already exists")
                return render(request, "encyclopedia/new-page.html", {
                    "form" : NewPageForm(request.POST)
                })

            else:
                content = form.cleaned_data["content"]

                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("article", kwargs={"article": title}))

    else:
        return render(request, "encyclopedia/new-page.html", {
            "form" : NewPageForm()
        })

def random_page(request):
    return HttpResponseRedirect(reverse("article", kwargs={"article": random.choice(util.list_entries())}))

def article(request, article):
    if request.GET.get('q', '') != '':
        return search(request)

    if article in util.list_entries():
        content = markdown2.markdown(util.get_entry(article))
        return render(request, "encyclopedia/article.html", {
            "article": article,
            "content": content
        })

    else:
        return render(request, "encyclopedia/not-found.html", {
            "article": article
        })
