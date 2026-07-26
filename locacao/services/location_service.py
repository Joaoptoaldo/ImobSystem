from django.db.models import Q, Prefetch
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404

from locacao.models import Immobile, RegisterLocation


class LocationService:
    """
    Serviço responsável por toda a lógica de negócio relacionada a Locações
    """

    @staticmethod
    def get_available_immobiles():
        """
        Retorna imóveis disponíveis para locação com imagens pré-carregadas
        """
        return Immobile.objects.filter(is_locate=False).prefetch_related('immobile_images')

    @staticmethod
    def get_registered_locations():
        """
        Retorna todas as locações registradas com os dados
        de cliente e imóvel pré-carregados.
        """
        return RegisterLocation.objects.select_related(
            'client', 'immobile'
        ).all()

    @staticmethod
    def register_location(form, immobile_id):
        """
        Registra uma nova locação para um imóvel.
        - Valida se o imóvel existe e está disponível
        - Cria o registro de locação
        - Marca o imóvel como locado

        Retorna o registro de locação criado.
        """
        immobile = get_object_or_404(Immobile, id=immobile_id, is_locate=False)

        location = form.save(commit=False)
        location.immobile = immobile
        location.save()

        immobile.is_locate = True
        immobile.save()

        return location

    @staticmethod
    @transaction.atomic
    def finish_location(location_id):
        """
        Finaliza uma locação ativa.
        - Retorna 404 se a locação não existir ou já estiver encerrada (dt_finished preenchido)
        - Marca o imóvel como disponível (is_locate=False)
        - Define a data/hora atual em dt_finished

        Retorna o registro de locação atualizado.
        """
        location = get_object_or_404(
            RegisterLocation, id=location_id, dt_finished__isnull=True
        )

        location.dt_finished = timezone.now()
        location.save()

        location.immobile.is_locate = False
        location.immobile.save()

        return location

    @staticmethod
    def get_report_data(filters=None):
        """
        Gera dados para relatórios de imóveis locados,
        aplicando os filtros fornecidos.

        Args:
            filters: dicionário com possíveis chaves:
                - client: nome ou email do cliente
                - is_locate: booleano
                - type_item: tipo do imóvel
                - dt_start: data início do período
                - dt_end: data fim do período

        Retorna QuerySet de imóveis com locações relacionadas.
        """
        immobiles = Immobile.objects.prefetch_related(
            Prefetch(
                'reg_location',
                queryset=RegisterLocation.objects.select_related('client')
            )
        ).all()

        if not filters:
            return immobiles.distinct()

        location_filters = Q()
        get_client = filters.get('client')
        get_dt_start = filters.get('dt_start')
        get_dt_end = filters.get('dt_end')
        get_locate = filters.get('is_locate')
        get_type_item = filters.get('type_item')

        if get_client:
            location_filters &= (
                Q(reg_location__client__name__icontains=get_client) |
                Q(reg_location__client__email__icontains=get_client)
            )

        if get_dt_start and get_dt_end:
            location_filters &= (
                Q(reg_location__dt_start__lte=get_dt_end) &
                Q(reg_location__dt_end__gte=get_dt_start)
            )

        if location_filters:
            immobiles = immobiles.filter(location_filters)

        if get_locate is not None and get_locate != '':
            immobiles = immobiles.filter(
                is_locate=(str(get_locate).lower() == 'true')
            )

        if get_type_item:
            immobiles = immobiles.filter(type_item=get_type_item)

        return immobiles.distinct()
