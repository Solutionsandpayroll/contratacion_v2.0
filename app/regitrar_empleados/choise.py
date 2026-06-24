ESTADO_CIVIL_CHOICES = [
    ('Soltero(a)', 'Soltero(a)'),
    ('Casado(a)', 'Casado(a)'),
    ('Separado(a)', 'Separado(a)'),
    ('Unión Libre', 'Unión Libre'),
    ('Viudo(a)', 'Viudo(a)'),
    ('Religiosa(a)', 'Religiosa(a)')
]

TIPO_COTIZANTE_CHOICES = [
    ('01 Dependiente', 'Dependiente'),
    ('12 aprendiz en etapa lectiva', 'Aprendiz en etapa lectiva'),
    ('19 Aprendiz en etapa productiva', 'Aprendiz en etapa productiva'),
]

SI_NO_CHOICES = [
    ('No', 'No'),
    ('Sí', 'Sí'),
]

PENSIONADO_CHOICES = [
    ('No', 'No'),
    ('Vejez', 'Vejez'),
]

TIPO_LIQUIDACION_CHOICES = [
    ('0 - NO APLICA', 'NO APLICA'),
    ('1 - Quincenal', 'Quincenal'),
    ('2 - Mensual', 'Mensual'),
    ('3 - Semanal', 'Semanal'),
    ('4 - Catorcenal', 'Catorcenal'),
    ('5 - Grupo 2', 'Grupo 2')
]

MODO_LIQUIDACION_CHOICES = [
    ('0 - Normal', 'Normal'),
    ('1 - Aprendiz', 'Aprendiz'),
    ('2 - Sin transporte', 'Sin transporte'),
    ('3 - Asumido SS', 'Asumido SS'),
    ('4 - Especial', 'Especial'),
    ('5 - Liquidación x Hora', 'Liquidación x Hora'),
    ('6 - Flexibilización', 'Flexibilización'),
    ('10 - Valor Hora x Clasif', 'Valor Hora x Clasif'),
    ('11 - Valor Hora x Puntos', 'Valor Hora x Puntos')
]

HORAS_MES_CHOICES = [
    (110, '110 horas'),
    (220, '220 horas'),
    (230, '230 horas'),
    (235, '235 horas'),
    (240, '240 horas'),
]

CLASE_SALARIO_CHOICES = [
    ('1 - Normal', 'Normal'),
    ('2 - Integral', 'Integral'),
]


CLASIFICACION_CHOICES = [
    ('NO APLICA', 'NO APLICA'),
    ('Operario', 'Operario'),
    ('Administrativo', 'Administrativo'),
    ('Directivo', 'Directivo'),
]

METODO_RETENCION_CHOICES = [
    ('Modalidad 1', 'Modalidad 1'),
    ('Modalidad 2', 'Modalidad 2'),
]

# --------------------------------------------------------------------------
# NUEVAS LISTAS DE EPS, FONDO DE PENSIONES, ARL,
# CAJA DE COMPENSACIÓN Y FONDO DE CESANTÍAS
# --------------------------------------------------------------------------
EPS_CHOICES = [
    ('200 - ALIANSALUD EPS', 'ALIANSALUD EPS'),
    ('201 - SALUD TOTAL SA', 'SALUD TOTAL SA'),
    ('203 - EPS SANITAS', 'EPS SANITAS'),
    ('204 - COMPENSAR ENTIDAD PROMOTORA DE SALUD', 'COMPENSAR ENTIDAD PROMOTORA DE SALUD'),
    ('205 - EPS SURA', 'EPS SURA'),
    ('206 - COMFENALCO VALLE EPS', 'COMFENALCO VALLE EPS'),
    ('207 - MEDIMÁS EPS S.A.S.', 'MEDIMÁS EPS S.A.S.'),
    ('208 - COOMEVA EPS', 'COOMEVA EPS'),
    ('209 - FAMISANAR', 'FAMISANAR'),
    ('210 - SERVICIO OCCIDENTAL DE SALUD S.O.S. S.A.', 'SERVICIO OCCIDENTAL DE SALUD S.O.S. S.A.'),
    ('211 - CRUZ BLANCA S.A', 'CRUZ BLANCA S.A'),
    ('213 - SALUDVIDA S.A EPS', 'SALUDVIDA S.A EPS'),
    ('214 - NUEVA EPS', 'NUEVA EPS'),
    ('215 - FONDO DE SOLIDARIDAD Y GARANTÍA FOSYGA', 'FONDO DE SOLIDARIDAD Y GARANTÍA FOSYGA'),
    ('216 - EMPRESAS PÚBLICAS DE MEDELLÍN DEPARTAMENTO MÉDICO', 'EMPRESAS PÚBLICAS DE MEDELLÍN DEPARTAMENTO MÉDICO'),
    ('217 - FONDO DE PASIVO SOCIAL DE FERROCARRILES', 'FONDO DE PASIVO SOCIAL DE FERROCARRILES'),
    ('218 - ALIANZA MEDELLIN ANTIOQUIA EPS S.A.S', 'ALIANZA MEDELLIN ANTIOQUIA EPS S.A.S'),
    ('219 - CAPITAL SALUD EPS', 'CAPITAL SALUD EPS'),
    ('299 - NO APLICA', 'NO APLICA'),
]

