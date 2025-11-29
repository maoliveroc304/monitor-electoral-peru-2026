import pandas as pd

def obtener_data_propuestas():
    """
    Base de datos detallada de propuestas extraídas de los Planes de Gobierno (2026).
    Estructurada por los 8 ejes temáticos con descripciones ampliadas.
    """
    
    # EJES: 
    # 1. Economía, 2. Social, 3. Educación, 4. Salud, 
    # 5. Seguridad, 6. Infraestructura, 7. Ambiente, 8. Gobernanza

    data = [
        # --- ACCIÓN POPULAR (Julio Chávez) ---
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "Reactivación y Empleo Masivo",
            "Texto": "Implementación de una política expansiva de gasto público eficiente enfocada en proyectos de alto impacto social, con la meta de generar 5 millones de puestos de trabajo bajo el lema 'Trabajar y dejar trabajar' para recuperar la economía familiar.",
            "Tipo": "Programa Nacional"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "Desglobalización y MYPES",
            "Texto": "Fortalecimiento del aparato productivo nacional mediante la restricción de importaciones que compitan deslealmente y el otorgamiento de líneas de crédito baratas y accesibles para las Micro y Pequeñas Empresas (MYPES).",
            "Tipo": "Política Económica"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Economía", "Subtema": "Reforma Laboral Inclusiva",
            "Texto": "Creación de marcos legales para contratos estables de media jornada y estacionales, complementado con incentivos tributarios específicos para empresas que contraten a ciudadanos entre 55 y 65 años.",
            "Tipo": "Reforma Legislativa"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Gobernanza", "Subtema": "Justicia y Modernización",
            "Texto": "Culminación definitiva de la implementación del Código Procesal Penal a nivel nacional y transformación digital integral del Poder Judicial para garantizar procesos céleres y transparentes.",
            "Tipo": "Reforma Institucional"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Gobernanza", "Subtema": "Descentralización Efectiva",
            "Texto": "Fortalecimiento de las Agencias Regionales de Desarrollo y potenciación de los GORE y Muni-Ejecutivos para asegurar que las decisiones de inversión pública respondan a las necesidades territoriales reales.",
            "Tipo": "Gestión Pública"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Gobernanza", "Subtema": "Gobierno Abierto",
            "Texto": "Implementación de estándares de datos abiertos para que toda la información sobre gastos realizados con fondos públicos esté disponible de manera gratuita y accesible para la fiscalización ciudadana.",
            "Tipo": "Transparencia"
        },

        # --- FUERZA POPULAR (Keiko Fujimori) ---
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Empleo Rápido y Obras",
            "Texto": "Ejecución inmediata de un programa de 'Empleo Rápido' enfocado en el mantenimiento y construcción de pequeñas obras de infraestructura en zonas rurales y periféricas, asegurando contratación formal y digna.",
            "Tipo": "Programa Social"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Revolución MYPE - Licencia 0",
            "Texto": "Eliminación de barreras burocráticas de entrada al mercado mediante la 'Licencia 0', permitiendo el inicio de operaciones inmediato, acompañado de una ventanilla única electrónica para trámites.",
            "Tipo": "Decreto de Urgencia"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Institucionalidad (Prompyme)",
            "Texto": "Creación de la entidad 'Prompyme' con rango viceministerial, diseñada para centralizar y potenciar todos los programas del Estado dirigidos al soporte técnico, financiero y comercial de los emprendedores.",
            "Tipo": "Nueva Institución"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Gobernanza", "Subtema": "Comisión de Formalización",
            "Texto": "Instauración de la Comisión Nacional para la Formalización, un ente articulador que unificará los esfuerzos dispersos de los sectores estatales para integrar a la economía informal al sistema legal.",
            "Tipo": "Comisión Multisectorial"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Infraestructura", "Subtema": "Conectividad Rural",
            "Texto": "Expansión agresiva de la red de caminos vecinales y rurales para conectar centros de producción agrícola con los mercados regionales, reduciendo costos logísticos para los campesinos.",
            "Tipo": "Inversión Pública"
        },

        # --- RENOVACIÓN POPULAR (Rafael López Aliaga) ---
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Central de Lucha Anticorrupción",
            "Texto": "Creación de la Central de Lucha Contra la Corrupción (CCC) con facultades extraordinarias para realizar inteligencia financiera, detectar delitos en flagrancia y verificar el patrimonio de todos los funcionarios.",
            "Tipo": "Nueva Institución"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Reingeniería del Estado",
            "Texto": "Reducción drástica del número de ministerios para eliminar la burocracia ineficiente y traslado de las sedes de los ministerios restantes a las regiones del interior del país para una descentralización real.",
            "Tipo": "Reforma del Estado"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Código del Servicio Público",
            "Texto": "Implementación de un nuevo Código del Servicio Público que imponga la meritocracia estricta, evaluaciones de competencia obligatorias y la simplificación administrativa para eliminar trabas al ciudadano.",
            "Tipo": "Ley Orgánica"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Economía", "Subtema": "Justicia Comercial Ágil",
            "Texto": "Aprobación de una ley para que todas las controversias comerciales superiores a 10 UIT sean resueltas exclusivamente mediante arbitraje, descongestionando así la carga procesal del Poder Judicial.",
            "Tipo": "Reforma Judicial"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Control Judicial",
            "Texto": "Transferencia de los órganos de control interno del Poder Judicial y Ministerio Público a la jurisdicción de la Junta Nacional de Justicia para garantizar sanciones imparciales a jueces y fiscales.",
            "Tipo": "Reforma Constitucional"
        },

        # --- SOMOS PERÚ (George Forsyth) ---
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Reforma Política Integral",
            "Texto": "Eliminación total de la inmunidad parlamentaria para evitar la impunidad y retorno al sistema bicameral para mejorar la calidad legislativa y la representación política.",
            "Tipo": "Reforma Constitucional"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Fiscalización Efectiva",
            "Texto": "Restitución plena de la capacidad sancionadora de la Contraloría General de la República para inhabilitar y procesar a funcionarios que cometan actos de corrupción en la gestión pública.",
            "Tipo": "Ley"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Educación", "Subtema": "Escuela Judicial Peruana",
            "Texto": "Creación de la 'Escuela Judicial Peruana' en reemplazo de la actual Academia de la Magistratura, enfocada en la formación ética y técnica de nuevos jueces y fiscales.",
            "Tipo": "Institucional"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Vigilancia Ciudadana",
            "Texto": "Implementación de una plataforma digital de 'Seguimiento de Promesas Presidenciales' que permita a la ciudadanía auditar en tiempo real el cumplimiento de los compromisos de campaña.",
            "Tipo": "Tecnología Cívica"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Economía", "Subtema": "Descentralización Fiscal",
            "Texto": "Promoción de una nueva Ley de Descentralización Fiscal que otorgue mayor autonomía presupuestaria a las regiones, acompañada de un gobierno electrónico transparente en todos los ministerios.",
            "Tipo": "Ley"
        },

        # --- AVANZA PAÍS (Phillip Butters) ---
        {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Economía", "Subtema": "Defensa de la Propiedad",
            "Texto": "Garantía absoluta a la propiedad privada y fomento agresivo de la inversión privada mediante la reducción del tamaño del Estado y la eliminación de regulaciones asfixiantes.",
            "Tipo": "Política de Estado"
        },
        {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Seguridad", "Subtema": "Mano Dura",
            "Texto": "Reforma total del sistema penitenciario y policial para combatir el crimen organizado, priorizando el orden interno y la seguridad ciudadana por encima de consideraciones burocráticas.",
            "Tipo": "Plan de Seguridad"
        },
         {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Infraestructura", "Subtema": "Inversión Privada",
            "Texto": "Destrabe inmediato de megaproyectos mineros y de infraestructura paralizados, utilizando mecanismos de Gobierno a Gobierno (G2G) y Asociaciones Público-Privadas.",
            "Tipo": "Gestión"
        },
        {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Gobernanza", "Subtema": "Eficiencia Estatal",
            "Texto": "Fusión y cierre de entidades estatales redundantes para reducir el déficit fiscal y orientar los recursos hacia obras concretas en lugar de gasto corriente.",
            "Tipo": "Reforma Administrativa"
        },
        {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Social", "Subtema": "Focalización",
            "Texto": "Revisión integral de los programas sociales para asegurar que lleguen únicamente a quienes realmente lo necesitan, eliminando filtraciones y uso político.",
            "Tipo": "Auditoría"
        },

        # --- ALIANZA PARA EL PROGRESO (César Acuña) ---
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Seguridad", "Subtema": "Tecnología y Barrio Seguro",
            "Texto": "Implementación masiva de sistemas de videovigilancia con reconocimiento facial integrados a la PNP y fortalecimiento del patrullaje municipal (Serenazgo) con armas no letales.",
            "Tipo": "Inversión en Seguridad"
        },
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Infraestructura", "Subtema": "Conectividad Vial",
            "Texto": "Programa nacional de mejoramiento de carreteras y caminos vecinales para integrar las zonas productivas del interior con los puertos y mercados de exportación.",
            "Tipo": "Obra Pública"
        },
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Educación", "Subtema": "Infraestructura Educativa",
            "Texto": "Inversión prioritaria del 6% del PBI en la modernización de colegios y universidades públicas, asegurando internet y equipamiento tecnológico en todas las aulas.",
            "Tipo": "Presupuesto"
        },
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Salud", "Subtema": "Primer Nivel de Atención",
            "Texto": "Fortalecimiento de las postas y centros de salud con médicos especialistas y abastecimiento garantizado de medicamentos para descongestionar los grandes hospitales.",
            "Tipo": "Gestión Sanitaria"
        },
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Economía", "Subtema": "Apoyo al Emprendedor",
            "Texto": "Creación de un fondo de garantía estatal para facilitar el acceso a créditos con tasas preferenciales para jóvenes emprendedores y mujeres empresarias.",
            "Tipo": "Programa Financiero"
        }
    ]

    # --- GENERACIÓN DE CONTENIDO "EN PROCESO" PARA RESTO DE CANDIDATOS ---
    todos_candidatos = [
        "Hernando de Soto", "Susel Paredes", "Martín Vizcarra", "Antauro Humala", 
        "Roberto Sánchez", "Álvaro Paz de la Barra", "Carlos Añaños", "Alfonso López-Chau", 
        "Rafael Belaunde", "Fernando Cillóniz", "Mario Vizcarra", "Rosario Fernández",
        "Miguel del Castillo", "Morgan Quero", "Mariano González", "Fernando Olivera",
        "Vladimir Cerrón", "José Luna Gálvez", "Yonhy Lescano", "Carlos Espá",
        "Jorge Nieto", "Charlie Carrasco", "Fiorella Molinelli", "Roberto Chiabra", 
        "Vicente Alanoca", "Carlos Álvarez", "Walter Chirinos", "Wolfgang Grozo"
    ]

    ejes_principales = ["Economía", "Seguridad", "Salud", "Educación", "Gobernanza"]
    
    candidatos_con_data = set(d['Candidato'] for d in data)
    
    for cand in todos_candidatos:
        if cand not in candidatos_con_data:
            for eje in ejes_principales:
                data.append({
                    "Candidato": cand,
                    "Partido": "N/A",
                    "Eje": eje,
                    "Subtema": "Información en Proceso",
                    "Texto": f"El equipo técnico de Monitor Electoral está analizando actualmente el plan de gobierno presentado por {cand} ante el JNE. En breve se detallarán las propuestas específicas para el eje de {eje}, alineadas a los objetivos de desarrollo nacional.",
                    "Tipo": "Pendiente"
                })

    return pd.DataFrame(data)
