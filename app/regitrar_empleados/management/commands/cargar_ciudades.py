from django.core.management.base import BaseCommand
from regitrar_empleados.models import Subcliente, CentroCosto


# --- LISTA COMPLETA DE CENTRO_COSTOS_CHOICES ---
CENTRO_COSTOS_CHOICES = [
    ('C1004 - SGWI', 'C1004 - SGWI'),
    ('C1005 - CSD', 'C1005 - CSD'),
    ('C1007 - NZD', 'C1007 - NZD'),
    ('C1022 - Root Capital', 'C1022 - Root Capital'),
    ('C1024 - MKD', 'C1024 - MKD'),
    ('C1029 - INSIDER', 'C1029 - INSIDER'),
    ('C1032 - FLEXCO', 'C1032 - FLEXCO'),
    ('C1036 - ACTION AD', 'C1036 - ACTION AD'),
    ('C1037 - REMOFIRST', 'C1037 - REMOFIRST'),
    ('C1038 - ONCEHUB', 'C1038 - ONCEHUB'),
    ('C1041 - EDRINGTON', 'C1041 - EDRINGTON'),
    ('C1042 - EPDM', 'C1042 - EPDM'),
    ('C1043 - NEO', 'C1043 - NEO'),
    ('C1048 - GM CONSULTORIA Y ASESORIA LTDA', 'C1048 - GM CONSULTORIA Y ASESORIA LTDA'),
    ('C1049 - ADVANCIO', 'C1049 - ADVANCIO'),
    ('C1050 - HEMMERSBACH', 'C1050 - HEMMERSBACH'),
    ('C1051 - YONYOU', 'C1051 - YONYOU'),
    ('C1052 - BUBBLE BPM INC', 'C1052 - BUBBLE BPM INC'),
    ('C1053 - GLOBAL EXPANSION', 'C1053 - GLOBAL EXPANSION'),
    ('C1055 - RIVERMATE', 'C1055 - RIVERMATE'),
    ('C1056 - EUROPORTAGE', 'C1056 - EUROPORTAGE'),
    ('C1058 - POC PHARMA', 'C1058 - POC PHARMA'),
    ('C1059 - SIFFI', 'C1059 - SIFFI'),
    ('CC000 - GEO HR SERVICES', 'CC000 - GEO HR SERVICES'),
    ('CC005 - BASIS GLOBAL TECHNOLOGIES, INC.', 'CC005 - BASIS GLOBAL TECHNOLOGIES, INC.'),
    ('CC009 - GUNNEBO ENTRANCE CONTROL', 'CC009 - GUNNEBO ENTRANCE CONTROL'),
    ('CC010 - INSTRUCTURE GLOBAL LTD', 'CC010 - INSTRUCTURE GLOBAL LTD'),
    ('CC012 - LIFENET HEALTH', 'CC012 - LIFENET HEALTH'),
    ('CC013 - MARIADB', 'CC013 - MARIADB'),
    ('CC015 - OPPORTUNITY INTERNATIONAL', 'CC015 - OPPORTUNITY INTERNATIONAL'),
    ('CC017 - SEAGULL SCIENTIFIC', 'CC017 - SEAGULL SCIENTIFIC'),
    ('CC020 - SOPHOS', 'CC020 - SOPHOS'),
    ('CC021 - HITACHI GLOBAL AIR POWER', 'CC021 - HITACHI GLOBAL AIR POWER'),
    ('CC023 - WIKIMEDIA FOUNDATION', 'CC023 - WIKIMEDIA FOUNDATION'),
    ('CC024 - ACCESS INFORMATION MANAGEMENT SHARED SERVICES, LLC', 'CC024 - ACCESS INFORMATION MANAGEMENT SHARED SERVICES, LLC'),
    ('CC027 - ROOT CAPITAL', 'CC027 - ROOT CAPITAL'),
    ('CC028 - ROCKETFELLER PHILANTHROPY ADVISORS', 'CC028 - ROCKETFELLER PHILANTHROPY ADVISORS'),
    ('CC029 - LEISTRITZ ADVANCED TECHNOLOGIES CORP', 'CC029 - LEISTRITZ ADVANCED TECHNOLOGIES CORP'),
    ('CC030 - BAC', 'CC030 - BAC'),
    ('CC032 - IETA', 'CC032 - IETA'),
    ('CC033 - HSI', 'CC033 - HSI'),
    ('CC034 - UPWORK', 'CC034 - UPWORK'),
    ('CC035 - GEORGIA INSTITUTE OF TECHNOLOGY', 'CC035 - GEORGIA INSTITUTE OF TECHNOLOGY'),
    ('CC038 - BOBST', 'CC038 - BOBST'),
    ('CC040 - ENVIRONMENTAL DYNAMICS INTL', 'CC040 - ENVIRONMENTAL DYNAMICS INTL'),
    ('CC042 - LEPU MEDICAL', 'CC042 - LEPU MEDICAL'),
    ('CC049 - CARESTREAM DENTAL', 'CC049 - CARESTREAM DENTAL'),
    ('CC051 - ZINKLAR', 'CC051 - ZINKLAR'),
    ('CC052 - GLOBAL FUND FOR SURVIVORS', 'CC052 - GLOBAL FUND FOR SURVIVORS'),
    ('CC053 - NEXTURE BIO', 'CC053 - NEXTURE BIO'),
    ('CC054 - SIG SAUER', 'CC054 - SIG SAUER'),
    ('CC055 - INTERNATIONAL RESEARCH AND EXCHANGE BOARD INC', 'CC055 - INTERNATIONAL RESEARCH AND EXCHANGE BOARD INC'),
    ('CC057 - PROJECT MANAGEMENT INSTITUTE', 'CC057 - PROJECT MANAGEMENT INSTITUTE'),
    ('CC058 - SPARQ', 'CC058 - SPARQ'),
    ('CC059 - EPRODUCTIVE SOFTWARE', 'CC059 - EPRODUCTIVE SOFTWARE'),
    ('CC060 - BEST FORMULATIONS', 'CC060 - BEST FORMULATIONS'),
    ('CC065 - ALLEGIS GROUP  INC', 'CC065 - ALLEGIS GROUP  INC'),
    ('CC066 - SELLMARK CORPORATION', 'CC066 - SELLMARK CORPORATION'),
    ('CC067 - TITAN METER BIDCO CORPORATION', 'CC067 - TITAN METER BIDCO CORPORATION'),
    ('CC068 - UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL', 'CC068 - UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL'),
    ('CC070 - BMC MEDICAL CO LTD', 'CC070 - BMC MEDICAL CO LTD'),
    ('CC071 - WEBBER+STUDIO', 'CC071 - WEBBER+STUDIO'),
    ('CC072 - GRAINGER SERVICES INTERNATIONAL, Inc', 'CC072 - GRAINGER SERVICES INTERNATIONAL, Inc'),
    ('CC073 - ZENNIO', 'CC073 - ZENNIO'),
    ('CC074 - EARTHWORKS', 'CC074 - EARTHWORKS'),
    ('CC075 - DET-TRONICS', 'CC075 - DET-TRONICS'),
    ('CC076 - FORGE GLOBAL', 'CC076 - FORGE GLOBAL'),
    ('CC077 - LANO SOFTWARE GMBH', 'CC077 - LANO SOFTWARE GMBH'),
    ('CC078 - PURDUE UNIVERSITY', 'CC078 - PURDUE UNIVERSITY'),
    ('CC100 - GROUP IT', 'CC100 - GROUP IT'),
    ('A1001 - GASTOS ADMINISTRATIVOS S&P', 'A1001 - GASTOS ADMINISTRATIVOS S&P'),
    ('A1002 - COSTOS DE VENTAS', 'A1002 - COSTOS DE VENTAS'),
    ('A1004 - ADMON Y PREPARACIÓN DE NÓMINA Y SEG SOCIAL S&P', 'A1004 - ADMON Y PREPARACIÓN DE NÓMINA Y SEG SOCIAL S&P'),
    ('A1005 - SERVICIO BPO IN HOUSE S&P', 'A1005 - SERVICIO BPO IN HOUSE S&P'),
    ('A1006 - GESTION DE PAGO A TERCEROS', 'A1006 - GESTION DE PAGO A TERCEROS'),
    ('A1009 - PROFESSIONAL EMPLOYER SERVICE S&P', 'A1009 - PROFESSIONAL EMPLOYER SERVICE S&P'),
]