AFP_CHOICES = [   # Reemplaza la antigua AFP_CHOICES
    ('100 - PROTECCION', 'PROTECCION'),
    ('101 - PORVENIR', 'PORVENIR'),
    ('102 - OLD MUTUAL FONDO DE PENSIONES OBLIGATORIAS-SKANDIA', 'OLD MUTUAL FONDO DE PENSIONES OBLIGATORIAS-SKANDIA'),
    ('103 - OLD MUTUAL FONDO ALTERNATIVO DE PENSIONES', 'OLD MUTUAL FONDO ALTERNATIVO DE PENSIONES'),
    ('104 - COLFONDOS', 'COLFONDOS'),
    ('105 - CAJA DE AUXILIOS Y DE PRESTACIONES DE ACDAC', 'CAJA DE AUXILIOS Y DE PRESTACIONES DE ACDAC'),
    ('106 - FONDO DE PREVISIÓN SOCIAL DEL CONGRESO', 'FONDO DE PREVISIÓN SOCIAL DEL CONGRESO'),
    ('107 - PENSIONES DE ANTIOQUIA', 'PENSIONES DE ANTIOQUIA'),
    ('108 - ADMINISTRADORA COLOMBIANA DE PENSIONES COLPENSIONES', 'ADMINISTRADORA COLOMBIANA DE PENSIONES COLPENSIONES'),
    ('199 - NO APLICA', 'NO APLICA'),
]

ARL_CHOICES = [
    ('300 - A.R.L. SEGUROS DE VIDA COLPATRIA S.A. -ARL AXA COLPATRIA', 'A.R.L. SEGUROS DE VIDA COLPATRIA S.A. -ARL AXA COLPATRIA'),
    ('301 - COMPAÑÍA DE SEGUROS BOLÍVAR S.A.', 'COMPAÑÍA DE SEGUROS BOLÍVAR S.A.'),
    ('302 - SEGUROS DE VIDA AURORA', 'SEGUROS DE VIDA AURORA'),
    ('303 - ARP ALFA', 'ARP ALFA'),
    ('304 - LIBERTY SEGUROS DE VIDA S.A.', 'LIBERTY SEGUROS DE VIDA S.A.'),
    ('305 - POSITIVA COMPAÑÍA DE SEGUROS', 'POSITIVA COMPAÑÍA DE SEGUROS'),
    ('306 - COLMENA RIESGOS PROFESIONALES', 'COLMENA RIESGOS PROFESIONALES'),
    ('307 - ARL SURA', 'ARL SURA'),
    ('308 - LA EQUIDAD SEGUROS DE VIDA', 'LA EQUIDAD SEGUROS DE VIDA'),
    ('309 - MAPFRE COLOMBIA VIDA SEGUROS S.A', 'MAPFRE COLOMBIA VIDA SEGUROS S.A'),
    ('399 - NO APLICA', 'NO APLICA'),
]

