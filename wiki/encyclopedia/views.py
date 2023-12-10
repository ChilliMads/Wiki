from django import forms
from . import util
from django.shortcuts import render, redirect
import random
import markdown2

class Searchbar(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


def index(request): #index side functionality
    entries = util.list_entries()
    return render(request, 'encyclopedia/index.html', {'entries': entries, 'search':Searchbar()})


def entry(request, title): #entry side functionality
    entry_content = util.get_entry(title)  # Gets the content of the entry with the title 
    
    # we check if the entry is not None
    if entry_content is not None: 
        html_content = markdown2.markdown(entry_content) 

        return render(request, 'encyclopedia/entry.html', {'title': title, 'content': html_content}) #In this linje we return the entry page with the title and the content
    else:
        return render(request, 'encyclopedia/error_Message.html', {'message': 'Page not found'}) #Here we reutrn the error page if the entry is not found, with an erro message "page not found"


# Search functionality - The search function is used to search for an entry in the encyclopedia
def search(request): 
    query = request.GET.get('q', '').strip()    # We get the query from the search bar                                
    
    # We check if the query is not empty if it is we redirect to the index page
    if query: 
        entry_content = util.get_entry(query)
        if entry_content:
            return redirect('entry', title=query)
        else:
            entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "entries": entries
            })
    else:
        return redirect('index')

# This create function is used to creating a new entry in the encyclopedia and checks if the entry already exists
def create(request):
    # We check if the request is a POST request and if it is we get the title and content from the form. 
    if request.method == 'POST': 
        title = request.POST['title'] 
        content = request.POST['content']
        existing_entry = util.get_entry(title)
        if existing_entry: #Here we check if entry already exists
            return render(request, 'encyclopedia/error_Message.html', {'message': 'Entry already exists'}) #If the entry does we return an error message
        else:
            util.save_entry(title, content) #If the entry does not exist we save the entry
            return redirect('entry', title=title)
    else:
        return render(request, 'encyclopedia/create_entry.html')
    

# Edit a entry wih ny contekst 
def edit(request, title): 
    if request.method == 'POST':
        new_content = request.POST['content']
        util.save_entry(title, new_content)
        return redirect('entry', title=title)
    else:
        existing_content = util.get_entry(title)
        return render(request, 'encyclopedia/edit_entry.html', {'title': title, 'content': existing_content})
# This functionality is used to edit an existing entry in the encyclopedia

#Chooses a random page from the encyclopedia
def random_page(request): 
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect('entry', title=random_title)
    else:
        return render(request, 'encyclopedia/error_Message.html', {'message': 'No entries available'})