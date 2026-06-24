from django.contrib import messages
import uuid
import io
import os
import zipfile
from datetime import date
from docxtpl import DocxTemplate
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
import base64
import requests

def generar_id_empleado():
    """
    Genera un ID único corto para empleados
    """
    return uuid.uuid4().hex[:12].upper()


def mensaje_exito(request, mensaje):
    messages.success(request, mensaje)


def mensaje_error(request, mensaje):
    messages.error(request, mensaje)


# =========================
# Funcionalidad para generar los documentos de contratación
# =========================


# ---------------------------------------------------------------------------
# MAPEO DE TIPO DE CONTRATO
# ---------------------------------------------------------------------------

TIPO_CONTRATO_MAP = {
    '01': {'es': 'INDEFINIDO', 'en': 'INDEFINITE'},
    '02': {'es': 'FIJO',       'en': 'FIXED TERM'},
    '03': {'es': 'INDEFINIDO', 'en': 'INDEFINITE'},
    '05': {'es': 'FIJO',       'en': 'FIXED TERM'},
}

# Frases clave para detectar el código aunque vengan en texto largo
_TIPO_CONTRATO_KEYWORDS = {
    'indefinido': {'es': 'INDEFINIDO', 'en': 'INDEFINITE'},
    'fijo':       {'es': 'FIJO',       'en': 'FIXED TERM'},
    'fixed':      {'es': 'FIJO',       'en': 'FIXED TERM'},
    'integral':   None,  # no determina por sí solo
}

# Nombre de plantilla de contrato según tipo_contrato e integral
_PLANTILLAS_CONTRATO = {
    ('FIJO',       False): 'EmployementContract_FixedTerm_Ordinary Salary-copia.docx',
    ('FIJO',       True):  'EmploymentContract_FixedTerm_Integral Salary-copia.docx',
    ('INDEFINIDO', True):  'EmploymentContract_Indefinite_Integral Salary-copia.docx',
    ('INDEFINIDO', False): 'EmploymentContract_Indefinite_Ordinary Salary-copia.docx',
}

# Plantillas que se incluyen siempre
_PLANTILLAS_FIJAS = [
    'Homme Ofice Agreement-copia.docx',
    'NDA-copia.docx',
    'RECOMENDACIONES MEDICAS-copia.docx',
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

MESES_ES = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
    5: 'mayo',  6: 'junio',   7: 'julio', 8: 'agosto',
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre',
}

MESES_EN = {
    1: 'January', 2: 'February', 3: 'March',    4: 'April',
    5: 'May',     6: 'June',     7: 'July',      8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December',
}


