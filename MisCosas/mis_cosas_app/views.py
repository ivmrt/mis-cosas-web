from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .ytchannel import YTChannel
from .models import Alimentador, Item

import urllib

# Create your views here.

def youtube_parser(id):
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + id
    xmlStream = urllib.request.urlopen(url)
    canal = YTChannel(xmlStream)
    # Guardamos el alimentador (si no existe) en la base de datos,
    # nos servirá para saber a qué canal pertenece cada vídeo.
    alimentador, creado = Alimentador.objects.get_or_create(nombre=canal.nombre_canal(), enlace=canal.link_canal(), id_canal=id)
    # Recorremos la lista de videos obtenida de la función YTChannel y guardamos cada uno como un item
    for video in canal.videos():
        video = Item(nombre=video['title'], enlace=video['link'], id=video['id'],
        descripcion=video['description'], alimentador=alimentador)
        video.save()

def index(request):
    if request.method == "POST":
        # Recojo el id del alimentador
        id = request.POST['id']
        # De momento solo tenemos youtube, utilizamos el parseador de YouTube
        youtube_parser(id)
        return redirect('/')
    elif request.method == "GET":
        return render(request, 'mis_cosas_app/index.html')

def log_out(request):
    logout(request)
    return redirect("/")

def usuarios(request):
    lista_usuarios = User.objects.all()
    context = {'lista_usuarios': lista_usuarios}
    return render(request, 'mis_cosas_app/usuarios.html', context)

def log_in(request):
    if request.method == "POST":
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password']
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('/')
    else:
        formulario = AuthenticationForm()
        context = {'formulario': formulario}
        return render(request, 'mis_cosas_app/login.html', context)


def new_user(request):
    # La misma función sirve para generar el formulario y para crear el usuario
    if request.method == "POST":
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            if usuario is not None:
                login(request, usuario)
                return redirect('/')
    # Si el formulario no es válido, no devuelve nada (None) y salta excepción
    else:
        formulario = UserCreationForm();
        context = {'formulario': formulario}
        return render(request, 'mis_cosas_app/nuevo_usuario.html', context)

def info(request):
    return render(request, 'mis_cosas_app/info.html')


def alimentadores(request):
    lista_alimentadores = Alimentador.objects.all()
    context = {'lista_alimentadores': lista_alimentadores}
    return render(request, 'mis_cosas_app/alimentadores.html', context)

def alimentador(request, id_alimentador):
    alimentador = Alimentador.objects.get(id_canal = id_alimentador)
    context = {'alimentador': alimentador}
    return render(request, 'mis_cosas_app/alimentador.html', context)

def item(request, id_item):
    item = Item.objects.get(id = id_item)
    context = {'item': item}
    return render(request, 'mis_cosas_app/item.html', context)
