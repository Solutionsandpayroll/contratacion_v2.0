from django.db import models


class Empleado(models.Model):

    # =========================
    # Identificación y Registro
    # =========================
    id_empleado = models.CharField(primary_key=True, max_length=20)
    fecha_registro = models.DateTimeField(null=True, blank=True)
    codigo_empleado = models.CharField(max_length=20, null=True, blank=True)
    codigo_alterno = models.CharField(max_length=20, null=True, blank=True)
    tipo_doc = models.CharField(max_length=10, null=True, blank=True)
    documento = models.CharField(max_length=20, null=True, blank=True)
    numero_contrato = models.CharField(max_length=50, null=True, blank=True)

    # =========================
    # Datos Personales
    # =========================
    nombre_1 = models.CharField(max_length=200, null=True, blank=True)
    nombre_2 = models.CharField(max_length=100, null=True, blank=True)
    primer_apellido = models.CharField(max_length=100, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=100, null=True, blank=True)

    f_nacimiento = models.DateField(null=True, blank=True)
    lugar_nacimiento = models.CharField(max_length=200, null=True, blank=True)

    sexo = models.CharField(max_length=5, null=True, blank=True)
    grupo_sanguineo = models.CharField(max_length=10, null=True, blank=True)
    factor_rh = models.CharField(max_length=5, null=True, blank=True)
    sabado_habil = models.CharField(max_length=1, null=True, blank=True, default='0')
    ciudad_exp_documento = models.CharField(max_length=200, null=True, blank=True)

    estado_civil = models.CharField(max_length=20, null=True, blank=True)

    num_hijos = models.IntegerField(null=True, blank=True)
    personas_acargo = models.IntegerField(null=True, blank=True)

    # =========================
    # Contacto y Residencia
    # =========================
    ciudad_residencia = models.CharField(max_length=200, null=True, blank=True)
    direccion_residencia = models.CharField(max_length=200, null=True, blank=True)

    telefono_residencia = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)

    email = models.EmailField(max_length=200, null=True, blank=True)

    extranjero = models.BooleanField(default=False, blank=True)
    reside_extranjero = models.BooleanField(default=False, blank=True)

    # =========================
    # Información Laboral
    # =========================
    f_ingreso = models.DateField(null=True, blank=True)
    f_retiro = models.DateField(null=True, blank=True)

    estado = models.CharField(max_length=20, null=True, blank=True)
    regimen = models.CharField(max_length=50, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=200, null=True, blank=True)

    cargo = models.CharField(max_length=100, null=True, blank=True)

    horas_mes = models.IntegerField(null=True, blank=True)

    pensionado = models.BooleanField(default=False, blank=True)

    tipo_cotizante = models.CharField(max_length=20, null=True, blank=True)
    subtipo_cotizante = models.CharField(max_length=20, null=True, blank=True)

    # =========================
    # Nómina y Liquidación
    # =========================
    clase_salario = models.CharField(max_length=200, null=True, blank=True)

    sueldo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    valor_hora = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    tipo_liquidacion = models.CharField(max_length=200, null=True, blank=True)

    modo_liquidacion_conceptos = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    pago_por_dias = models.BooleanField(default=False, blank=True)
    variable = models.BooleanField(default=False, blank=True)

    cuenta_gastos = models.CharField(max_length=50, null=True, blank=True)

    # =========================
    # Información Bancaria
    # =========================
    banco = models.CharField(max_length=50, null=True, blank=True)
    tipo_cuenta = models.CharField(max_length=50, null=True, blank=True)
    numero_cuenta = models.CharField(max_length=30, null=True, blank=True)

    # =========================
    # Organización
    # =========================
    compania = models.CharField(max_length=200, null=True, blank=True)
    sucursal = models.CharField(max_length=200, null=True, blank=True)
    centro_costos = models.CharField(max_length=200, null=True, blank=True)
    subcliente = models.CharField(max_length=200, null=True, blank=True)

    clasificacion_2 = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_3 = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_4 = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_5 = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_6 = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_7 = models.CharField(max_length=200, null=True, blank=True)

    # =========================
    # Seguridad Social
    # =========================
    eps = models.CharField(max_length=200, null=True, blank=True)
    afp = models.CharField(max_length=200, null=True, blank=True)
    arl = models.CharField(max_length=200, null=True, blank=True)
    ccf = models.CharField(max_length=200, null=True, blank=True)
    fondo_cesantias = models.CharField(max_length=200, null=True, blank=True)

    # =========================
    # Retenciones
    # =========================
    metodo_retencion = models.CharField(max_length=200, null=True, blank=True)

    porcentaje_ret = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    deducible_vivienda = models.BooleanField(default=False, blank=True)
    deducible_dependientes = models.BooleanField(default=False, blank=True)
    deducible_medicina = models.BooleanField(default=False, blank=True)

    ahorro_afc = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    aporte_voluntario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # =========================
    # Beneficios
    # =========================
    vacaciones = models.IntegerField(null=True, blank=True)

    dias_vacaciones_extra = models.IntegerField(
        null=True,
        blank=True
    )

    aux_alimentacion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    aux_salud = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    aux_transporte = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    otros_auxilios = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    bonificacion_ingreso = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # =========================
    # Pólizas y Otros
    # =========================
    poliza_salud = models.BooleanField(default=False, blank=True)

    proveedor_poliza_salud = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    beneficiarios_poliza_salud = models.TextField(
        null=True,
        blank=True
    )

    monto_poliza_salud = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    fecha_inicio_poliza = models.DateField(
        null=True,
        blank=True
    )

    poliza_vida = models.BooleanField(default=False, blank=True)

    proveedor_poliza_vida = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    monto_poliza_vida = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    parqueadero = models.BooleanField(default=False, blank=True)
    tarjeta_credito = models.BooleanField(default=False, blank=True)
    equipo_computo = models.BooleanField(default=False, blank=True)

    motivo_retiro = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.documento} - {self.nombre_1} {self.primer_apellido}"


