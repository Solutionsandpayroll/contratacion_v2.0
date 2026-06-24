from django import forms
from django.core.validators import RegexValidator

from .utils import archivo_a_base64
from .models import Empleado, Ciudad, CentroCosto, Subcliente
from .choise import *
from django.utils import timezone
import datetime
import re
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError


# ============================================================
# VALIDADORES REUTILIZABLES
# ============================================================
solo_letras_validator = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]*$',
    message='Solo se permiten letras y espacios.',
)

sin_letras_validator = RegexValidator(
    regex=r'^[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]*$',
    message='Este campo solo permite números y caracteres especiales.',
)

# ============================================================
# CAMPOS CON TOMSELECT (FK / listas largas)
# ============================================================
TOMSELECT_FIELDS = {
    'ciudad_residencia',
    'lugar_nacimiento',
    'centro_costos',
    'subcliente',
    'banco',
    'eps',
    'afp',
    'arl',
    'ccf',
    'fondo_cesantias',
}


# ============================================================
# CAMPOS DE SELECCIÓN PERSONALIZADOS (solo muestran el nombre,
# no el código completo país/departamento/DANE) — Punto 5
# ============================================================
class CiudadChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField para Ciudad que en el <option> visible solo muestra
    el nombre de la ciudad (p. ej. 'Bogotá') en vez del string completo
    con códigos (p. ej. '058 - 01 - 01002 - Bogotá'). El valor interno
    (PK) sigue siendo el mismo, así que el resto de la lógica del proyecto
    (Ciudad.from_str, etc.) no se ve afectada.
    """
    def label_from_instance(self, obj):
        nombre = getattr(obj, 'nombre_ciudad', None)
        return (nombre or str(obj)).strip()


class CentroCostoChoiceField(forms.ModelChoiceField):
    """Igual que CiudadChoiceField pero para Centro de Costos: solo nombre."""
    def label_from_instance(self, obj):
        nombre = getattr(obj, 'nombre', None)
        return (nombre or str(obj)).strip()


class SubclienteChoiceField(forms.ModelChoiceField):
    """Igual que CiudadChoiceField pero para Subcliente: solo nombre."""
    def label_from_instance(self, obj):
        nombre = getattr(obj, 'nombre', None)
        return (nombre or str(obj)).strip()


# ============================================================
# CLASE BASE — DEFAULTS AUTOMÁTICOS
# ============================================================
class DefaultModelForm(forms.ModelForm):
    FIELD_DEFAULTS = {}

    def __init__(self, *args, **kwargs):
        if args:
            data = args[0]
            if data is not None and hasattr(data, 'copy'):
                data = data.copy()
                for field_name, default_value in self.FIELD_DEFAULTS.items():
                    if not data.get(field_name):
                        data[field_name] = default_value
                args = (data,) + args[1:]
        elif 'data' in kwargs and kwargs['data'] is not None:
            data = kwargs['data'].copy()
            for field_name, default_value in self.FIELD_DEFAULTS.items():
                if not data.get(field_name):
                    data[field_name] = default_value
            kwargs['data'] = data

        super().__init__(*args, **kwargs)

        for field_name, default_value in self.FIELD_DEFAULTS.items():
            if field_name in self.fields:
                if not self.initial.get(field_name):
                    self.initial[field_name] = default_value


# ============================================================
# FORMULARIO BÁSICO
# ============================================================
class EmpleadoBasicoForm(DefaultModelForm):
    tipo_doc = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + TIPO_DOC_CHOICES,
        initial='CC',
        label='Tipo Documento',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ciudad_residencia = CiudadChoiceField(
        queryset=Ciudad.objects.all(),
        label='Ciudad de Residencia',
        empty_label='Selecciona o escribe...',
        widget=forms.Select(attrs={'class': 'form-select ciudad-select'}),
        required=False,
    )

    sexo = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + SEXO_CHOICES,
        label='Sexo',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    estado = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + ESTADO_CHOICES,
        initial='En Proceso',
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Empleado
        fields = [
            'tipo_doc', 'documento', 'nombre_1', 'nombre_2',
            'primer_apellido', 'segundo_apellido',
            'ciudad_residencia', 'sexo', 'celular', 'email', 'estado', 'compania'
        ]
        labels = {
            'nombre_1': 'Primer Nombre',
            'nombre_2': 'Segundo Nombre',
            'primer_apellido': 'Primer Apellido',
            'segundo_apellido': 'Segundo Apellido',
        }

    FIELD_DEFAULTS = {
        'tipo_doc': 'CC',
        'estado':   'En Proceso',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

        for nombre, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                if nombre in TOMSELECT_FIELDS:
                    self.fields[nombre].widget.attrs = {'class': 'form-select ciudad-select'}
                    if hasattr(self.fields[nombre], 'empty_label'):
                        self.fields[nombre].empty_label = 'Selecciona o escribe...'
                else:
                    current_attrs = self.fields[nombre].widget.attrs.copy()
                    current_attrs['class'] = 'form-select'
                    self.fields[nombre].widget.attrs = current_attrs

    def clean_nombre_1(self):
        valor = self.cleaned_data.get('nombre_1', '')
        if valor:
            solo_letras_validator(valor)
            return valor.upper()
        return valor

    def clean_nombre_2(self):
        valor = self.cleaned_data.get('nombre_2', '')
        if valor:
            solo_letras_validator(valor)
            return valor.upper()
        return valor

    def clean_primer_apellido(self):
        valor = self.cleaned_data.get('primer_apellido', '')
        if valor:
            solo_letras_validator(valor)
            return valor.upper()
        return valor

    def clean_segundo_apellido(self):
        valor = self.cleaned_data.get('segundo_apellido', '')
        if valor:
            solo_letras_validator(valor)
            return valor.upper()
        return valor

    def clean_documento(self):
        valor = self.cleaned_data.get('documento', '')
        if valor:
            sin_letras_validator(valor)
        return valor

    def clean_celular(self):
        valor = self.cleaned_data.get('celular', '')
        if valor:
            sin_letras_validator(valor)
        return valor

    def clean_ciudad_residencia(self):
        ciudad = self.cleaned_data.get('ciudad_residencia')
        if ciudad:
            return str(ciudad)
        return ''


# ============================================================
# WIDGET DE FECHA PERSONALIZADO
# ============================================================
class DateInputWidget(forms.DateInput):
    input_type = 'text'

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control date-input',
            'placeholder': 'DD/MM/AAAA',
            'autocomplete': 'off'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value:
            if isinstance(value, datetime.date):
                return value.strftime('%d/%m/%Y')
            elif isinstance(value, str):
                return value
        return ''


# ============================================================
# FORMULARIO COMPLETO
# ============================================================
class EmpleadoCompletoForm(DefaultModelForm):
    BOOLEAN_CHOICES = [
        ('False', 'No'),
        ('True', 'Sí'),
    ]

    # ── Datos Personales ──────────────────────────────────────────────────────
    f_nacimiento = forms.DateField(
        widget=DateInputWidget(), label='Fecha de Nacimiento',
        input_formats=['%d/%m/%Y'], required=False
    )
    lugar_nacimiento = CiudadChoiceField(
        queryset=Ciudad.objects.all(), label='Lugar de Nacimiento',
        empty_label='Selecciona o escribe...',
        widget=forms.Select(attrs={'class': 'form-select ciudad-select'}),
        required=False,
    )
    estado_civil = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + ESTADO_CIVIL_CHOICES,
        initial='Soltero(a)', label='Estado Civil',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )

    # ── Contacto y Residencia ────────────────────────────────────────────────
    ciudad_residencia = CiudadChoiceField(
        queryset=Ciudad.objects.all(), label='Ciudad de Residencia',
        empty_label='Selecciona o escribe...',
        widget=forms.Select(attrs={'class': 'form-select ciudad-select'}),
        required=False,
    )
    direccion_residencia = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Dirección de Residencia'
    )
    telefono_residencia = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Teléfono Residencia'
    )

    # ── Información Laboral ──────────────────────────────────────────────────
    f_ingreso = forms.DateField(
        widget=DateInputWidget(), label='Fecha de Ingreso',
        input_formats=['%d/%m/%Y'], required=False
    )
    f_retiro = forms.DateField(
        widget=DateInputWidget(), label='Fecha de Retiro',
        input_formats=['%d/%m/%Y'], required=False
    )
    tipo_contrato = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + TIPO_CONTRATO_CHOICES,
        initial='01 - Termino indefinido', label='Tipo de Contrato',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    cargo = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}), label='Cargo'
    )
    horas_mes = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + HORAS_MES_CHOICES,
        initial='220', label='Horas al Mes',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    tipo_cotizante = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + TIPO_COTIZANTE_CHOICES,
        initial='01 Dependiente', label='Tipo Cotizante',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    subtipo_cotizante = forms.CharField(
        max_length=20, required=False, initial='NO APLICA',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Subtipo Cotizante'
    )
    regimen = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + NACIONALIDAD_CHOICES,
        label='Régimen/Nacionalidad',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )

    # ── Nómina y Liquidación ─────────────────────────────────────────────────
    clase_salario = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + CLASE_SALARIO_CHOICES,
        initial='1 - Normal', label='Clase de Salario',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    sueldo = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 5.000.000',
            'inputmode': 'numeric',
            'autocomplete': 'off',
        }),
        label='Sueldo'
    )
    valor_hora = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'id': 'id_valor_hora',
            'tabindex': '-1',
        }),
        label='Valor Hora'
    )
    tipo_liquidacion = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + TIPO_LIQUIDACION_CHOICES,
        initial='2 - Mensual', label='Tipo de Liquidación',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    modo_liquidacion_conceptos = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + MODO_LIQUIDACION_CHOICES,
        initial='0 - Normal', label='Modo de Liquidación',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    cuenta_gastos = forms.CharField(
        max_length=50, required=False, initial='28',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Cuenta de Gastos'
    )

    # ── Información Bancaria ─────────────────────────────────────────────────
    banco = forms.ChoiceField(
        choices=[('', 'Selecciona o escribe...')] + BANCO_CHOICES,
        label='Banco',
        widget=forms.Select(attrs={'class': 'form-select ciudad-select'}),
        required=False
    )
    tipo_cuenta = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + TIPO_CUENTA_CHOICES,
        initial='1 - Consignación Cuenta Ahorros', label='Tipo de Cuenta',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    numero_cuenta = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Número de Cuenta'
    )

    # ── Organización ─────────────────────────────────────────────────────────
    sucursal = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}), label='Sucursal'
    )
    centro_costos = CentroCostoChoiceField(
        queryset=CentroCosto.objects.all(), label='Centro de Costos',
        empty_label='Selecciona o escribe...',
        widget=forms.Select(attrs={'class': 'form-select ciudad-select'}),
        required=False,
    )
    subcliente = SubclienteChoiceField(
        queryset=Subcliente.objects.all(), label='Subcliente',
        empty_label='Selecciona o escribe...',
        widget=forms.Select(attrs={'class': 'form-select ciudad-select'}),
        required=False,
    )
    clasificacion_2 = forms.ChoiceField(
        choices=[('', 'Selecciona...')] + CLASIFICACION_CHOICES,
        label='Clasificación',
        widget=forms.Select(attrs={'class': 'form-select'}), required=False
    )
    clasificacion_3 = forms.CharField(max_length=200, required=False, initial='NO APLICA', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Clasificación 3')
    clasificacion_4 = forms.CharField(max_length=200, required=False, initial='NO APLICA', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Clasificación 4')
    clasificacion_5 = forms.CharField(max_length=200, required=False, initial='NO APLICA', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Clasificación 5')
    clasificacion_6 = forms.CharField(max_length=200, required=False, initial='NO APLICA', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Clasificación 6')
    clasificacion_7 = forms.CharField(max_length=200, required=False, initial='NO APLICA', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Clasificación 7')

    # ── Seguridad Social ─────────────────────────────────────────────────────
    eps = forms.ChoiceField(choices=[('', 'Selecciona o escribe...')] + EPS_CHOICES, label='EPS', widget=forms.Select(attrs={'class': 'form-select ciudad-select'}), required=False)
    afp = forms.ChoiceField(choices=[('', 'Selecciona o escribe...')] + AFP_CHOICES, label='AFP', widget=forms.Select(attrs={'class': 'form-select ciudad-select'}), required=False)
    arl = forms.ChoiceField(choices=[('', 'Selecciona o escribe...')] + ARL_CHOICES, label='ARL', widget=forms.Select(attrs={'class': 'form-select ciudad-select'}), required=False)
    ccf = forms.ChoiceField(choices=[('', 'Selecciona o escribe...')] + CAJA_COMPENSACION_CHOICES, label='Caja de Compensación', widget=forms.Select(attrs={'class': 'form-select ciudad-select'}), required=False)
    fondo_cesantias = forms.ChoiceField(choices=[('', 'Selecciona o escribe...')] + FONDO_CESANTIAS_CHOICES, label='Fondo de Cesantías', widget=forms.Select(attrs={'class': 'form-select ciudad-select'}), required=False)

    # ── Retenciones ──────────────────────────────────────────────────────────
    metodo_retencion = forms.ChoiceField(choices=[('', 'Selecciona...')] + METODO_RETENCION_CHOICES, initial='Modalidad 1', label='Método de Retención', widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    porcentaje_ret = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Porcentaje Retención')
    ahorro_afc = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Ahorro AFC')
    aporte_voluntario = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Aporte Voluntario')

    # ── Beneficios ───────────────────────────────────────────────────────────
    vacaciones = forms.IntegerField(min_value=0, required=False, initial=15, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label='Vacaciones')
    dias_vacaciones_extra = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label='Días Vacaciones Extra')
    aux_alimentacion = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Auxilio Alimentación')
    aux_salud = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Auxilio Salud')
    aux_transporte = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Auxilio Transporte')
    otros_auxilios = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Otros Auxilios')
    bonificacion_ingreso = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Bonificación Ingreso')

    # ── Booleanos Si/No ──────────────────────────────────────────────────────
    extranjero          = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='¿Es Extranjero?',           widget=forms.Select(attrs={'class': 'form-select'}))
    reside_extranjero   = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='¿Reside en el Extranjero?', widget=forms.Select(attrs={'class': 'form-select'}))
    pensionado          = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='¿Pensionado?',               widget=forms.Select(attrs={'class': 'form-select'}))
    pago_por_dias       = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='¿Pago por Días?',            widget=forms.Select(attrs={'class': 'form-select'}))
    variable            = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='¿Variable?',                 widget=forms.Select(attrs={'class': 'form-select'}))
    deducible_vivienda      = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Deducible Vivienda',      widget=forms.Select(attrs={'class': 'form-select'}))
    deducible_dependientes  = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Deducible Dependientes',  widget=forms.Select(attrs={'class': 'form-select'}))
    deducible_medicina      = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Deducible Medicina',      widget=forms.Select(attrs={'class': 'form-select'}))
    poliza_salud        = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Póliza Salud',               widget=forms.Select(attrs={'class': 'form-select'}))
    poliza_vida         = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Póliza Vida',                widget=forms.Select(attrs={'class': 'form-select'}))
    parqueadero         = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Parqueadero',                widget=forms.Select(attrs={'class': 'form-select'}))
    tarjeta_credito     = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Tarjeta Crédito',            widget=forms.Select(attrs={'class': 'form-select'}))
    equipo_computo      = forms.TypedChoiceField(choices=BOOLEAN_CHOICES, coerce=lambda v: v=='True', empty_value=False, initial='False', label='Equipo Cómputo',             widget=forms.Select(attrs={'class': 'form-select'}))

    # ── Pólizas y Otros ──────────────────────────────────────────────────────
    proveedor_poliza_salud      = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Proveedor Póliza Salud')
    beneficiarios_poliza_salud  = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label='Número de Beneficiarios')
    monto_poliza_salud          = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Monto Póliza Salud')
    fecha_inicio_poliza         = forms.DateField(widget=DateInputWidget(), label='Fecha Inicio Póliza', input_formats=['%d/%m/%Y'], required=False)
    proveedor_poliza_vida       = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Proveedor Póliza Vida')
    monto_poliza_vida           = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}), label='Monto Póliza Vida')
    motivo_retiro               = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='Motivo de Retiro')
    num_hijos                   = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label='Número de Hijos')
    personas_acargo             = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label='Personas a Cargo')
    sexo = forms.ChoiceField(choices=[('', 'Selecciona...')] + SEXO_CHOICES, label='Sexo', widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Empleado
        exclude = [
            'id_empleado', 'tipo_doc', 'documento',
            'nombre_1', 'nombre_2', 'primer_apellido', 'segundo_apellido',
            'celular', 'email', 'estado', 'compania', 'fecha_registro',
            'grupo_sanguineo', 'factor_rh', 'numero_contrato'
        ]

    FIELD_DEFAULTS = {
        'tipo_contrato':              '01 - Termino indefinido',
        'horas_mes':                  '220',
        'tipo_cotizante':             '01 Dependiente',
        'subtipo_cotizante':          'NO APLICA',
        'clase_salario':              '1 - Normal',
        'tipo_liquidacion':           '2 - Mensual',
        'modo_liquidacion_conceptos': '0 - Normal',
        'metodo_retencion':           'Modalidad 1',
        'cuenta_gastos':              '28',
        'clasificacion_3':            'NO APLICA',
        'clasificacion_4':            'NO APLICA',
        'clasificacion_5':            'NO APLICA',
        'clasificacion_6':            'NO APLICA',
        'clasificacion_7':            'NO APLICA',
        'estado_civil':               'Soltero(a)',
        'tipo_cuenta':                '1 - Consignación Cuenta Ahorros',
        'extranjero':                 'False',
        'reside_extranjero':          'False',
        'pensionado':                 'False',
        'pago_por_dias':              'False',
        'variable':                   'False',
        'deducible_vivienda':         'False',
        'deducible_dependientes':     'False',
        'deducible_medicina':         'False',
        'poliza_salud':               'False',
        'poliza_vida':                'False',
        'parqueadero':                'False',
        'tarjeta_credito':            'False',
        'equipo_computo':             'False',
        'vacaciones':                 '15',
    }

    # ── Mapa: nombre_campo → (Modelo, atributo_en_instancia) ─────────────────
    # Estos campos se guardan como string en el modelo pero son ModelChoiceField
    # en el form. El __init__ los resuelve a PK para que el select se pre-rellene.
    _STRING_TO_FK = {
        'ciudad_residencia': (Ciudad,      'ciudad_residencia'),
        'lugar_nacimiento':  (Ciudad,      'lugar_nacimiento'),
        'centro_costos':     (CentroCosto, 'centro_costos'),
        'subcliente':        (Subcliente,  'subcliente'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

        # TomSelect solo en TOMSELECT_FIELDS
        for nombre, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                if nombre in TOMSELECT_FIELDS:
                    self.fields[nombre].widget.attrs = {'class': 'form-select ciudad-select'}
                    if hasattr(self.fields[nombre], 'empty_label'):
                        self.fields[nombre].empty_label = 'Selecciona o escribe...'
                else:
                    self.fields[nombre].widget.attrs = {'class': 'form-select'}

        # ── RESOLVER STRING → PK ──────────────────────────────────────────────
        # El modelo guarda ciudad_residencia / lugar_nacimiento / centro_costos /
        # subcliente como CharField. Cuando Django hace super().__init__(instance=emp)
        # copia ese string al campo, y el ModelChoiceField no lo reconoce como PK,
        # dejando el <select> sin opción seleccionada (aunque sí renderiza el queryset).
        # Aquí buscamos el objeto por __str__ y ponemos su PK en self.initial,
        # que Django usa para renderizar el valor seleccionado en el widget.
        if self.instance and self.instance.pk:
            for field_name, (Model, attr) in self._STRING_TO_FK.items():
                valor_str = getattr(self.instance, attr, None)
                if valor_str:
                    try:
                        obj = Model.from_str(valor_str)
                        if obj:
                            self.initial[field_name] = obj.pk
                    except Exception:
                        pass

            # ── SUELDO: forzar string ENTERO (sin .00) en el initial ──────────
            # El modelo guarda 'sueldo' como Decimal (ej. 4500000.00). Si se deja
            # tal cual, el template renderiza value="4500000.00" y el JS de
            # formato de miles (formatoSueldo.formatear) interpreta el ".00"
            # como parte del número, generando "450.000.000" en vez de
            # "4.500.000". Por eso aquí se limpia a un entero plano antes de
            # que llegue al widget.
            sueldo_raw = getattr(self.instance, 'sueldo', None)
            if sueldo_raw is not None:
                try:
                    self.initial['sueldo'] = str(int(Decimal(sueldo_raw)))
                except Exception:
                    pass

            valor_hora_raw = getattr(self.instance, 'valor_hora', None)
            if valor_hora_raw is not None:
                try:
                    self.initial['valor_hora'] = str(Decimal(valor_hora_raw))
                except Exception:
                    pass

    # ── Validaciones ──────────────────────────────────────────────────────────
    def clean_telefono_residencia(self):
        valor = self.cleaned_data.get('telefono_residencia', '')
        if valor: sin_letras_validator(valor)
        return valor

    def clean_numero_cuenta(self):
        valor = self.cleaned_data.get('numero_cuenta', '')
        if valor: sin_letras_validator(valor)
        return valor

    def clean_sueldo(self):
        valor = self.cleaned_data.get('sueldo', '')
        if not valor: return None
        # Se limpia cualquier separador de miles ('.') y se normaliza la coma
        # decimal (',') a punto, por si el usuario escribe "4.500.000,50".
        limpio = str(valor).strip()
        if ',' in limpio and '.' in limpio:
            # Formato "4.500.000,50" -> quitar puntos de miles, coma a punto
            limpio = limpio.replace('.', '').replace(',', '.')
        else:
            # Sin coma decimal: cualquier punto presente es separador de miles
            limpio = limpio.replace('.', '').replace(',', '')
        if not limpio:
            return None
        try:
            return Decimal(limpio)
        except Exception:
            raise forms.ValidationError('Ingresa un valor numérico válido.')

    def clean_valor_hora(self):
        valor = self.cleaned_data.get('valor_hora', '')
        if not valor: return None
        limpio = str(valor).replace('.', '').replace(',', '').strip()
        if not limpio: return None
        try:
            return Decimal(limpio)
        except Exception:
            return None

    def clean(self):
        return super().clean()

    TEXT_FK_FIELDS = ['ciudad_residencia', 'lugar_nacimiento', 'centro_costos', 'subcliente']

    def save(self, commit=True):
        instance = super().save(commit=False)

        for field_name in self.TEXT_FK_FIELDS:
            obj = self.cleaned_data.get(field_name)
            if obj:
                setattr(instance, field_name, str(obj))

        sueldo = self.cleaned_data.get('sueldo')
        if sueldo is not None:
            instance.sueldo = sueldo

        valor_hora = self.cleaned_data.get('valor_hora')
        if valor_hora is not None:
            instance.valor_hora = valor_hora

        if not instance.fecha_registro:
            instance.fecha_registro = timezone.now()

        horas_mes = self.cleaned_data.get('horas_mes')
        instance.horas_mes = int(horas_mes) if horas_mes not in (None, '') else None

        boolean_fields = [
            'extranjero', 'reside_extranjero', 'pensionado', 'pago_por_dias', 'variable',
            'deducible_vivienda', 'deducible_dependientes', 'deducible_medicina',
            'poliza_salud', 'poliza_vida', 'parqueadero', 'tarjeta_credito', 'equipo_computo'
        ]
        for field in boolean_fields:
            if field in self.cleaned_data:
                setattr(instance, field, self.cleaned_data[field])

        if 'beneficiarios_poliza_salud' in self.cleaned_data and self.cleaned_data['beneficiarios_poliza_salud'] is not None:
            instance.beneficiarios_poliza_salud = str(self.cleaned_data['beneficiarios_poliza_salud'])

        if commit:
            instance.save()
        return instance


# ============================================================
# FORMULARIOS RÁPIDOS (QUICK ADD)
# ============================================================
class CiudadQuickForm(forms.ModelForm):
    codigo_pais = forms.CharField(required=False)
    codigo_departamento = forms.CharField(required=False)
    codigo_dane = forms.CharField(required=False)
    # nombre_ciudad permanece requerido (por defecto)

    class Meta:
        model = Ciudad
        fields = ['codigo_pais', 'codigo_departamento', 'codigo_dane', 'nombre_ciudad']

    def clean_nombre_ciudad(self):
        valor = self.cleaned_data.get('nombre_ciudad', '')
        return valor.strip().upper() if valor else valor


class CentroCostoQuickForm(forms.ModelForm):
    codigo = forms.CharField(required=False)
    # nombre permanece requerido

    class Meta:
        model = CentroCosto
        fields = ['codigo', 'nombre']

    def clean_codigo(self):
        valor = self.cleaned_data.get('codigo', '')
        return valor.strip().upper() if valor else valor


class SubclienteQuickForm(forms.ModelForm):
    # codigo ya es opcional gracias a blank=True en el modelo
    # nombre permanece requerido

    class Meta:
        model = Subcliente
        fields = ['codigo', 'nombre']

    def clean_codigo(self):
        valor = self.cleaned_data.get('codigo', '')
        valor = valor.strip() if valor else ''
        return valor or None
    

# --------------------------------------------------
# Formulario (puedes ponerlo en forms.py aparte)
# --------------------------------------------------
from django import forms
from django.core.exceptions import ValidationError

from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class CorreoForm(forms.Form):

    destinatario = forms.EmailField(
        label="Destinatario",
        required=True
    )

    ESTRUCTURA_CHOICES = [
        ("1", "Estructura 1"),
        ("2", "Otra estructura"),
    ]

    estructura = forms.ChoiceField(
        label="Estructura",
        choices=ESTRUCTURA_CHOICES,
        required=True
    )

    asunto = forms.CharField(
        label="Asunto",
        max_length=200,
        required=True
    )

    cuerpo_html = forms.CharField(
        label="Cuerpo HTML",
        widget=forms.Textarea(attrs={"rows": 10}),
        required=True
    )

    adjuntos = forms.CharField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "multiple": True,
                "class": "form-control"
            }
        )
    )