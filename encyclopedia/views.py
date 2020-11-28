from django.shortcuts import render
from django.shortcuts import HttpResponse
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util 
import markdown, random

# Class to create forms
class formNewEntry(forms.Form):
    title_entry = forms.CharField(label="Title:", max_length=30)
    title_entry.widget.attrs.update({"class":"new-entry-fields"})
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":10, "class":"new-entry-fields"}))

# Class to create form for the "editPage" functionality
class formEditEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":10, "class":"new-entry-fields"}))

# Outer method use by two funcionalities
def displayPageFromMarkdown (request, page):
    print(page)
    mdPage = util.get_entry(page)
    #print(mdPage)
    htmlFromMd = markdown.markdown(mdPage)
    #print(htmlFromMd)
    return render(request, "encyclopedia/entry.html", {
    'title': page,
    'entry': htmlFromMd
    })

# Outer method, in retrieves data from a specific entry
def retrieveContentEntry(pageName):
    contentOfEntry = None
    listOfPages = util.list_entries()
    for page in listOfPages:
        if page.lower() == pageName.lower():
            contentOfEntry = util.get_entry(page)


    return contentOfEntry

# First page of the wiki
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Get the requested page by URL
def getPage(request, pageName):
    listOfPages = util.list_entries()
    for page in listOfPages:
        if page.lower() == pageName.lower():
            # Call to outer method.
            return displayPageFromMarkdown(request, page)

    titleOfError= "404 Error"
    bodyOfError= "Error 404: page not found"
    return render(request, "encyclopedia/layoutError.html", {
        "title": titleOfError,
        "body": bodyOfError
    })

# Search for a specific page
def searchForEntry(request):
    # The request representation is: <QueryDict: {'q': ['key']}>
    pageToSearch = request.GET['q']
    listSimilarEntries = []
    listOfPages = util.list_entries()
    for page in listOfPages:
        if page.lower() == pageToSearch.lower():
            return displayPageFromMarkdown(request, page)

    for page in listOfPages:
        if pageToSearch.lower() in page.lower():
            listSimilarEntries.append(page)

    if not listSimilarEntries:
        messages.error(request, "Sorry, the page you are looking for doesn't exists.")
        return render(request, "encyclopedia/searchresult.html",{
            "entries":listSimilarEntries
        })
    else:
        return render(request, "encyclopedia/searchresult.html",{
            "entries":listSimilarEntries
        })

# This method supports POST-GET. 
# POST: it receives the request from the user
# GET: displays form to be fill by the user
def newEntry(request):
    if request.method == 'POST':
        form = formNewEntry(request.POST)
        if form.is_valid():
            entryPostRequest = request.POST
            # To get value from keys => dict.get('key')
            # <QueryDict: 'title_entry': ['example'], 'content': ['example']}>
            
            # Check if entry already exits
            actualEntry = retrieveContentEntry(entryPostRequest.get('title_entry'))
            if not actualEntry:
                titleNewEntry = entryPostRequest.get('title_entry')
                contentNewEntry = entryPostRequest.get('content')
                util.save_entry(titleNewEntry, contentNewEntry)
                return HttpResponseRedirect(reverse('index'))
            else:
                # messages.add_message(request, messages.ERROR, 'Page already exits')
                # or messages.error(request, 'An unexpected error occured.')
                messages.error(request, 'Page already exists, please choose another title.')
                return render(request, "encyclopedia/addentry.html", {
                    "form": form
                })
        else:
            return render(request, "encyclopedia/addentry.html", {
            "form": form
            })

    else:
        return render(request, "encyclopedia/addentry.html", {
        "form": formNewEntry()
        })

# This method supports POST-GET
# POST: receive request from user
# GET: display form to the user
def editEntry(request, pageName):
    if request.method == 'POST':
        # Create a form from the request in order to validate it
        form = formEditEntry(request.POST)
        if form.is_valid():
            editPostRequest = request.POST
            newContentEntry = editPostRequest.get('content')
            util.save_entry(pageName, newContentEntry)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'encyclopedia/editentry.html', {
                'title': pageName,
                'form':form
            })
    else:
        # Validation, if the page the user is requesting to edit doesn't exists,
        # display an error. Otherwise, return form.
        entryContentMb = retrieveContentEntry(pageName)
        if not entryContentMb:
            titleOfError= "404 Error"
            bodyOfError= "Error 404: page not found"
            return render(request, "encyclopedia/layoutError.html", {
            "title": titleOfError,
            "body": bodyOfError
            })
        else:
            return render(request, 'encyclopedia/editentry.html',{
                'title' : pageName,
                'form': formEditEntry(initial = {'content': entryContentMb})
            })

# Method to display a random entry
def getRandomEntry(request):
    listOfPages = util.list_entries()
    countElements = (len(listOfPages) - 1)
    rdmIndex = random.randint(0,countElements)
    entryName = listOfPages[rdmIndex]
    return displayPageFromMarkdown(request, entryName)
