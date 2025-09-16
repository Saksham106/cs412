from django.shortcuts import render

# Create your views here.
def show_form(request):
    template_name = 'formdata/form.html'
    return render(request, 'formdata/form.html')