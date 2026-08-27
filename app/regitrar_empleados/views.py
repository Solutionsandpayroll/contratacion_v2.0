from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .utils import *
from .graph import enviar_correo_via_graph, REMITENTE
import requests
from django.conf import settings
from django.utils import timezone
import pandas as pd
from datetime import datetime, date
import requests as http_requests
import base64
import os
import mimetypes
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from . utils_ficha_ingreso import *
import json

from iniciar_sesion.decorators import login_requerido

# ─────────────────────────────────────────────────────────────────────────────
# CACHE DE CHOICES (evita N+1 consultas y cursores server-side)
# ─────────────────────────────────────────────────────────────────────────────
def _construir_choices_cache():
    """
    Obtiene UNA sola vez por request todos los registros de Ciudad, CentroCosto
    y Subcliente, y construye:
      - Listas de tuplas (pk, label) para usar como choices en los formularios.
      - Diccionarios que mapean la representación string del objeto a su pk,
        para resolver el initial de cada empleado completamente en memoria,
        sin tener que volver a consultar la base de datos.
    """
    ciudades = list(Ciudad.objects.all())
    centros  = list(CentroCosto.objects.all())
    subs     = list(Subcliente.objects.all())

    def _choices(objetos, empty_label='Selecciona o escribe...'):
        opciones = [('', empty_label)]
        opciones += [(str(o.pk), str(o)) for o in objetos]
        return opciones

    # Mapas string -> pk (en memoria)
    ciudad_por_str = {str(c): c.pk for c in ciudades}
    centro_por_str = {str(c): c.pk for c in centros}
    sub_por_str    = {str(s): s.pk for s in subs}

    return {
        'choices': {
            'ciudad_residencia':      _choices(ciudades),
            'lugar_nacimiento':       _choices(ciudades),
            'ciudad_exp_documento':    _choices(ciudades),
            'centro_costos':          _choices(centros),
            'subcliente':             _choices(subs),
        },
        'ciudad_por_str': ciudad_por_str,
        'centro_por_str': centro_por_str,
        'sub_por_str':    sub_por_str,
    }


def _aplicar_choices_cache(form, choices_cache):
    """Sustituye el queryset lazy de cada ModelChoiceField por la lista
    de choices ya materializada, para no volver a golpear la BD al renderizar."""
    for nombre, choices in choices_cache['choices'].items():
        if nombre in form.fields:
            form.fields[nombre].choices = choices


def _build_completo_form(emp, choices_cache=None):
    """
    Construye un EmpleadoCompletoForm para un empleado, rellenando los
    campos ModelChoiceField con los objetos adecuados recuperados
    a partir del string almacenado en el modelo.

    Si se proporciona choices_cache (construido con _construir_choices_cache),
    la resolución se hace totalmente en memoria usando los diccionarios
    string->pk, evitando cualquier consulta adicional a la base de datos.
    """
    initial = {}

    if choices_cache is not None:
        # ── Resolución 100% en memoria ───────────────────────────────────
        ciudad_map = choices_cache['ciudad_por_str']
        centro_map = choices_cache['centro_por_str']
        sub_map    = choices_cache['sub_por_str']

        if emp.ciudad_residencia:
            pk = ciudad_map.get(emp.ciudad_residencia.strip())
            if pk:
                initial['ciudad_residencia'] = pk

        if emp.lugar_nacimiento:
            pk = ciudad_map.get(emp.lugar_nacimiento.strip())
            if pk:
                initial['lugar_nacimiento'] = pk

        if emp.ciudad_exp_documento:
            pk = ciudad_map.get(emp.ciudad_exp_documento.strip())
            if pk:
                initial['ciudad_exp_documento'] = pk

        if emp.centro_costos:
            pk = centro_map.get(emp.centro_costos.strip())
            if pk:
                initial['centro_costos'] = pk

        if emp.subcliente:
            pk = sub_map.get(emp.subcliente.strip())
            if pk:
                initial['subcliente'] = pk

    else:
        # ── Fallback: comportamiento original con consultas por fila ─────
        if emp.ciudad_residencia:
            ciudad = Ciudad.from_str(emp.ciudad_residencia)
            if ciudad:
                initial['ciudad_residencia'] = ciudad.pk

        if emp.lugar_nacimiento:
            lugar = Ciudad.from_str(emp.lugar_nacimiento)
            if lugar:
                initial['lugar_nacimiento'] = lugar.pk

        if emp.ciudad_exp_documento:
            ciudad_exp = Ciudad.from_str(emp.ciudad_exp_documento)
            if ciudad_exp:
                initial['ciudad_exp_documento'] = ciudad_exp.pk

        if emp.centro_costos:
            centro = CentroCosto.from_str(emp.centro_costos)
            if centro:
                initial['centro_costos'] = centro.pk

        if emp.subcliente:
            sub = Subcliente.from_str(emp.subcliente)
            if sub:
                initial['subcliente'] = sub.pk

    form = EmpleadoCompletoForm(instance=emp, initial=initial)

    if choices_cache is not None:
        _aplicar_choices_cache(form, choices_cache)

    return form


