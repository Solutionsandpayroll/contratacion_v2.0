from django.urls import path
from .views import *


urlpatterns = [

    path("panel/",panel_admin_view,name="panel_admin"),

    # URL DE LA VIEW PRINCIPAL DE EMPLEADOS
    path('registrar-empleado/',empleados_view,name='empleados'),

    # URL DE LA VIEW DE CREACIÓN DE DOCUMENTOS
    path('<str:id_empleado>/generar-documentos/',generar_documentos_empleado,name='generar_documentos_empleado'),

    # URL DE LA VIEW DE CREACION DE LA FICHA DE INGRESO
    path('generar-ficha/', generar_ficha_empleados, name='generar_ficha_empleados'),

    # URL DE LA VIEW DE BENEFICIOS DE LOS EMPLEADOS
    path('beneficios/', lista_beneficios_empleados, name='beneficios_empleados'),

    # URL PARA LA CREACION DE NUEVOS CAMPOS COMO CIUDADES CENTRO DE COSTOS 
    path('ajax/ciudad/crear/', crear_ciudad_ajax, name='crear_ciudad_ajax'),
    path('ajax/centro-costo/crear/', crear_centro_costo_ajax, name='crear_centro_costo_ajax'),
    path('ajax/subcliente/crear/', crear_subcliente_ajax, name='crear_subcliente_ajax'),


    path("enviar/", enviar_correo, name="enviar_correo"),
    
    
]