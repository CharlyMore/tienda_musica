from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_instrumentos, name='listar_instrumentos'),
    path('crear/', views.crear_instrumento, name='crear_instrumento'),
    path('detalle/<int:id>/', views.detalle_instrumento, name='detalle_instrumento'),
    path('editar/<int:id>/', views.editar_instrumento, name='editar_instrumento'),
    path('eliminar/<int:id>/', views.eliminar_instrumento, name='eliminar_instrumento'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/instrumentos/', views.InstrumentosAPIView.as_view(), name='api_instrumentos'),
    path(
        'api/instrumentos/<int:id>/',
        views.InstrumentoDetalleAPIView.as_view(),
        name='api_detalle_instrumento'
    ),
]
