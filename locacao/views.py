from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from locacao.forms import ClientForm, ImmobileForm, RegisterLocationForm
from locacao.models import Immobile
from locacao.services import ClientService, ImmobileService, LocationService

ITEMS_PER_PAGE = 20


def _paginate(queryset, request):
    """
    Helper para paginar uma queryset e tratar parâmetros de página inválidos
    """ 
    paginator = Paginator(queryset, ITEMS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


# VIEWS - CLIENTE

@login_required
def form_client(request):
    """
    View para cadastrar um cliente.
    """
    form = ClientForm()

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            ClientService.create_client(form)
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('list-location')

    return render(request, 'form_client.html', {'form': form})


@login_required
def list_client(request):
    """
    View que lista todos os clientes cadastrados.
    """
    clients = _paginate(ClientService.get_all_clients(), request)
    return render(request, 'list_client.html', {'clients': clients})


@login_required
def update_client(request, id):
    """
    View para editar um cliente.
    """
    get_client = ClientService.get_client_by_id(id)
    form = ClientForm(instance=get_client)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=get_client)
        if form.is_valid():
            ClientService.update_client(form, id)
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('list-client')

    return render(request, 'form_client.html', {
        'form': form,
        'client': get_client,
        'is_update': True
    })


@login_required
def delete_client(request, id):
    """
    View para excluir um cliente.
    """
    get_client = ClientService.get_client_by_id(id)
    if request.method == 'POST':
        ClientService.delete_client(id)
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('list-client')

    return render(request, 'confirm_delete.html', {'client': get_client})



# VIEWS - IMÓVEL

@login_required
def form_immobile(request):
    """
    View para cadastrar um imóvel.
    """
    form = ImmobileForm()
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            ImmobileService.create_immobile(form, request.FILES.getlist('immobile'))
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('list-location')
    return render(request, 'form_immobile.html', {'form': form})


@login_required
def list_immobile(request):
    """
    View que lista todos os imóveis cadastrados (para administração).
    Permite filtrar por tipo de imóvel.
    """
    immobiles = ImmobileService.get_all_immobiles()

    type_item = request.GET.get('type_item')
    if type_item:
        immobiles = immobiles.filter(type_item=type_item)

    immobiles = _paginate(immobiles, request)
    return render(request, 'list_immobile.html', {'immobiles': immobiles})


@login_required
def update_immobile(request, id):
    """
    View para editar um imóvel.
    """
    get_immobile = ImmobileService.get_immobile_by_id(id)
    form = ImmobileForm(instance=get_immobile)

    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES, instance=get_immobile)
        if form.is_valid():
            ImmobileService.update_immobile(form, request.FILES.getlist('immobile'), id)
            messages.success(request, 'Imóvel atualizado com sucesso!')
            return redirect('list-immobile')

    return render(request, 'form_immobile.html', {
        'form': form,
        'immobile': get_immobile,
        'is_update': True
    })


@login_required
def delete_immobile(request, id):
    """
    View para excluir um imóvel.
    """
    get_immobile = ImmobileService.get_immobile_by_id(id)
    if request.method == 'POST':
        ImmobileService.delete_immobile(id)
        messages.success(request, 'Imóvel excluído com sucesso!')
        return redirect('list-immobile')

    return render(request, 'confirm_delete_immobile.html', {
        'immobile': get_immobile
    })



# VIEWS - LOCAÇÃO

@login_required
def list_location(request):
    """
    View que lista os imóveis disponíveis para locação.
    """
    immobiles = _paginate(LocationService.get_available_immobiles(), request)
    context = {'immobiles': immobiles}
    return render(request, 'list_location.html', context)


@login_required
def list_location_register(request):
    """
    View que lista todas as locações registradas.
    """
    locations = _paginate(LocationService.get_registered_locations(), request)
    return render(request, 'list_location_register.html', {
        'locations': locations
    })


@login_required
@transaction.atomic
def finish_location(request, id):
    """
    View para encerrar uma locação ativa.
    GET: renderiza template de confirmação
    POST: executa o encerramento e redireciona
    Retorna 404 se a locação não existir ou já estiver encerrada.
    """
    from locacao.models import RegisterLocation

    location = get_object_or_404(
        RegisterLocation, id=id, dt_finished__isnull=True
    )

    if request.method == 'POST':
        LocationService.finish_location(id)
        messages.success(
            request,
            f'Locação do imóvel {location.immobile.code} encerrada com sucesso!'
        )
        return redirect('list-locations')

    return render(request, 'confirm_finish_location.html', {
        'location': location
    })


@login_required
@transaction.atomic
def form_location(request, id):
    """
    View para cadastrar uma locação.
    Retorna 404 se o imóvel não existir ou já estiver locado.
    """
    immobile = get_object_or_404(Immobile, id=id, is_locate=False)

    form = RegisterLocationForm()
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            LocationService.register_location(form, id)
            messages.success(
                request,
                f'Locação do imóvel {immobile.code} registrada com sucesso!'
            )
            return redirect('list-location')

    context = {'form': form, 'location': immobile}
    return render(request, 'form_location.html', context)



# VIEWS - RELATÓRIOS

@login_required
def reports(request):
    """
    View que gera relatórios de imóveis locados,
    filtrando por cliente, tipo de imóvel, data de locação e status.
    """
    filters = {
        'client': request.GET.get('client'),
        'is_locate': request.GET.get('is_locate'),
        'type_item': request.GET.get('type_item'),
        'dt_start': request.GET.get('dt_start'),
        'dt_end': request.GET.get('dt_end'),
    }
    
    immobiles = LocationService.get_report_data(filters)
    immobiles = _paginate(immobiles, request)
    return render(request, 'reports.html', {'immobiles': immobiles})
