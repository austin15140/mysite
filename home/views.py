from django.shortcuts import render
from datetime import datetime

def index(request):
    year = datetime.now().year
    c_name = 'tgthrFit'
    context = {'year': year, 'c_name': c_name}
    return render(request, 'home/index.html', context)