# ─────────────────────────────────────────────────────────────────────────────
# OTRAS VISTAS
# ─────────────────────────────────────────────────────────────────────────────
@login_requerido
def panel_admin_view(request):

    contexto = {
        'usuario': request.session.get('usuario'),
        'id_usuario': request.session.get('id_usuario'),
    }

    return render(
        request,
        "panel_admin.html",
        contexto
    )


def split_full_name(full_name):
    parts = full_name.strip().split()
    if len(parts) == 0:
        return '', '', '', ''
    elif len(parts) == 1:
        return parts[0], '', '', ''
    elif len(parts) == 2:
        return parts[0], '', parts[1], ''
    elif len(parts) == 3:
        return parts[0], '', parts[1], parts[2]
    else:
        return parts[0], parts[1], parts[-2], parts[-1]


def parse_fecha(valor):
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        valor = valor.strip()
        if not valor:
            return None
        try:
            return datetime.strptime(valor, '%d-%m-%Y').date()
        except ValueError:
            return None
    return None


ARCHIVO_FIJO_PATH   = os.path.join(settings.MEDIA_ROOT, 'Formato hoja de vida S&P_V03 (21).xlsx')
ARCHIVO_FIJO_NOMBRE = 'Formato hoja de vida S&P_V03 (21).xlsx'
ARCHIVO_FIJO_TIPO   = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

MIME_A_EXT = {
    'image/jpeg':               '.jpg',
    'image/jpg':                '.jpg',
    'image/png':                '.png',
    'image/gif':                '.gif',
    'image/webp':                '.webp',
    'image/bmp':                '.bmp',
    'image/tiff':               '.tiff',
    'application/pdf':          '.pdf',
    'application/msword':       '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
}