CAJA_COMPENSACION_CHOICES = [
    ('400 - CAMACOL', 'CAMACOL'),
    ('401 - COMFENALCO ANTIOQUIA CCF', 'COMFENALCO ANTIOQUIA CCF'),
    ('402 - CCF DE ANTIOQUIA', 'CCF DE ANTIOQUIA'),
    ('403 - CCF CAJACOPI ATLÁNTICO', 'CCF CAJACOPI ATLÁNTICO'),
    ('404 - COMBARRANQUILLA', 'COMBARRANQUILLA'),
    ('405 - COMFAMILIAR ATLÁNTICO', 'COMFAMILIAR ATLÁNTICO'),
    ('406 - COMFENALCO CARTAGENA', 'COMFENALCO CARTAGENA'),
    ('407 - CCF DE CARTAGENA', 'CCF DE CARTAGENA'),
    ('408 - COMFABOY', 'COMFABOY'),
    ('409 - CCF DE CALDAS', 'CCF DE CALDAS'),
    ('410 - COMFACA', 'COMFACA'),
    ('411 - COMFACAUCA', 'COMFACAUCA'),
    ('412 - CCF CESAR', 'CCF CESAR'),
    ('413 - COMFACOR', 'COMFACOR'),
    ('415 - CAFAM', 'CAFAM'),
    ('416 - COLSUBSIDIO', 'COLSUBSIDIO'),
    ('418 - CCF COMPENSAR', 'CCF COMPENSAR'),
    ('419 - COMFACUNDI', 'COMFACUNDI'),
    ('420 - CCF DEL CHOCÓ', 'CCF DEL CHOCÓ'),
    ('421 - CCF DE LA GUAJIRA', 'CCF DE LA GUAJIRA'),
    ('422 - COMFAMILIAR DEL HUILA', 'COMFAMILIAR DEL HUILA'),
    ('423 - CCF DEL MAGDALENA', 'CCF DEL MAGDALENA'),
    ('424 - COFREM META', 'COFREM META'),
    ('425 - CCF DE NARIÑO', 'CCF DE NARIÑO'),
    ('426 - CCF DEL ORIENTE', 'CCF DEL ORIENTE'),
    ('427 - CCF COMFANORTE', 'CCF COMFANORTE'),
    ('428 - CCF DE BARRANCABERMEJA CAFABA', 'CCF DE BARRANCABERMEJA CAFABA'),
    ('429 - CAJASAN', 'CAJASAN'),
    ('430 - COMFENALCO SANTANDER', 'COMFENALCO SANTANDER'),
    ('431 - CCF DEL SUCRE', 'CCF DEL SUCRE'),
    ('432 - COMFENALCO QUINDÍO', 'COMFENALCO QUINDÍO'),
    ('433 - COMFAMILIAR RISARALDA', 'COMFAMILIAR RISARALDA'),
    ('434 - CCF DEL SUR DEL TOLIMA CAFASUR', 'CCF DEL SUR DEL TOLIMA CAFASUR'),
    ('435 - COMFATOLIMA', 'COMFATOLIMA'),
    ('436 - COMFENALCO –TOLIMA', 'COMFENALCO –TOLIMA'),
    ('437 - COMFENALCO VALLE', 'COMFENALCO VALLE'),
    ('438 - COMFANDI', 'COMFANDI'),
    ('439 - CCF DEL PUTUMAYO', 'CCF DEL PUTUMAYO'),
    ('440 - CAJASAI', 'CAJASAI'),
    ('441 - CCF DEL AMAZONAS CAFAMAZ', 'CCF DEL AMAZONAS CAFAMAZ'),
    ('442 - COMFIAR CCF DE ARAUCA', 'COMFIAR CCF DE ARAUCA'),
    ('443 - COMCAJA', 'COMCAJA'),
    ('444 - COMFACASANARE', 'COMFACASANARE'),
    ('445 - CAJAMAG', 'CAJAMAG'),
    ('499 - NO APLICA', 'NO APLICA'),
]

FONDO_CESANTIAS_CHOICES = [
    ('500 - FNA CESANTIAS', 'FNA CESANTIAS'),
    ('501 - PORVENIR', 'PORVENIR'),
    ('502 - PROTECCION', 'PROTECCION'),
    ('503 - COLFONDOS', 'COLFONDOS'),
    ('599 - SIN FONDO DE CESANTIAS', 'SIN FONDO DE CESANTIAS'),
]

ESTADO_CHOICES = [
    ('En Proceso', 'En Proceso'),
    ('Proceso Finalizado', 'Proceso Finalizado'),
    ('Contratado', 'Contratado'),
    ('Retirado', 'Retirado'),
    ('Suspendidos', 'Suspendidos'),
]

