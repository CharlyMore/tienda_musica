from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.contrib import messages
from .models import Instrumento
from .forms import InstrumentoForm, InstrumentoEditarForm

from .models import tienda_musica_project

def listar_instrumentos(request):
    busqueda = request.GET.get('buscar', '')
    categoria = request.GET.get('categoria', '')

    instrumentos = Instrumento.objects.all()

    if busqueda:
        instrumentos = instrumentos.filter(nombre__icontains=busqueda)
    if categoria:
        instrumentos = instrumentos.filter(categoria=categoria)

    context = {
        'instrumentos': instrumentos,
        'total': instrumentos.count()
    }
    return render(request, 'instrumento/listar.html', context)

def crear_instrumento(request):
    if request.method == 'POST':
        form = InstrumentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Instrumento registrado con éxito!')
            return redirect('listar_instrumentos')
    else:
        form = InstrumentoForm()
    return render(request, 'instrumento/crear.html', {'form': form})

def editar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, pk=id)
    if request.method == 'POST':
        form = InstrumentoEditarForm(request.POST, instance=instrumento)
        if form.is_valid():
            form.save()
            messages.info(request, '¡Instrumento actualizado correctamente!')
            return redirect('listar_instrumentos')
    else:
        form = InstrumentoEditarForm(instance=instrumento)
    return render(request, 'instrumento/editar.html', {'form': form, 'instrumento': instrumento})

def eliminar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, pk=id)
    if request.method == 'POST':
        instrumento.delete()
        messages.warning(request, 'Instrumento eliminado correctamente.')
        return redirect('listar_instrumentos')
    return render(request, 'instrumento/eliminar.html', {'instrumento': instrumento})