from django.shortcuts import  render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse 
import re
import markdown2
import random

from . import util

entrylist = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
#función principal que devuelve la entrada correspondiente o redirige a la página de error si la entrada no existe

def wiki(request, title):
    
    if title in entrylist:
        content = util.get_entry(title)

        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": markdown2.markdown(content)
            
        })
    else:
        return render(request, "encyclopedia/error.html", {
            'error': 'The requested page was not found or does not exist yet.'
        })


#función de búsqueda

def search(request):

    if request.method == 'POST':
        resultlist = [] 
        query = request.POST
        query = query['q']
        
        for page in entrylist:
            if re.search(query.lower(), page.lower()):  
                resultlist.append(page)

            if query.lower() == page.lower():
                return redirect(wiki, title=page)


        if len(resultlist) == 0:  #si la longitud de los resultados es igual a 0 entonces redirige a la página de error
            return render(request, "encyclopedia/error.html", {
                'error': f'No information about \'{query}\' in our Encyclopedia. '
            })

        

        return render(request, "encyclopedia/search.html", {
            'entries': resultlist
    })



#función para crear una nueva página

def new_page(request):
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title not in entrylist:
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("new_page"))
        else: 
            return render(request, "encyclopedia/new_page.html", {
            "exists": True
            })

    return render(request, "encyclopedia/new_page.html", {
        "exists": False
    })
        
#función para editar una entrada

def edit_page(request, title):
    content = util.get_entry(title)
    

    if request.method == "POST":
        content = request.POST.get('new')
        util.save_entry(title, content)
        return redirect(wiki, title=title)

    return render(request, "encyclopedia/edit_page.html", {
        'title': title,
        'content': content
    })

    
#función random

def random_page(request):

    entries = util.list_entries() 
    selected_page = random.choice(entries)
    content = util.get_entry(selected_page)
    return render(request, "encyclopedia/random_page.html", {
            "title": selected_page,
            "content": markdown2.markdown(content)
            
        })



        