BANCO_CHOICES = [
    ('11 - RAPPYPAY', 'RAPPYPAY'),
    ('18 - Banco NU', 'Banco NU'),
    ('01 - BANCO DE BOGOTÁ', 'BANCO DE BOGOTÁ'),
    ('02 - BANCO POPULAR', 'BANCO POPULAR'),
    ('06 - ITAÚ CORPBANCA COLOMBIA S.A.', 'ITAÚ CORPBANCA COLOMBIA S.A.'),
    ('07 - BANCOLOMBIA S.A.', 'BANCOLOMBIA S.A.'),
    ('08 - SCOTIABANK COLOMBIA', 'SCOTIABANK COLOMBIA'),
    ('09 - CITIBANK COLOMBIA', 'CITIBANK COLOMBIA'),
    ('10 - HSBC', 'HSBC'),
    ('12 - GNB SUDAMERIS S.A.', 'GNB SUDAMERIS S.A.'),
    ('13 - BBVA COLOMBIA', 'BBVA COLOMBIA'),
    ('14 - BANCO DE CREDITO', 'BANCO DE CREDITO'),
    ('19 - COLPATRIA', 'COLPATRIA'),
    ('23 - BANCO DE OCCIDENTE', 'BANCO DE OCCIDENTE'),
    ('30 - BCSC S.A.', 'BCSC S.A.'),
    ('32 - BANCO CAJA SOCIAL - BCSC S.A.', 'BANCO CAJA SOCIAL - BCSC S.A.'),
    ('33 - INTERNATIONAL CIA FINANCIAMIEN', 'INTERNATIONAL CIA FINANCIAMIEN'),
    ('36 - BANCO PRODUBAN', 'BANCO PRODUBAN'),
    ('40 - BANCO AGRARIO DE COLOMBIA S.A.', 'BANCO AGRARIO DE COLOMBIA S.A.'),
    ('51 - BANCO DAVIVIENDA S.A.', 'BANCO DAVIVIENDA S.A.'),
    ('52 - BANCO AV VILLAS', 'BANCO AV VILLAS'),
    ('53 - BANCO W S.A.', 'BANCO W S.A.'),
    ('57 - BANCO COLMENA', 'BANCO COLMENA'),
    ('58 - BANCO PROCREDIT', 'BANCO PROCREDIT'),
    ('59 - BANCAMIA', 'BANCAMIA'),
    ('60 - BANCO PICHINCHA S.A.', 'BANCO PICHINCHA S.A.'),
    ('61 - BANCOOMEVA', 'BANCOOMEVA'),
    ('62 - CMR FALABELLA S.A.', 'CMR FALABELLA S.A.'),
    ('63 - BANCO FINANDINA S.A.', 'BANCO FINANDINA S.A.'),
    ('64 - BANCO MULTIBANK S.A', 'BANCO MULTIBANK S.A'),
    ('65 - BANCO SANTANDER COLOMBIA S.A.', 'BANCO SANTANDER COLOMBIA S.A.'),
    ('66 - BANCO COOPERATIVO COOPCENTRAL', 'BANCO COOPERATIVO COOPCENTRAL'),
    ('67 - BANCO COMPARTIR S.A', 'BANCO COMPARTIR S.A'),
    ('69 - BANCO SERFINANZA S.A.', 'BANCO SERFINANZA S.A.'),
    ('74 - NEQUI', 'NEQUI'),
    ('75 - DAVIPLATA', 'DAVIPLATA'),
    ('76 - FINANCIERA JURISCOOP', 'FINANCIERA JURISCOOP'),
    ('77 - COOP FINANCIERA DE ANTIOQUIA', 'COOP FINANCIERA DE ANTIOQUIA'),
    ('78 - COOTRAFA COOP FINANCIERA', 'COOTRAFA COOP FINANCIERA'),
    ('79 - CONFIAR COOPERATIVA FINANCIERA', 'CONFIAR COOPERATIVA FINANCIERA'),
    ('80 - COLTEFINANCIERA S.A', 'COLTEFINANCIERA S.A'),
    ('81 - EC PACIFIC', 'EC PACIFIC'),
    ('90 - BANCO CORREVAL', 'Banco Correval'),
]


TIPO_CUENTA_CHOICES = [
    ('1 - Consignación Cuenta Ahorros', 'Consignación Cuenta Ahorros'),
    ('2 - Consignación Cuenta Corriente', 'Consignación Cuenta Corriente'),
    ('3 - Pago con Cheque', 'Pago con Cheque'),
    ('4 - Pago en Efectivo', 'Pago en Efectivo'),
    ('5 - Otra Forma de Pago', 'Otra Forma de Pago'),
]


TIPO_DOC_CHOICES = [
    ('CC', 'CC'),
    ('CE', 'CE'),
    ('PT', 'PT'),
    ('TI', 'TI'),
    ('RC', 'RC'),
    ('PA', 'PA'),
    ('PE', 'PE'),
    ('NI', 'NI'),
    ('TE', 'TE'),
    ('DE', 'DE'),
    ('IE', 'IE')
]

SEXO_CHOICES = [
    ('M', 'M'),
    ('F', 'F'),
]

TIPO_CONTRATO_CHOICES = [
    ('01 - Termino indefinido', 'Termino indefinido'),
    ('02 - Termino fijo', 'Termino fijo'),
    ('03 - Termino indefinido sin transp', 'Termino indefinido sin transp'),
    ('05 - Termino fijo < 1 año', 'Termino fijo < 1 año'),
    ('06 - Honorarios', 'Honorarios'),
    ('09 - Aprendiz Sena', 'Aprendiz Sena')
]

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

NACIONALIDAD_CHOICES = [
    ('1 - Colombiano', 'Colombiano'),
    ('2 - Extranjero', 'Extranjero'),
    ('3 - Doble', 'Doble')
]


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