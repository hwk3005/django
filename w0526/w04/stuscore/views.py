from django.shortcuts import render
from stuscore.models import Stuscore

def list(request):
    qs = Stuscore.objects.all()
    context = {'list':qs}
    return render(request,'stuscore_list.html',context)
