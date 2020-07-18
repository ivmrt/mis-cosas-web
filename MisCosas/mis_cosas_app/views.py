from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .ytchannel import YTChannel
from .flickrparser import FlickrParser
from .models import Alimentador, Item, Voto, Comentario, Usuario
from .forms import ComentarioForm
from django.utils import timezone
import json

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
        items = Item.objects.all()
        items_votados = items.order_by('-votos')
        formato = request.GET.get('formato')

        # Ítems votados por el usuario
        if request.user.is_authenticated:
            usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
            items_votados_usuario = Voto.objects.filter(usuario=request.user)
            items_votados_ordenados = items_votados_usuario.order_by('-fecha')
            context = {'alimentadores': alimentadores, 'items_votados_usuario': items_votados_ordenados[0:5], 'modo': usuario_para_oscuro, 'items_votados': items_votados[0:10]}
        else:
            items_votados_usuario= None
            context = {'alimentadores': alimentadores, 'items_votados_usuario': items_votados_usuario, 'items_votados': items_votados[0:10]}
        if formato == "XML":
            return render(request, 'mis_cosas_app/index.xml', context, content_type="application/xhtml+xml")
        elif formato == "JSON":
            alimentadores_json = []
            items_json = []
            items_votados_usuario_json = []
            respuesta_json = []
            for item in items_votados:
                items_json.append({"titulo": item.nombre, "enlace": item.enlace,
                "votos_totales": item.votos, "votos_positivos": item.votos_positivos,
                "votos_negativos": item.votos_negativos})
            for alimentador in alimentadores:
                alimentadores_json.append({"alimentador": alimentador.nombre,
                "enlace": alimentador.enlace, "puntuación": alimentador.votos})
            if request.user.is_authenticated:
                for item in items_votados_usuario:
                    items_votados_usuario_json.append({"titulo": item.item.nombre,
                    "enlace": item.item.enlace, "voto positivo": item.voto_positivo,
                    "voto negativo": item.voto_negativo})
                respuesta_json.append({"items": items_json[0:10], "alimentadores": alimentadores_json,
                "5 ultimos items votados por el usuario": items_votados_usuario_json})
            else:
                respuesta_json.append({"items": items_json[0:10], "alimentadores": alimentadores_json})
            respuesta_json = json.dumps(respuesta_json)
            return HttpResponse(respuesta_json, content_type="application/json")

        return render(request, 'mis_cosas_app/index.html', context)

def log_out(request):
    logout(request)
    return redirect("/")

def usuarios(request):
    lista_usuarios = User.objects.all()
    if request.user.is_authenticated:
        usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
        context = {'lista_usuarios': lista_usuarios, 'modo': usuario_para_oscuro}
    else:
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
        if request.user.is_authenticated:
            usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
            context = {'formulario': formulario, 'modo': usuario_para_oscuro}
        else:
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
        if request.user.is_authenticated:
            usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
            context = {'formulario': formulario, 'modo': usuario_para_oscuro}
        else:
            context = {'formulario': formulario}
        return render(request, 'mis_cosas_app/nuevo_usuario.html', context)

def info(request):
    if request.user.is_authenticated:
        usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
        context = {'modo': usuario_para_oscuro}
        return render(request, 'mis_cosas_app/info.html', context)
    else:
        return render(request, 'mis_cosas_app/info.html')


def alimentadores(request):
    lista_alimentadores = Alimentador.objects.all()
    # Puntuación de los alimentadores
    for alimentador in lista_alimentadores:
        alimentador.votos = 0
        for item in alimentador.item_set.all():
            item.votos = 0
            for voto in item.voto_set.all():
                if voto.voto_positivo:
                    item.votos = item.votos + 1
                elif voto.voto_negativo:
                    item.votos = item.votos - 1
            alimentador.votos = alimentador.votos + item.votos
            alimentador.save()

    if request.user.is_authenticated:
        usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
        context = {'lista_alimentadores': lista_alimentadores, 'modo': usuario_para_oscuro}
    else:
        context = {'lista_alimentadores': lista_alimentadores}
    return render(request, 'mis_cosas_app/alimentadores.html', context)

def alimentador(request, id_alimentador):
    alimentador = Alimentador.objects.get(id_canal = id_alimentador)
    if request.user.is_authenticated:
        usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
        context = {'alimentador': alimentador, 'modo': usuario_para_oscuro}
    else:
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
        if request.user.is_authenticated:
            usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
            context = {'item': item, 'voto': voto, 'comentario': comentario, 'modo': usuario_para_oscuro}
        else:
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

        # Puntuación total del ítem
        item.votos = 0
        item.votos_positivos = 0
        item.votos_negativos = 0
        for voto in Voto.objects.filter(item = item):
            if voto.voto_positivo:
                item.votos_positivos = item.votos_positivos + 1
            elif voto.voto_negativo:
                item.votos_negativos = item.votos_negativos + 1
            item.votos = item.votos_positivos - item.votos_negativos
            item.save()

        # Puntuación total de los alimentador.
        for alimentador in Alimentador.objects.all():
            alimentador.votos = 0
            for item in alimentador.item_set.all():
                item.votos = 0
                for voto in item.voto_set.all():
                    if voto.voto_positivo:
                        item.votos = item.votos + 1
                    elif voto.voto_negativo:
                        item.votos = item.votos - 1
                alimentador.votos = alimentador.votos + item.votos
                alimentador.save()

        return redirect(request.META['HTTP_REFERER'])

def usuario(request, id_usuario):
    if request.method == 'POST':
        tema = request.POST['tema']
        usuario, creado = Usuario.objects.get_or_create(usuario = request.user, defaults={'tema_oscuro': False})
        if tema == "Modo oscuro":
            usuario.tema_oscuro = True
            usuario.save()
        elif tema == "Modo claro":
            usuario.tema_oscuro = False
            usuario.save()
        url = '/usuarios/' + request.user.username
        return redirect(url)
    elif request.method == 'GET':
        usuario = User.objects.get(username = id_usuario)
        foto = Usuario.objects.get(usuario = usuario).foto
        items_votados = Voto.objects.filter(usuario = usuario)
        items_comentados = Comentario.objects.filter(usuario = usuario)
        if request.user.is_authenticated:
            usuario_para_oscuro, creado = Usuario.objects.get_or_create(usuario = request.user)
            context = {'foto': foto, 'usuario': usuario, 'items_votados': items_votados, 'items_comentados': items_comentados, 'modo': usuario_para_oscuro}
        else:
            context = {'foto': foto, 'usuario': usuario, 'items_votados': items_votados, 'items_comentados': items_comentados}
        return render(request, 'mis_cosas_app/usuario.html', context)
