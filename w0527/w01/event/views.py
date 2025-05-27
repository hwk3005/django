from django.shortcuts import render
from event.models import Event
def list(request):
    qs = Event.objects.all()
    context = {'list':qs}
    return render(request,'event/list.html',context)
