from django.db import models
from datetime import datetime 


# Create your models here.
class Client(models.Model):
    """
    classe que registra uma tabela de clientes
    """
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', max_length=200, unique=True)
    phone = models.CharField('Telefone', max_length=15)
    
    def __str__(self):
        return "{} - {}".format(self.name, self.email)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']
        
        
class TypeImmobile(models.TextChoices):
    """
    define os tipos de imóveis disponíveis
    """
    APARTMENT = 'APARTAMENTO','APARTAMENTO'
    KITNET = 'KITNET','KITNET'
    HOUSE = 'CASA','CASA' 


class Immobile(models.Model):
    """
    classe que registra uma tabela de imóveis 
    """
    code = models.CharField('Código', max_length=100)
    type_item = models.CharField('Tipo de Imóvel', max_length=100, choices=TypeImmobile.choices)
    address = models.TextField('Endereço')
    price = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    is_locate = models.BooleanField('Está Locado?', default=False)

    def __str__(self):
        return "{} - {}".format(self.code, self.type_item)
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-id']
        
        
class ImmobileImage(models.Model):
    """
    classe que cadastra as imagens do imóvel
    """
    image = models.ImageField('Imagens', upload_to='images')
    immobile = models.ForeignKey(Immobile, related_name='immobile_images', on_delete=models.CASCADE)
 
    def __str__(self):
        return self.immobile.code 
      

class RegisterLocation(models.Model):
    """
    classe que registra as locações realizadas
    """
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE, related_name='reg_location', verbose_name='Imóvel')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    dt_start = models.DateTimeField('Início')
    dt_end = models.DateTimeField('Fim')
    create_at = models.DateField('Criado em', default=datetime.now, blank=True)
    
    def __str__(self):
        return "{} - {}".format(self.client, self.immobile)
    
    class Meta:
        verbose_name = 'Registrar Locação'
        verbose_name_plural = 'Registrar Locação'
        ordering = ['-id']
        