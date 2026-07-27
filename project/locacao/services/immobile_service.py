from django.shortcuts import get_object_or_404

from locacao.models import Immobile, ImmobileImage


class ImmobileService:
    """
    Serviço responsável por toda a lógica de negócio relacionada a Imóveis
    """

    @staticmethod
    def get_all_immobiles():
        """
        Retorna todos os imóveis com imagens pré-carregadas
        """
        return Immobile.objects.prefetch_related('immobile_images').all()

    @staticmethod
    def get_immobile_by_id(immobile_id):
        """
        Retorna um imóvel pelo ID ou lança 404
        """
        return get_object_or_404(Immobile, id=immobile_id)

    @staticmethod
    def get_available_immobiles():
        """
        Retorna apenas imóveis disponíveis (não locados)
        """
        return Immobile.objects.filter(is_locate=False)

    @staticmethod
    def _handle_images(immobile, files):
        """
        Processa e salva as imagens enviadas para um imóvel
        """
        if files:
            for f in files:
                ImmobileImage.objects.create(
                    immobile=immobile,
                    image=f
                )

    @staticmethod
    def create_immobile(form, files):
        """
        Cria um novo imóvel com suas imagens a partir de um formulário validado.
        Retorna o imóvel criado.
        """
        immobile = form.save()
        ImmobileService._handle_images(immobile, files)
        return immobile

    @staticmethod
    def update_immobile(form, files, immobile_id):
        """
        Atualiza um imóvel existente e processa novas imagens.
        Retorna o imóvel atualizado.
        """
        immobile = ImmobileService.get_immobile_by_id(immobile_id)
        immobile = form.save()
        ImmobileService._handle_images(immobile, files)
        return immobile

    @staticmethod
    def delete_immobile(immobile_id):
        """
        Exclui um imóvel pelo ID.
        Remove os arquivos físicos de todas as imagens antes de deletar os registros.
        """
        immobile = ImmobileService.get_immobile_by_id(immobile_id)

        # Remove arquivos físicos de todas as imagens antes do CASCADE
        for image_obj in immobile.immobile_images.all():
            if image_obj.image:
                image_obj.image.delete(save=False)

        immobile.delete()
