from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .ytchannel import YTChannel
from .flickrparser import FlickrParser
from .models import Alimentador, Item, FotoDePerfil, Voto, Comentario
from .forms import ComentarioForm
from django.utils import timezone

import urllib

def youtube_parser(id):
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + id
    xmlStream = urllib.request.urlopen(url)
    canal = YTChannel(xmlStream)
    # Guardamos el alimentador (si no existe) en la base de datos,
    # nos servirá para saber a qué canal pertenece cada vídeo.
    alimentador, creado = Alimentador.objects.get_or_create(nombre=canal.nombre_canal(), enlace=canal.link_canal(), id_canal=id, tipo="Youtube")
    # Recorremos la lista de videos obtenida de la función YTChannel y guardamos cada uno como un item
    for video in canal.videos():
        video = Item(nombre=video['title'], enlace=video['link'], id=video['id'],
        descripcion=video['description'], alimentador=alimentador)
        video.save()

def flickr_parser(id):
    url = 'http://www.flickr.com/services/feeds/photos_public.gne?tags=' + id
    xmlStream = urllib.request.urlopen(url)
    etiqueta = FlickrParser(xmlStream)
    # Guardamos el alimentador (si no existe) en la base de datos,
    # nos servirá para saber a qué canal pertenece cada vídeo.
    alimentador, creado = Alimentador.objects.get_or_create(nombre=etiqueta.nombre_etiqueta(), enlace=etiqueta.link_etiqueta(), id_canal=id, tipo="Flickr")
    # Recorremos la lista de videos obtenida de la función YTChannel y guardamos cada uno como un item
    for foto in etiqueta.fotos():
        foto = Item(nombre=foto['title'], enlace=foto['link'], id=foto['id'],
        foto=foto['photo'], alimentador=alimentador)
        foto.save()

def index(request):
    if request.method == "POST":
        # Ahora tenemos varias acciones con POST, añadir un alimentador, seleccionar, eliminar
        accion = request.POST['accion']
        if accion == "Obtener videos":
            id = request.POST['id']
            youtube_parser(id)
            url = '/alimentadores/' + id
            return redirect(url)
        elif accion == "Obtener fotos":
            id = request.POST['id']
            flickr_parser(id)
            url = '/alimentadores/' + id
            return redirect(url)
        elif accion == "Eliminar":
            id_alimentador = request.POST['id_alimentador']
            alimentador = Alimentador.objects.get(id_canal = id_alimentador)
            alimentador.seleccionado = False
            alimentador.save()
        elif accion == "Seleccionar":
            id_alimentador = request.POST['id_alimentador']
            alimentador = Alimentador.objects.get(id_canal = id_alimentador)
            if alimentador.tipo == "Youtube":
                youtube_parser(id_alimentador)
            elif alimentador.tipo == "Flickr":
                flickr_parser(id_alimentador)
            alimentador.seleccionado = True
            alimentador.save()
            url = '/alimentadores/' + id_alimentador
            return redirect(url)
        return redirect(request.META['HTTP_REFERER'])
    elif request.method == "GET":
        alimentadores = Alimentador.objects.filter(seleccionado=True)
        # Ítems votados por el usuario
        if request.user.is_authenticated:
            items_votados = Voto.objects.filter(usuario=request.user)
            items_votados_ordenados = items_votados.order_by('-fecha')
            context = {'alimentadores': alimentadores, 'items_votados': items_votados_ordenados[0:5]}
        else:
            items_votados= None
            context = {'alimentadores': alimentadores, 'items_votados': items_votados}

        #10 ítems con más puntuación


        return render(request, 'mis_cosas_app/index.html', context)

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
            return redirect('/login')
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
    if request.method == 'GET':
        item = Item.objects.get(id = id_item)
        if request.user.is_authenticated:
            try:
                voto = Voto.objects.get(item = item, usuario = request.user)
            except Voto.DoesNotExist:
                voto = None
        else:
            voto = None
        comentario = ComentarioForm()
        context = {'item': item, 'voto': voto, 'comentario': comentario}
        return render(request, 'mis_cosas_app/item.html', context)
    elif request.method == 'POST':
        accion = request.POST['accion']
        item = Item.objects.get(id = id_item)
        try:
            voto = Voto.objects.get(item = item, usuario = request.user)
        except Voto.DoesNotExist:
            voto = Voto(item = item, usuario = request.user)
        if accion == "Like":
            voto.voto_negativo = False
            voto.voto_positivo = True
            voto.fecha = timezone.now()
            voto.save()
        elif accion == "Dislike":
            voto.voto_negativo = True
            voto.voto_positivo = False
            voto.fecha = timezone.now()
            voto.save()
        elif accion == "Comentar":
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = Comentario(usuario = request.user, comentario = form.cleaned_data['comentario'],
                item = item, fecha = timezone.now())
                comentario.save()
        # Actualizamos la puntuación total del ítem.


        return redirect(request.META['HTTP_REFERER'])

def usuario(request, id_usuario):
    usuario = User.objects.get(username = id_usuario)
    items_votados = Voto.objects.filter(usuario = usuario)
    items_comentados = Comentario.objects.filter(usuario = usuario)
    context = {'usuario': usuario, 'items_votados': items_votados, 'items_comentados': items_comentados}
    return render(request, 'mis_cosas_app/usuario.html', context)