# ─────────────────────────────────────────────────────────────────────────────
# VISTA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
@login_requerido
def empleados_view(request):
    empleados = Empleado.objects.all().order_by('-id_empleado')
    form_basico   = EmpleadoBasicoForm()
    form_completo = EmpleadoCompletoForm()

    if request.method == 'POST':
        accion = request.POST.get('accion')

        # ── CARGAR EXCEL ──────────────────────────────────────────────────
        if accion == 'cargar_excel':
            archivo = request.FILES.get('archivo_excel')
            if archivo:
                try:
                    df = pd.read_excel(archivo, header=None)
                    registros_creados = 0

                    for idx, row in df.iterrows():
                        if idx == 0:
                            continue

                        full_name   = row.iloc[1]  if len(row) > 1  and pd.notna(row.iloc[1])  else None
                        email       = row.iloc[2]  if len(row) > 2  and pd.notna(row.iloc[2])  else None
                        compania    = row.iloc[5]  if len(row) > 5  and pd.notna(row.iloc[5])  else None
                        celular     = row.iloc[7]  if len(row) > 7  and pd.notna(row.iloc[7])  else None
                        f_ingreso_r = row.iloc[23] if len(row) > 23 and pd.notna(row.iloc[23]) else None
                        f_retiro_r  = row.iloc[24] if len(row) > 24 and pd.notna(row.iloc[24]) else None
                        sueldo      = row.iloc[25] if len(row) > 25 and pd.notna(row.iloc[25]) else None

                        if not full_name and not email:
                            continue

                        n1, n2, ap1, ap2 = split_full_name(str(full_name)) if full_name else ('', '', '', '')

                        nuevo = Empleado(
                            id_empleado      = generar_id_empleado(),
                            nombre_1         = n1.upper(),
                            nombre_2         = n2.upper(),
                            primer_apellido  = ap1.upper(),
                            segundo_apellido = ap2.upper(),
                            email            = str(email).strip() if email else '',
                            compania         = str(compania).strip() if compania else '',
                            celular          = str(celular).strip() if celular else '',
                            f_ingreso        = parse_fecha(f_ingreso_r),
                            f_retiro         = parse_fecha(f_retiro_r),
                            sueldo           = sueldo,
                            estado           = 'En Proceso',
                            fecha_registro   = timezone.now(),
                            numero_contrato  = '1',
                        )
                        nuevo.save()
                        registros_creados += 1

                    mensaje_exito(request, f'Se cargaron {registros_creados} empleados desde el Excel.')
                except Exception as e:
                    mensaje_error(request, f'Error al procesar el archivo: {str(e)}')
            else:
                mensaje_error(request, 'No se seleccionó ningún archivo.')
            return redirect('empleados')

        # ── CREAR ─────────────────────────────────────────────────────────
        elif accion == 'crear':
            form_basico = EmpleadoBasicoForm(request.POST)
            if form_basico.is_valid():
                empleado = form_basico.save(commit=False)
                empleado.id_empleado     = generar_id_empleado()
                empleado.fecha_registro  = timezone.now()
                empleado.numero_contrato = '1'
                empleado.save()
                mensaje_exito(request, 'Usuario registrado correctamente')
                return redirect('empleados')

        # ── EDITAR BÁSICO ─────────────────────────────────────────────────
        elif accion == 'editar_basico':
            empleado = get_object_or_404(Empleado, pk=request.POST.get('id_empleado'))
            form_basico = EmpleadoBasicoForm(request.POST, instance=empleado)
            if form_basico.is_valid():
                form_basico.save()
                mensaje_exito(request, 'Información básica actualizada')
                return redirect('empleados')

        # ── COMPLETAR ─────────────────────────────────────────────────────
        elif accion == 'completar':
            empleado = get_object_or_404(Empleado, pk=request.POST.get('id_empleado'))
            form_completo = EmpleadoCompletoForm(request.POST, instance=empleado)
            if form_completo.is_valid():
                emp = form_completo.save(commit=False)
                if emp.horas_mes in ('', None):
                    emp.horas_mes = None
                if not emp.fecha_registro:
                    emp.fecha_registro = timezone.now()
                if not emp.numero_contrato:
                    emp.numero_contrato = '1'
                if emp.direccion_residencia:
                    emp.direccion_residencia = emp.direccion_residencia.upper()
                emp.save()
                mensaje_exito(request, 'Información completada correctamente')
                return redirect('empleados')
            else:
                # ── Cache de choices para los demás empleados ──
                choices_cache = _construir_choices_cache()
                empleados_list = list(empleados)
                for emp in empleados_list:
                    if emp.id_empleado == empleado.id_empleado:
                        emp.form_completo = form_completo
                    else:
                        emp.form_completo = _build_completo_form(emp, choices_cache)
                defaults = dict(EmpleadoCompletoForm.FIELD_DEFAULTS)
                defaults.update(EmpleadoBasicoForm.FIELD_DEFAULTS)
                field_defaults_json = json.dumps(defaults)
                context = {
                    'empleados':     empleados_list,
                    'form_basico':   form_basico,
                    'form_completo': form_completo,
                    'modal_completar_abierto': f'modalCompletar{empleado.id_empleado}',
                    'field_defaults_json': field_defaults_json,
                }
                return render(request, 'empleados.html', context)

        # ── ELIMINAR ──────────────────────────────────────────────────────
        elif accion == 'eliminar':
            id_empleado = request.POST.get('id_empleado')
            empleado = Empleado.objects.filter(pk=id_empleado).first()
            if empleado:
                empleado.delete()
                mensaje_exito(request, 'Usuario eliminado correctamente')
            else:
                mensaje_error(request, 'El empleado ya había sido eliminado.')
            return redirect('empleados')


    # ─── CONSTRUCCIÓN DEL CONTEXTO PARA GET ───────────────────────────────
    empleados = list(empleados)
    choices_cache = _construir_choices_cache()
    for emp in empleados:
        emp.form_completo = _build_completo_form(emp, choices_cache)

    modal_crear_abierto  = form_basico.errors and not request.POST.get('id_empleado')
    modal_editar_abierto = form_basico.errors and request.POST.get('id_empleado')

    defaults = dict(EmpleadoCompletoForm.FIELD_DEFAULTS)
    defaults.update(EmpleadoBasicoForm.FIELD_DEFAULTS)
    field_defaults_json = json.dumps(defaults)

    context = {
        'empleados':            empleados,
        'form_basico':          form_basico,
        'form_completo':        form_completo,
        'modal_crear_abierto':  modal_crear_abierto,
        'modal_editar_abierto': request.POST.get('id_empleado') if modal_editar_abierto else '',
        'field_defaults_json':  field_defaults_json,
    }
    return render(request, 'empleados.html', context)

