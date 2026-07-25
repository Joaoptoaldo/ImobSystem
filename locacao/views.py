from django.shortcuts import render, redirect
from django.db.models import Q

from locacao.models import Immobile, ImmobileImage
from locacao.forms import ClientForm, ImmobileForm, RegisterLocationForm

# Create your views here.
def list_location(request):
    """
    função que lista os imóveis disponíveis para locação
    """
    immobiles = Immobile.objects.filter(is_locate=False)
    context = {
        'immobiles': immobiles
    }
    return render(request, 'list_location.html', context)
  
  
def form_client(request):
    """
    função que cadastra um cliente
    """
    form = ClientForm()
    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')   
          
    return render(request, 'form_client.html', {'form': form})
  
  
def form_immobile(request):
    """
    função que cadastra um imóvel
    """
    form = ImmobileForm() 
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile')
            if files:
                for f in files:
                    ImmobileImage.objects.create(
                        immobile=immobile, 
                        image=f
                    )
            return redirect('list-location')   
    return render(request, 'form_immobile.html', {'form': form})



def form_location(request, id):
    """
    função que cadastra uma locação
    """
    get_locate = Immobile.objects.get(id=id)

    form = RegisterLocationForm()  
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate
            location_form.save()  
            
            immo = Immobile.objects.get(id=id)
            immo.is_locate = True 
            immo.save() 

            return redirect('list-location') 

    context = {'form': form, 'location': get_locate}
    return render(request, 'form_location.html', context)


def reports(request): 
    """
    função que gera relatórios de imóveis locados, 
    filtrando por cliente, tipo de imóvel, data de locação e status da locação
    """
    immobile = Immobile.objects.all()
    
    get_client = request.GET.get('client') 
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item') 

    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')
    print(get_dt_start, get_dt_end)

    if get_client:
        immobile = Immobile.objects.filter(
			Q(reg_location__client__name__icontains=get_client) | 
			Q(reg_location__client__email__icontains=get_client))
    
    if get_dt_start and get_dt_end:
        immobile = Immobile.objects.filter(
			reg_location__create_at__range=[get_dt_start,get_dt_end])

    if get_locate:
        immobile = Immobile.objects.filter(is_locate=get_locate)

    if get_type_item:
        immobile = Immobile.objects.filter(type_item=get_type_item)

    return render(request, 'reports.html', {'immobiles':immobile})
