from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Max, Q

from final.models import Location
from sightings.forms import LocationForm
from sightings.forms import AddForm

def show(request):
    locations = Location.objects.all()
    context = {
            'locations':locations
            }
    return render(request,'sightings/show.html',context)

def detail(request,Unique_Squirrel_ID):
    squirrel = Location.objects.get(Unique_Squirrel_ID = Unique_Squirrel_ID)
    form= LocationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({})

    context = {
           'form':form
            }
    return render(request, 'sightings/detail.html',context)


def add_sightings(request):
    addform = AddForm(request.POST)
    if request.method == 'POST':
        if addform.is_valid():
            addform.save()
            return JsonResponse({})
        else:
            return JsonResponse({'Errors':addform.errors}, status=400)
    
    context = {
            'addform': addform
            }
    return render(request, 'sightings/add_sightings.html',context)


def stats(request):
    total_sightings = Location.objects.aggregate(Count('Unique_Squirrel_ID'))
    age_count = Location.objects.values('Age').annotate(Count('Age'))
    running = Location.objects.filter(Running=True).annotate(Count('Running'))
    latest_sighting = Location.objects.aggregate(Max('Date'))
    fur_color = Location.objects.values('Primary_Fur').annotate(Count('Primary_Fur'))
    context = {
            'Total Sightings': total_sightings,
            'Age count': age_count,
            'Latest sighting': latest_sighting,
            'Fur color count': fur_color,
            'Running count': running,
            }
    return render(request, 'sightings/stats.html', context)
