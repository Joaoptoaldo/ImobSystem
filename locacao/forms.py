from django import forms
from locacao.models import Client, Immobile, RegisterLocation
from django.core.exceptions import ValidationError


class ClientForm(forms.ModelForm):
    """
    classe para cadastrar um cliente
    """
    class Meta:
        model = Client
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'
        
        # placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'Digite o nome completo do cliente'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite o E-mail do cliente'
        self.fields['phone'].widget.attrs['placeholder'] = 'Digite o telefone do cliente'
              
    def clean_email(self):
        """
        função para validar se o e-mail já existe no banco de dados, caso exista, retorna um erro
        """
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este e-mail já está cadastrado em nosso sistema.')
        return email


class ImmobileForm(forms.ModelForm):
    """
    classe para cadastrar um imóvel
    """
    class Meta:
        model = Immobile
        fields = '__all__'
        exclude = ('is_locate',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Placeholders
        self.fields['code'].widget.attrs['placeholder'] = 'Digite o código do imóvel'
        self.fields['price'].widget.attrs['placeholder'] = 'Digite o valor do imóvel'
        self.fields['address'].widget.attrs['placeholder'] = 'Digite o endereço completo do imóvel'
                
    def clean_code(self):
        """
        função para validar se o código do imóvel já existe no banco de dados, caso exista, retorna um erro
        """
        code = self.cleaned_data.get('code')
        if Immobile.objects.filter(code=code).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este código de imóvel já está cadastrado em nosso sistema.')
        return code
                
                
class RegisterLocationForm(forms.ModelForm):
    """
    classe para cadastrar uma locação 
    """
    dt_start = forms.DateTimeField(widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}))
    dt_end = forms.DateTimeField(widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}))

    class Meta:
        model = RegisterLocation
        fields = '__all__'
        exclude = ('immobile','create_at',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
              field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        """
        função para validar se a data de início é menor que a data de fim, caso não seja, retorna um erro
        """
        cleaned_data = super().clean()
        dt_start = cleaned_data.get('dt_start')
        dt_end = cleaned_data.get('dt_end')
        
        if dt_start and dt_end and dt_start >= dt_end:
            raise ValidationError('A data de início deve ser menor que a data de fim.')
        return cleaned_data