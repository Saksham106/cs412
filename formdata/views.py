from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_form(request):
    template_name = 'formdata/form.html'
    return render(request, 'formdata/form.html')

def submit(request):

    template_name = 'formdata/confirmation.html'
    print(request)

    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color': favorite_color,
        }

    return render(request, template_name=template_name, context=context)