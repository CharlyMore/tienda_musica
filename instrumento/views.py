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
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import Instrumento
from .forms import InstrumentoForm, InstrumentoEditarForm

<<<<<<< HEAD

def _datos_instrumento(instrumento):
    return {
        'id': instrumento.id,
        'nombre': instrumento.nombre,
        'marca': instrumento.marca,
        'categoria': instrumento.categoria,
        'precio': instrumento.precio,
        'stock': instrumento.stock,
        'anio_fabricacion': instrumento.anio_fabricacion,
        'descripcion': instrumento.descripcion,
    }

=======
from .models import tienda_musica_project
>>>>>>> 821ec96a2b75de0aa832bad9ca727c6e35562f73

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


def detalle_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, pk=id)
    return render(request, 'instrumento/detalle.html', {'instrumento': instrumento})


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


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        usuario = authenticate(username=username, password=password)

        if usuario is None:
            return Response(
                {'error': 'Usuario o contraseña incorrectos'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=usuario)
        return Response({
            'mensaje': 'Autenticación correcta',
            'usuario': usuario.username,
            'token': token.key,
        }, status=status.HTTP_200_OK)


class InstrumentosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instrumentos = Instrumento.objects.all()
        return Response(
            [_datos_instrumento(instrumento) for instrumento in instrumentos],
            status=status.HTTP_200_OK
        )

    def post(self, request):
        form = InstrumentoForm(request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        instrumento = form.save()
        return Response({
            'mensaje': 'Instrumento creado correctamente',
            'instrumento': _datos_instrumento(instrumento),
        }, status=status.HTTP_201_CREATED)


class InstrumentoDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        instrumento = get_object_or_404(Instrumento, pk=id)
        return Response(_datos_instrumento(instrumento), status=status.HTTP_200_OK)

    def delete(self, request, id):
        instrumento = get_object_or_404(Instrumento, pk=id)
        instrumento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        instrumento = get_object_or_404(Instrumento, pk=id)
        campos_requeridos = [
            'nombre', 'marca', 'categoria', 'precio', 'stock',
            'anio_fabricacion', 'descripcion',
        ]
        faltantes = [campo for campo in campos_requeridos if campo not in request.data]
        if faltantes:
            return Response({
                'error': 'Debes enviar todos los datos.',
                'campos_faltantes': faltantes,
            }, status=status.HTTP_400_BAD_REQUEST)

        form = InstrumentoEditarForm(request.data, instance=instrumento)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        instrumento = form.save()
        return Response({
            'mensaje': 'Instrumento actualizado correctamente',
            'instrumento': _datos_instrumento(instrumento),
        }, status=status.HTTP_200_OK)