#=============================================
# Generar Archivos de contratacion
#=============================================
@login_requerido
@require_POST
def generar_documentos_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, pk=id_empleado)

    datos_extra = {
        'tipo_salario':        request.POST.get('tipo_salario', 'ordinario'),
        'jornada':             request.POST.get('jornada', 'tiempo_completo'),
        'horario_trabajo':     request.POST.get('horario_trabajo', '8:00 am - 6:00 pm'),
        'residencia':          request.POST.get('residencia', 'residencia'),
        'otro_residencia_val': request.POST.get('otro_residencia_val', ''),
        'fecha_examenes':      request.POST.get('fecha_examenes', ''),
    }

    items_hw = []
    i = 0
    while True:
        hw = request.POST.get(f'hw_{i}')
        if hw is None:
            break
        ref = request.POST.get(f'ref_{i}', '')
        if hw.strip():
            items_hw.append({'hw': hw.strip(), 'ref': ref.strip()})
        i += 1

    try:
        zip_buffer = generar_zip_documentos(
            empleado=empleado,
            media_root=settings.MEDIA_ROOT,
            datos_extra=datos_extra,
            items_hw=items_hw if items_hw else None,
        )
    except Exception as exc:
        return HttpResponse(
            f'Error generando documentos: {exc}',
            status=500,
            content_type='text/plain',
        )

    # ── Nombre del ZIP: NombreApellido_TipoDocNumero_Documentos.zip ──
    nombre_completo = (
        f"{empleado.nombre_1 or ''} {empleado.primer_apellido or ''}"
        .strip()
        .replace(' ', '_')
    )
    tipo_doc  = (empleado.tipo_doc or '').replace(' ', '_')
    documento = str(empleado.documento or empleado.id_empleado)
    nombre_archivo = f"{nombre_completo}_{tipo_doc}{documento}_Documentos.zip"

    response = HttpResponse(
        zip_buffer.read(),
        content_type='application/zip',
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response

#=============================================
# Generar Ficha de Ingreso 
#=============================================
@login_requerido
def generar_ficha_empleados(request):
    mes = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    if mes:
        year, month = mes.split('-')
        empleados_qs = Empleado.objects.filter(
            f_ingreso__year=year,
            f_ingreso__month=month
        ).order_by('primer_apellido', 'nombre_1')
    else:
        empleados_qs = Empleado.objects.none()

    context = {
        'empleados': empleados_qs,
        'mes': mes,
    }

    if request.method == 'POST':
        ids_seleccionados = request.POST.getlist('empleados')
        if not ids_seleccionados:
            messages.error(request, 'Debe seleccionar al menos un empleado.')
            return render(request, 'generar_ficha.html', context)

        empleados = Empleado.objects.filter(id_empleado__in=ids_seleccionados)

        plantilla_path = os.path.join(settings.MEDIA_ROOT, 'FICHA DE INGRESO-copia.xlsx')
        if not os.path.exists(plantilla_path):
            messages.error(request, 'Plantilla no encontrada.')
            return render(request, 'generar_ficha.html', context)

        excel_bytes = generar_excel_empleados(empleados, plantilla_path)
        response = HttpResponse(
            excel_bytes.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="ficha_ingresos_{mes}.xlsx"'
        return response

    return render(request, 'generar_ficha.html', context)

#=======================================================================
# VIEW BENEFICIOS EMPLEADOS
#=======================================================================
@login_requerido
def lista_beneficios_empleados(request):
    empleados = Empleado.objects.all()
    for emp in empleados:
        emp.nombre_completo = f"{emp.nombre_1 or ''} {emp.nombre_2 or ''} {emp.primer_apellido or ''} {emp.segundo_apellido or ''}".strip()
    return render(request, 'beneficios.html', {'empleados': empleados})


#=======================================================================
# VIEW CREACION DE NUEVOS CAMPOS 
#=======================================================================
@login_requerido
@require_POST
def crear_ciudad_ajax(request):
    form = CiudadQuickForm(request.POST)
    if form.is_valid():
        ciudad = form.save()
        return JsonResponse({'ok': True, 'id': ciudad.id, 'text': str(ciudad)})
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


@login_requerido
@require_POST
def crear_centro_costo_ajax(request):
    form = CentroCostoQuickForm(request.POST)
    if form.is_valid():
        centro = form.save()
        return JsonResponse({'ok': True, 'id': centro.id, 'text': str(centro)})
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

@login_requerido
@require_POST
def crear_subcliente_ajax(request):
    form = SubclienteQuickForm(request.POST)
    if form.is_valid():
        sub = form.save()
        return JsonResponse({'ok': True, 'id': sub.id, 'text': str(sub)})
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


# ENVIAR CORREO A EMPLEADO
@login_requerido
def enviar_correo(request):
    print("=" * 60)
    print("[DEBUG] Entrando a enviar_correo() - method:", request.method)
    print("=" * 60)

    if request.method != "POST":
        return redirect('empleados')

    id_empleado = request.POST.get("id_empleado")
    empleado = get_object_or_404(Empleado, pk=id_empleado)

    estructura = request.POST.get("estructura")
    asunto = request.POST.get("asunto", "").strip()
    cuerpo_html = request.POST.get("cuerpo_html", "").strip()

    # Reemplazo seguro de {nombre} en el servidor
    nombre_completo = f"{empleado.nombre_1} {empleado.primer_apellido}".strip()
    asunto = asunto.replace("{nombre}", nombre_completo)
    cuerpo_html = cuerpo_html.replace("{nombre}", nombre_completo)
    asunto = asunto.replace("{empresa}", empleado.compania or "")
    cuerpo_html = cuerpo_html.replace("{empresa}", empleado.compania or "")

    if not asunto or not cuerpo_html:
        messages.error(request, "El asunto y el cuerpo del correo son obligatorios.")
        return redirect('empleados')

    print(f"[DEBUG] asunto={asunto!r} cuerpo_html len={len(cuerpo_html)}")
    print(f"[DEBUG] destinatario={empleado.email!r}")

    lista_adjuntos = []
    incluir_formato = request.POST.get("incluir_formato_hoja_vida") == "1"
    archivos_usuario = request.FILES.getlist("adjuntos")
    usuario_reemplazo = any(f.name == ARCHIVO_FIJO_NOMBRE for f in archivos_usuario)

    if estructura == "1" and incluir_formato and not usuario_reemplazo and os.path.exists(ARCHIVO_FIJO_PATH):
        lista_adjuntos.append(archivo_disco_a_base64(ARCHIVO_FIJO_PATH, ARCHIVO_FIJO_NOMBRE, ARCHIVO_FIJO_TIPO))

    for archivo in archivos_usuario:
        lista_adjuntos.append(archivo_a_base64(archivo))

    print("[DEBUG] Antes de llamar a Graph...")

    # ── Envío vía Microsoft Graph ──
    try:
        respuesta = enviar_correo_via_graph(
            destinatario=empleado.email,
            asunto=asunto,
            cuerpo_html=cuerpo_html,
            adjuntos=lista_adjuntos,
        )
        print(f"[GRAPH] status={respuesta.status_code} body={respuesta.text!r}")
        print(f"[GRAPH] destinatario={empleado.email!r} remitente={REMITENTE}")
    except requests.exceptions.RequestException as exc:
        print(f"[GRAPH ERROR] Excepción capturada: {type(exc).__name__}: {exc}")
        messages.error(request, f"Error de conexión con Microsoft Graph: {exc}")
        return redirect('empleados')
    except Exception as exc:
        print(f"[GRAPH ERROR INESPERADO] {type(exc).__name__}: {exc}")
        raise

    if respuesta.status_code in (200, 202):
        messages.success(request, "Correo enviado correctamente.")
    else:
        messages.error(request, f"Error {respuesta.status_code}: {respuesta.text}")

    return redirect('empleados')