def _como_date(valor) -> 'date | None':
    """
    Convierte el valor a date si aún no lo es (puede llegar como string 'YYYY-MM-DD'
    desde ciertos backends de Django con managed=False).
    """
    if valor is None:
        return None
    if isinstance(valor, date):
        return valor
    # Intentar parsear string 'YYYY-MM-DD'
    try:
        from datetime import datetime
        return datetime.strptime(str(valor)[:10], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


def _formatear_fecha_es(d) -> str:
    """Formatea una fecha como '10 de octubre de 2008'."""
    d = _como_date(d)
    if not d:
        return ''
    return f'{d.day} de {MESES_ES[d.month]} de {d.year}'


def _formatear_fecha_en(d) -> str:
    """Formatea una fecha como 'October 10, 2008'."""
    d = _como_date(d)
    if not d:
        return ''
    return f'{MESES_EN[d.month]} {d.day}, {d.year}'


def _limpiar_valor_seleccion(valor: str | None) -> str:
    """
    Extrae el nombre legible de un campo tipo:
      '058 - 01 - 01002 - Bogotá'              → 'Bogotá'
      'ARAGUA (ARAGUA DE BARCELONA)'            → 'ARAGUA'
      'BOGOTÁ (BOGOTÁ D.C.)'                    → 'BOGOTÁ'
    Pasos:
      1. Toma la última parte separada por ' - '
      2. Elimina todo lo que esté entre paréntesis (incluye los paréntesis)
      3. Elimina espacios sobrantes
    Nota: La búsqueda de la instancia original se realiza con los métodos
          Ciudad.from_str(), CentroCosto.from_str() y Subcliente.from_str()
          definidos en models.py.
    """
    import re
    if not valor:
        return ''
    partes = [p.strip() for p in valor.split(' - ')]
    nombre = partes[-1] if len(partes) > 1 else valor.strip()
    # Quitar paréntesis y su contenido: "ARAGUA (ARAGUA DE BARCELONA)" → "ARAGUA"
    nombre = re.sub(r'\s*\(.*?\)', '', nombre).strip()
    return nombre


def _determinar_tipo_contrato(tipo_contrato_raw: str | None):
    """
    Devuelve (tipo_es, tipo_en, es_integral).
    tipo_es: 'FIJO' | 'INDEFINIDO'
    tipo_en: 'FIXED TERM' | 'INDEFINITE'
    es_integral: True | False
    """
    raw = (tipo_contrato_raw or '').lower()

    # Intentar por código numérico al inicio
    for codigo, nombres in TIPO_CONTRATO_MAP.items():
        if raw.startswith(codigo):
            es_integral = 'integral' in raw
            return nombres['es'], nombres['en'], es_integral

    # Fallback por palabras clave
    if 'indefinido' in raw or 'indefinite' in raw:
        tipo_es, tipo_en = 'INDEFINIDO', 'INDEFINITE'
    elif 'fijo' in raw or 'fixed' in raw:
        tipo_es, tipo_en = 'FIJO', 'FIXED TERM'
    else:
        tipo_es, tipo_en = 'INDEFINIDO', 'INDEFINITE'  # default

    es_integral = 'integral' in raw
    return tipo_es, tipo_en, es_integral


def _nombre_completo(emp) -> str:
    """Concatena nombre_1, nombre_2, primer_apellido y segundo_apellido en mayúsculas."""
    partes = [
        getattr(emp, 'nombre_1', None) or '',
        getattr(emp, 'nombre_2', None) or '',
        getattr(emp, 'primer_apellido', None) or '',
        getattr(emp, 'segundo_apellido', None) or '',
    ]
    return ' '.join(p.strip() for p in partes if p.strip()).upper()


def _periodo_trabajo(f_ingreso, f_retiro) -> str:
    """Devuelve 'dd/mm/yyyy - dd/mm/yyyy' o solo inicio si no hay retiro."""
    fi = _como_date(f_ingreso)
    fr = _como_date(f_retiro)
    inicio = fi.strftime('%d/%m/%Y') if fi else ''
    fin    = fr.strftime('%d/%m/%Y') if fr else ''
    if inicio and fin:
        return f'{inicio} - {fin}'
    return inicio


def _sueldo_entero(sueldo) -> str:
    """Devuelve el sueldo sin decimales ni separador de miles como string."""
    if sueldo is None:
        return ''
    try:
        return str(int(float(sueldo)))
    except (ValueError, TypeError):
        return str(sueldo)


# ---------------------------------------------------------------------------
# LÓGICA DE JORNADA PARA HOME OFFICE AGREEMENT
# ---------------------------------------------------------------------------

def _contexto_jornada(jornada: str, horario: str,
                      residencia: str, otro_residencia_val: str,
                      ciudad_residencia: str, direccion_residencia: str) -> dict:
    """
    Genera las variables de jornada para la plantilla Home Office Agreement.

    jornada: 'tiempo_completo' | 'medio_tiempo' | 'otro'
    residencia: 'residencia' | 'otro'
    """
    ctx = {
        'j_completo':   'X' if jornada == 'tiempo_completo' else '_',
        'j_medio':      'X' if jornada == 'medio_tiempo' else '_',
        'j_otro':       'X' if jornada == 'otro' else '_',
        'horario_trabajo': horario or '',
        'u_residencia': 'X' if residencia == 'residencia' else '_',
        'u_otro':       'X' if residencia == 'otro' else '_',
        'u_otro_val':   otro_residencia_val if residencia == 'otro' else '',
        'ciudad_residencia': ciudad_residencia.upper() if ciudad_residencia else '',
        'direccion_residencia': direccion_residencia.upper() if direccion_residencia else '',
    }
    return ctx


# ---------------------------------------------------------------------------
# TABLA DINÁMICA HW/SW
# ---------------------------------------------------------------------------

def _construir_tabla_hw(items_hw: list[dict]) -> list[dict]:
    """
    items_hw: lista de dicts con keys 'hw' y 'ref'.
    Ej: [{'hw': 'Laptop Dell XPS', 'ref': 'D-001'}, ...]
    """
    return [{'hw': it.get('hw', ''), 'ref': it.get('ref', '')} for it in items_hw]


# ---------------------------------------------------------------------------
# PROXY DEL EMPLEADO
# ---------------------------------------------------------------------------
# Las plantillas usan {{empleado.nombre_completo}}, {{empleado.f_nacimiento_formateada}},
# etc. Para que docxtpl resuelva esos atributos correctamente, envolvemos el objeto
# Django en un EmpleadoProxy que expone todas las propiedades calculadas como
# atributos normales, sin tocar el modelo original.
# ---------------------------------------------------------------------------

class EmpleadoProxy:
    """
    Wrapper del objeto Empleado de Django.

    Expone todos los campos originales del modelo MÁS las propiedades
    calculadas que usan las plantillas Word con la sintaxis:
        {{ empleado.nombre_completo }}
        {{ empleado.f_nacimiento_formateada }}
        {{ empleado.tipo_contrato_simplificado }}
        ...

    El acceso a cualquier campo no declarado explícitamente se delega al
    objeto Django original mediante __getattr__, de modo que el resto de
    campos del modelo siguen disponibles en las plantillas.
    """

    def __init__(self, emp, datos_extra: dict):
        self._emp = emp
        self._datos_extra = datos_extra

        # ── Tipo de contrato ───────────────────────────────────────────────
        tipo_es, tipo_en, _ = _determinar_tipo_contrato(
            getattr(emp, 'tipo_contrato', None)
        )
        self._tipo_es = tipo_es
        self._tipo_en = tipo_en

        # Ordinario / Integral lo elige el usuario en el modal
        self._es_integral = (datos_extra.get('tipo_salario', 'ordinario') == 'integral')

        # ── Campos limpios (sin paréntesis, última parte del ' - ') ────────
        self._dir_residencia = (getattr(emp, 'direccion_residencia', None) or '').upper()
        self._ciudad_res      = (_limpiar_valor_seleccion(getattr(emp, 'ciudad_residencia',    None)) or '').upper()
        self._lugar_nac       = (_limpiar_valor_seleccion(getattr(emp, 'lugar_nacimiento',     None)) or '').upper()

        # ── Fechas pre-calculadas ──────────────────────────────────────────
        self._fecha_nac_es    = _formatear_fecha_es(getattr(emp, 'f_nacimiento', None))
        self._f_ingreso_es    = _formatear_fecha_es(getattr(emp, 'f_ingreso',    None))
        self._f_retiro_es     = _formatear_fecha_es(getattr(emp, 'f_retiro',     None))
        self._f_ingreso_en    = _formatear_fecha_en(getattr(emp, 'f_ingreso',    None))

    # ── Delegar al objeto Django para campos no declarados ─────────────────
    def __getattr__(self, name):
        return getattr(self._emp, name)

    # ──────────────────────────────────────────────────────────────────────
    # PROPIEDADES QUE USA LA PLANTILLA  (sintaxis: {{empleado.XXX}})
    # ──────────────────────────────────────────────────────────────────────

    @property
    def nombre_completo(self) -> str:
        """JUAN PABLO GARCÍA LÓPEZ"""
        partes = [
            getattr(self._emp, 'nombre_1',        None) or '',
            getattr(self._emp, 'nombre_2',        None) or '',
            getattr(self._emp, 'primer_apellido', None) or '',
            getattr(self._emp, 'segundo_apellido',None) or '',
        ]
        return ' '.join(p.strip() for p in partes if p.strip()).upper()

    @property
    def f_nacimiento_formateada(self) -> str:
        """10 de octubre de 2008"""
        return self._fecha_nac_es

    @property
    def lugar_nacimiento_fecha(self) -> str:
        """BOGOTA,10 de octubre de 2008"""
        if self._lugar_nac and self._fecha_nac_es:
            return f'{self._lugar_nac},{self._fecha_nac_es}'
        return self._lugar_nac or self._fecha_nac_es

    @property
    def f_ingreso_formateada(self) -> str:
        """14 de enero de 2019"""
        return self._f_ingreso_es

    @property
    def f_retiro_formateada(self) -> str:
        """14 de enero de 2020"""
        return self._f_retiro_es

    @property
    def f_ingreso_formateada_en(self) -> str:
        """January 14, 2019"""
        return self._f_ingreso_en

    @property
    def periodo_trabajo(self) -> str:
        """14/01/2019 - 14/01/2020"""
        return _periodo_trabajo(
            getattr(self._emp, 'f_ingreso', None),
            getattr(self._emp, 'f_retiro',  None),
        )

    @property
    def tipo_contrato_simplificado(self) -> str:
        """FIJO | INDEFINIDO"""
        return self._tipo_es

    @property
    def tipo_contrato_simplificado_en(self) -> str:
        """FIXED TERM | INDEFINITE"""
        return self._tipo_en

    @property
    def es_integral(self) -> bool:
        return self._es_integral

    # Campos limpios (sin paréntesis)
    @property
    def ciudad_residencia_limpia(self) -> str:
        return self._ciudad_res

    @property
    def lugar_nacimiento_limpio(self) -> str:
        return self._lugar_nac

    @property
    def sueldo_entero(self) -> str:
        return _sueldo_entero(getattr(self._emp, 'sueldo', None))

    @property
    def eps_limpia(self) -> str:
        return _limpiar_valor_seleccion(getattr(self._emp, 'eps', None))

    @property
    def afp_limpia(self) -> str:
        return _limpiar_valor_seleccion(getattr(self._emp, 'afp', None))

    @property
    def fondo_cesantias_limpio(self) -> str:
        return _limpiar_valor_seleccion(getattr(self._emp, 'fondo_cesantias', None))


# ---------------------------------------------------------------------------
# CONTEXTO PRINCIPAL DEL EMPLEADO
# ---------------------------------------------------------------------------

def construir_contexto(
    empleado,
    datos_extra: dict,
    items_hw: list[dict] | None = None,
) -> dict:
    """
    Construye el diccionario de contexto para docxtpl.

    La clave 'empleado' es un EmpleadoProxy, de modo que las plantillas
    pueden usar tanto:
        {{ empleado.nombre_completo }}   ← propiedad calculada
        {{ empleado.documento }}         ← campo del modelo Django
        {{ nombre_completo }}            ← variable suelta (también disponible)

    datos_extra:
        tipo_salario      : 'ordinario' (default) | 'integral'
        jornada           : 'tiempo_completo' | 'medio_tiempo' | 'otro'
        horario_trabajo   : str
        residencia        : 'residencia' | 'otro'
        otro_residencia_val: str
        fecha_examenes    : str 'YYYY-MM-DD' o date
        cargo_override    : str
    """
    # Crear el proxy — todas las propiedades calculadas viven aquí
    proxy = EmpleadoProxy(empleado, datos_extra)
    es_integral = proxy.es_integral

    # Cargo: override del modal o campo del modelo
    cargo = (
        datos_extra.get('cargo_override', '').strip()
        or _limpiar_valor_seleccion(getattr(empleado, 'cargo', None))
        or ''
    ).upper()

    # Fecha de exámenes: viene como string 'YYYY-MM-DD' desde el form
    fecha_examenes_raw = datos_extra.get('fecha_examenes', '')
    if isinstance(fecha_examenes_raw, date):
        fecha_examenes = _formatear_fecha_es(fecha_examenes_raw)
    elif fecha_examenes_raw:
        fecha_examenes = _formatear_fecha_es(fecha_examenes_raw)  # _como_date lo convierte
    else:
        fecha_examenes = ''

    ctx = {
        # ── Objeto proxy (para {{empleado.X}}) ────────────────────────────
        'empleado': proxy,

        # ── Variables sueltas (para {{X}} sin prefijo empleado) ───────────
        # Mantenerlas para compatibilidad con plantillas que no usen el prefijo
        'nombre_completo':               proxy.nombre_completo,
        'direccion_residencia':          proxy._dir_residencia,
        'ciudad_residencia':             proxy._ciudad_res,
        'lugar_nacimiento':              proxy._lugar_nac,
        'f_nacimiento_formateada':       proxy.f_nacimiento_formateada,
        'lugar_nacimiento_fecha':        proxy.lugar_nacimiento_fecha,
        'documento':                     getattr(empleado, 'documento', '') or '',
        'tipo_doc':                      (getattr(empleado, 'tipo_doc', None) or '').upper(),
        'cargo':                         cargo,
        'sueldo':                        proxy.sueldo_entero,
        'periodo_trabajo':               proxy.periodo_trabajo,
        'f_ingreso_formateada':          proxy.f_ingreso_formateada,
        'f_retiro_formateada':           proxy.f_retiro_formateada,
        'f_ingreso_formateada_en':       proxy.f_ingreso_formateada_en,
        'eps':                           proxy.eps_limpia,
        'afp':                           proxy.afp_limpia,
        'fondo_cesantias':               proxy.fondo_cesantias_limpio,
        'tipo_contrato_simplificado':    proxy.tipo_contrato_simplificado,
        'tipo_contrato_simplificado_en': proxy.tipo_contrato_simplificado_en,
        'es_integral':                   es_integral,
        'fecha_examenes':                fecha_examenes,
    }

    # Jornada (Home Office Agreement)
    ctx.update(_contexto_jornada(
        jornada=datos_extra.get('jornada', 'tiempo_completo'),
        horario=datos_extra.get('horario_trabajo', '8:00 am - 6:00 pm'),
        residencia=datos_extra.get('residencia', 'residencia'),
        otro_residencia_val=datos_extra.get('otro_residencia_val', ''),
        ciudad_residencia=proxy._ciudad_res,
        direccion_residencia=proxy._dir_residencia,
    ))

    # Tabla dinámica HW/SW
    ctx['tabla_hw'] = _construir_tabla_hw(items_hw or [])

    return ctx, es_integral


# ---------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL: GENERAR ZIP
# ---------------------------------------------------------------------------

def generar_zip_documentos(
    empleado,
    media_root: str,
    datos_extra: dict | None = None,
    items_hw: list[dict] | None = None,
) -> io.BytesIO:
    """
    Genera un archivo .zip en memoria con todos los documentos Word
    llenados con los datos del empleado.

    Parámetros
    ----------
    empleado    : instancia de models.Empleado
    media_root  : ruta al directorio /media/ donde están las plantillas
    datos_extra : dict con campos opcionales (jornada, horario, residencia, etc.)
    items_hw    : lista de dicts [{'hw': ..., 'ref': ...}]

    Retorna
    -------
    io.BytesIO con el contenido del .zip listo para enviar como HttpResponse
    """
    datos_extra = datos_extra or {}
    ctx, es_integral = construir_contexto(empleado, datos_extra, items_hw)

    # Determinar plantilla de contrato
    tipo_es = ctx['tipo_contrato_simplificado']
    nombre_plantilla_contrato = _PLANTILLAS_CONTRATO.get(
        (tipo_es, es_integral),
        _PLANTILLAS_CONTRATO[('INDEFINIDO', False)],  # fallback
    )

    plantillas = [nombre_plantilla_contrato] + _PLANTILLAS_FIJAS

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for nombre_plantilla in plantillas:
            ruta_plantilla = os.path.join(media_root, nombre_plantilla)

            if not os.path.exists(ruta_plantilla):
                # Si la plantilla no existe, agregar un archivo de texto de error
                zf.writestr(
                    f'ERROR_{nombre_plantilla}.txt',
                    f'Plantilla no encontrada: {ruta_plantilla}',
                )
                continue

            try:
                doc = DocxTemplate(ruta_plantilla)
                doc.render(ctx)

                doc_buffer = io.BytesIO()
                doc.save(doc_buffer)
                doc_buffer.seek(0)

                # Nombre del archivo de salida: sin '-copia' y sin espacios
                nombre_salida = nombre_plantilla.replace('-copia', '').replace(' ', '_')
                zf.writestr(nombre_salida, doc_buffer.read())

            except Exception as exc:  # noqa: BLE001
                # Si una plantilla falla, incluir un archivo de error en el zip
                zf.writestr(
                    f'ERROR_{nombre_plantilla}.txt',
                    f'Error al procesar la plantilla:\n{exc}',
                )

    zip_buffer.seek(0)
    return zip_buffer


#=============================
# UTILIDADES PARA ENVIAR CORREO VIA POWER AUTOMATE
#=============================
def archivo_a_base64(archivo: UploadedFile) -> dict:

    contenido_bytes = archivo.read()

    contenido_b64 = base64.b64encode(
        contenido_bytes
    ).decode("utf-8")

    return {
        "nombre": archivo.name,
        "contenido": contenido_b64,
        "tipo": archivo.content_type,
    }


def enviar_correo_via_power_automate(payload: dict):

    url = settings.POWER_AUTOMATE_URL

    headers = {
        "Content-Type": "application/json"
    }

    respuesta = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=120
    )

    return respuesta