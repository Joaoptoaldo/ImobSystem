from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from locacao.models import Immobile, ImmobileImage, RegisterLocation
from locacao.forms import ClientForm, ImmobileForm, RegisterLocationForm

# Create your views here.
@login_required
def list_location(request):
    """
    função que lista os imóveis disponíveis para locação
    """
    immobiles = Immobile.objects.filter(is_locate=False)
    context = {
        'immobiles': immobiles
    }
    return render(request, 'list_location.html', context)


@login_required
def form_client(request):
    """
    função que cadastra um cliente
    """
    form = ClientForm()

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('list-location')

    return render(request, 'form_client.html', {'form': form})


@login_required
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
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('list-location')
    return render(request, 'form_immobile.html', {'form': form})


@login_required
@transaction.atomic
def form_location(request, id):
    """
    função que cadastra uma locação
    """
    get_locate = get_object_or_404(Immobile, id=id, is_locate=False)

    form = RegisterLocationForm()
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate
            location_form.save()

            get_locate.is_locate = True
            get_locate.save()

            messages.success(request, f'Locação do imóvel {get_locate.code} registrada com sucesso!')
            return redirect('list-location')

    context = {'form': form, 'location': get_locate}
    return render(request, 'form_location.html', context)


@login_required
def reports(request):
    """
    função que gera relatórios de imóveis locados,
    filtrando por cliente, tipo de imóvel, data de locação e status da locação
    """
    immobiles = Immobile.objects.prefetch_related(
        Prefetch('reg_location', queryset=RegisterLocation.objects.select_related('client'))
    ).all()

    get_client = request.GET.get('client')
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item')

    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')

    location_filters = Q()
    if get_client:
        location_filters &= (
            Q(reg_location__client__name__icontains=get_client) |
            Q(reg_location__client__email__icontains=get_client)
        )

    if get_dt_start and get_dt_end:
        # Filtra locações cujo período (dt_start a dt_end) tenha interseção com o intervalo informado
        location_filters &= Q(reg_location__dt_start__date__lte=get_dt_end) & Q(reg_location__dt_end__date__gte=get_dt_start)

    if location_filters:
        immobiles = immobiles.filter(location_filters)

    if get_locate is not None and get_locate != '':
        immobiles = immobiles.filter(is_locate=(get_locate.lower() == 'true'))

    if get_type_item:
        immobiles = immobiles.filter(type_item=get_type_item)

    return render(request, 'reports.html', {'immobiles': immobiles.distinct()})
