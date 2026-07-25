from django.contrib import admin
from locacao import models

# Register your models here.
admin.site.register(models.Client) 
admin.site.register(models.RegisterLocation) 
 
class ImmobileImageInlineAdmin(admin.TabularInline):
    """
    classe que permite adicionar imagens de um imóvel diretamente na página de edição do imóvel
    """
    model = models.ImmobileImage
    extra = 0 

class ImmobileAdmin(admin.ModelAdmin):
    """
    classe que define o comportamento do admin para o modelo Immobile
    """
    inlines = [ImmobileImageInlineAdmin]


admin.site.register(
    models.Immobile, 
    ImmobileAdmin,
)