# --- LISTA COMPLETA DE SUBCLIENTE_CHOICES ---
SUBCLIENTE_CHOICES = [
    ('NO APLICA', 'NO APLICA'),
    ('02 - Remofirst - FERROUS', '02 - Remofirst - FERROUS'),
    ('04 - Remofirst - 10AK', '04 - Remofirst - 10AK'),
    ('05 - Remofirst - BLULEADZ', '05 - Remofirst - BLULEADZ'),
    ('06 - Remofirst - TC1 CORPORATION SAC', '06 - Remofirst - TC1 CORPORATION SAC'),
    ('07 - Remofirst - BGB COMUNICATIONS, LLC', '07 - Remofirst - BGB COMUNICATIONS, LLC'),
    ('08 - Remofirst - HYPATOS', '08 - Remofirst - HYPATOS'),
    ('09 - Remofirst - R&R WINDOWS', '09 - Remofirst - R&R WINDOWS'),
    ('10 - Remofirst - VELO 3D', '10 - Remofirst - VELO 3D'),
    ('12 - Remofirst - STARLIGHT SOFTWARE SOLUTIONS', '12 - Remofirst - STARLIGHT SOFTWARE SOLUTIONS'),
    ('13 - Remofirst - ONE FIREFLY, LLC', '13 - Remofirst - ONE FIREFLY, LLC'),
    ('14 - Remofirst - SEARCH WIZARDS, INC', '14 - Remofirst - SEARCH WIZARDS, INC'),
    ('15 - Remofirst - INSIGTHFUL', '15 - Remofirst - INSIGTHFUL'),
    ('18 - Remofirst - COOP EDGAR', '18 - Remofirst - COOP EDGAR'),
    ('19 - Remofirst - AMG GLOBAL DISTRIBUTION INC.', '19 - Remofirst - AMG GLOBAL DISTRIBUTION INC.'),
    ('20 - Remofirst - CARBONBETTER', '20 - Remofirst - CARBONBETTER'),
    ('21 - Remofirst - CPaT Global LLC.', '21 - Remofirst - CPaT Global LLC.'),
    ('22 - Remofirst - Keller Managemenrt Company', '22 - Remofirst - Keller Managemenrt Company'),
    ('23 - Remofirst - AG Law Firm LLC', '23 - Remofirst - AG Law Firm LLC'),
    ('24 - Remofirst - Prometryx, Inc', '24 - Remofirst - Prometryx, Inc'),
    ('25 - Remofirst - ISLAMIC RELIEF', '25 - Remofirst - ISLAMIC RELIEF'),
    ('26 - Remofirst - SwiftData Technology LLC', '26 - Remofirst - SwiftData Technology LLC'),
    ('27 - Remofirst - FACADE STUDIO, LLC', '27 - Remofirst - FACADE STUDIO, LLC'),
    ('28 - Remofirst - International Concierge Inc', '28 - Remofirst - International Concierge Inc'),
    ('29 - Remofirst - Klein & Sheridan, LC', '29 - Remofirst - Klein & Sheridan, LC'),
    ('30 - Remofirst - Micro-Dyn Medical Systems, L', '30 - Remofirst - Micro-Dyn Medical Systems, L'),
    ('31 - Remofirst - THX Ltd', '31 - Remofirst - THX Ltd'),
    ('32 - Remofirst - Donebydeputy Inc', '32 - Remofirst - Donebydeputy Inc'),
    ('33 - Remofirst - Salty Slopes LLC', '33 - Remofirst - Salty Slopes LLC'),
    ('34 - Remofirst - ASM LAW GROUP', '34 - Remofirst - ASM LAW GROUP'),
    ('35 - Remofirst - Thresholdz Inc', '35 - Remofirst - Thresholdz Inc'),
    ('36 - Remofirst - Guard-Buildings, INC', '36 - Remofirst - Guard-Buildings, INC'),
    ('37 - Remofirst - SinergiaAnimal', '37 - Remofirst - SinergiaAnimal'),
    ('38 - Remofirst - Quantic Vision, S.A', '38 - Remofirst - Quantic Vision, S.A'),
    ('40 - Remofirst - RecruitGo Portal', '40 - Remofirst - RecruitGo Portal'),
    ('41 - Remofirst - Radpair', '41 - Remofirst - Radpair'),
    ('42 - Remofirst - TESICNOR S.L', '42 - Remofirst - TESICNOR S.L'),
    ('43 - Remo - American Freight Solutions, Inc', '43 - Remo - American Freight Solutions, Inc'),
    ('44 - Remofirst - Ultramain Systems, Inc', '44 - Remofirst - Ultramain Systems, Inc'),
    ('45 - Remofirst - BÜCHI Labortechnik AG', '45 - Remofirst - BÜCHI Labortechnik AG'),
    ('46 - Remo - MMV Medicines for Malaria Venture', '46 - Remo - MMV Medicines for Malaria Venture'),
    ('47 - Remo - Berkheimer Enterprises LLC DBA Be', '47 - Remo - Berkheimer Enterprises LLC DBA Be'),
    ('48 - Remofirst - IGS SOLUTIONS', '48 - Remofirst - IGS SOLUTIONS'),
    ('49 - Remofirst - Magno Jet Industria Ltda', '49 - Remofirst - Magno Jet Industria Ltda'),
    ('50 - Remofirst - BRIT AI WEB SOLUTIONS LLC', '50 - Remofirst - BRIT AI WEB SOLUTIONS LLC'),
    ('51 - Remofirst - TECNIZY-GCAT GROUP', '51 - Remofirst - TECNIZY-GCAT GROUP'),
    ('52 - Remorfirst - LUZIDOS INC', '52 - Remorfirst - LUZIDOS INC'),
    ('53 - Remofirst - Remote Medicine, Inc', '53 - Remofirst - Remote Medicine, Inc'),
    ('54 - Remofirst - Roger R. Foisy Professi', '54 - Remofirst - Roger R. Foisy Professi'),
    ('55 - Remofirst - Bayview Dental Inc', '55 - Remofirst - Bayview Dental Inc'),
]


