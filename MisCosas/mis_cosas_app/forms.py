from django import forms
from django.contrib.auth.models import User
from .models import Comentario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('comentario',)