class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_dane = models.CharField(max_length=10)        # '18785'
    codigo_departamento = models.CharField(max_length=5) # '18'
    codigo_pais = models.CharField(max_length=5)         # '057'
    nombre_ciudad = models.CharField(max_length=200)     # 'SOLITA'

    class Meta:
        db_table = 'ciudades'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['nombre_ciudad']

    def __str__(self):
        return f'{self.codigo_pais} - {self.codigo_departamento} - {self.codigo_dane} - {self.nombre_ciudad}'

    @classmethod
    def from_str(cls, valor: str):
        """
        Recupera una instancia de Ciudad a partir de la cadena con formato:
        '057 - 18 - 18785 - SOLITA' (la misma que produce __str__).
        Si no encuentra coincidencia exacta, devuelve None.
        """
        if not valor:
            return None
        partes = [p.strip() for p in valor.split(' - ')]
        if len(partes) == 4:
            codigo_pais, codigo_departamento, codigo_dane, nombre = partes
            try:
                return cls.objects.get(
                    codigo_pais=codigo_pais,
                    codigo_departamento=codigo_departamento,
                    codigo_dane=codigo_dane,
                    nombre_ciudad__iexact=nombre,
                )
            except cls.DoesNotExist:
                pass
            except cls.MultipleObjectsReturned:
                return cls.objects.filter(
                    codigo_pais=codigo_pais,
                    codigo_departamento=codigo_departamento,
                    codigo_dane=codigo_dane,
                    nombre_ciudad__iexact=nombre,
                ).first()
        # Fallback: buscar por coincidencia exacta de la representación completa
        for ciudad in cls.objects.all():
            if str(ciudad) == valor.strip():
                return ciudad
        return None


class CentroCosto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'centro_costos'
        verbose_name = 'Centro de Costo'
        verbose_name_plural = 'Centros de Costos'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

    @classmethod
    def from_str(cls, valor: str):
        """
        Recupera un CentroCosto a partir de su representación 'codigo - nombre'.
        Si no se encuentra, intenta solo por nombre.
        """
        if not valor:
            return None
        partes = valor.split(' - ', 1)
        if len(partes) == 2:
            codigo, nombre = partes
            centro = cls.objects.filter(codigo__iexact=codigo.strip(), nombre__iexact=nombre.strip()).first()
            if centro:
                return centro
        # Fallback: buscar por nombre exacto
        return cls.objects.filter(nombre__iexact=valor.strip()).first()


class Subcliente(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'subclientes'
        verbose_name = 'Subcliente'
        verbose_name_plural = 'Subclientes'
        ordering = ['nombre']

    def __str__(self):
        if self.codigo:
            return f'{self.codigo} - {self.nombre}'
        return self.nombre

    @classmethod
    def from_str(cls, valor: str):
        """
        Recupera un Subcliente a partir de su representación:
        'codigo - nombre' o simplemente 'nombre' (si no tiene código).
        """
        if not valor:
            return None
        # Si contiene ' - ', asumimos formato 'codigo - nombre'
        partes = valor.split(' - ', 1)
        if len(partes) == 2:
            codigo, nombre = partes
            sub = cls.objects.filter(codigo__iexact=codigo.strip(), nombre__iexact=nombre.strip()).first()
            if sub:
                return sub
        # Fallback: buscar solo por nombre
        return cls.objects.filter(nombre__iexact=valor.strip()).first()