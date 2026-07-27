from django.shortcuts import get_object_or_404

from locacao.models import Client


class ClientService:
    """
    Serviço responsável por toda a lógica de negócio relacionada a Clientes
    """

    @staticmethod
    def get_all_clients():
        """
        Retorna todos os clientes cadastrados
        """
        return Client.objects.all()

    @staticmethod
    def get_client_by_id(client_id):
        """
        Retorna um cliente pelo ID ou lança 404
        """
        return get_object_or_404(Client, id=client_id)

    @staticmethod
    def create_client(form):
        """
        Cria um novo cliente a partir de um formulário validado.
        Retorna o cliente criado
        """
        client = form.save()
        return client

    @staticmethod
    def update_client(form, client_id):
        """
        Atualiza um cliente existente a partir de um formulário validado.
        Retorna o cliente atualizado
        """
        client = ClientService.get_client_by_id(client_id)
        client = form.save()
        return client

    @staticmethod
    def delete_client(client_id):
        """
        Exclui um cliente pelo ID
        """
        client = ClientService.get_client_by_id(client_id)
        client.delete()