def procesar_centro_costo(entry):
    """
    Recibe una tupla ('C1004 - SGWI', 'C1004 - SGWI') y extrae codigo y nombre.
    """
    valor = entry[0]
    if ' - ' in valor:
        partes = valor.split(' - ', 1)
        codigo = partes[0].strip()
        nombre = partes[1].strip() if len(partes) > 1 else ''
    else:
        codigo = valor
        nombre = valor
    return codigo, nombre


def procesar_subcliente(entry):
    """
    Recibe una tupla ('02 - Remofirst - FERROUS', ...) o ('NO APLICA', ...).
    Devuelve (codigo, nombre). Para 'NO APLICA', codigo=None.
    """
    valor = entry[0]
    if valor == 'NO APLICA':
        return None, 'NO APLICA'
    if ' - ' in valor:
        partes = valor.split(' - ', 1)
        codigo = partes[0].strip()
        nombre = partes[1].strip() if len(partes) > 1 else ''
        return codigo, nombre
    return valor, valor


class Command(BaseCommand):
    help = 'Carga los centros de costo y subclientes en la base de datos'

    def handle(self, *args, **kwargs):
        # ========== CENTROS DE COSTO ==========
        self.stdout.write(self.style.MIGRATE_HEADING('Cargando centros de costo...'))
        creados_cc = 0
        actualizados_cc = 0
        errores_cc = 0

        for entry in CENTRO_COSTOS_CHOICES:
            try:
                codigo, nombre = procesar_centro_costo(entry)
                if not codigo:
                    continue
                obj, creado = CentroCosto.objects.update_or_create(
                    codigo=codigo,
                    defaults={'nombre': nombre}
                )
                if creado:
                    creados_cc += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Creado: {obj}'))
                else:
                    actualizados_cc += 1
                    self.stdout.write(self.style.WARNING(f'↻ Actualizado: {obj}'))
            except Exception as e:
                errores_cc += 1
                self.stdout.write(self.style.ERROR(f'❌ Error en {entry[0]}: {e}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n📊 Centros de costo — Creados: {creados_cc} | Actualizados: {actualizados_cc} | Errores: {errores_cc}'
        ))

        # ========== SUBCLIENTES ==========
        self.stdout.write(self.style.MIGRATE_HEADING('\nCargando subclientes...'))
        creados_sub = 0
        actualizados_sub = 0
        errores_sub = 0

        for entry in SUBCLIENTE_CHOICES:
            try:
                codigo, nombre = procesar_subcliente(entry)
                if codigo is None:
                    # Caso especial: 'NO APLICA' → codigo = None
                    obj, creado = Subcliente.objects.get_or_create(
                        codigo=None,
                        defaults={'nombre': nombre}
                    )
                    if not creado and obj.nombre != nombre:
                        obj.nombre = nombre
                        obj.save()
                        actualizados_sub += 1
                        self.stdout.write(self.style.WARNING(f'↻ Actualizado: {obj}'))
                    elif creado:
                        creados_sub += 1
                        self.stdout.write(self.style.SUCCESS(f'✅ Creado: {obj}'))
                    else:
                        self.stdout.write(f'ℹ️  Existente: {obj}')
                else:
                    obj, creado = Subcliente.objects.update_or_create(
                        codigo=codigo,
                        defaults={'nombre': nombre}
                    )
                    if creado:
                        creados_sub += 1
                        self.stdout.write(self.style.SUCCESS(f'✅ Creado: {obj}'))
                    else:
                        actualizados_sub += 1
                        self.stdout.write(self.style.WARNING(f'↻ Actualizado: {obj}'))
            except Exception as e:
                errores_sub += 1
                self.stdout.write(self.style.ERROR(f'❌ Error en {entry[0]}: {e}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n📊 Subclientes — Creados: {creados_sub} | Actualizados: {actualizados_sub} | Errores: {errores_sub}'
        ))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Proceso completado. Total creados: {creados_cc + creados_sub} | Total actualizados: {actualizados_cc + actualizados_sub} | Errores: {errores_cc + errores_sub}'
        ))