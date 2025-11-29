import pandas as pd

def obtener_data_propuestas():
    """
    Base de datos de propuestas extraídas de los Planes de Gobierno (2026).
    Fuente: Documentos proporcionados.
    """
    
    data = [
        # --- ACCIÓN POPULAR (Julio Chávez) ---
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "Reactivación y Empleo",
            "Texto": "Ejecutar política expansiva con gasto eficiente para crear 5 millones de puestos de trabajo. Lema: 'Trabajar y dejar trabajar'.",
            "Tipo": "Programa"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "MYPEs y Crédito",
            "Texto": "Otorgar crédito barato a las MYPES y priorizar el aparato productivo nacional (Desglobalizar la economía).",
            "Tipo": "Económico"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "Reforma Laboral",
            "Texto": "Crear contratos laborales estables de media jornada e incentivos tributarios para contratar personas entre 55 y 65 años.",
            "Tipo": "Ley"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Gobernanza", "Subtema": "Justicia",
            "Texto": "Culminar la implementación del Código Procesal Penal y modernización digital del sistema judicial.",
            "Tipo": "Reforma"
        },

        # --- FUERZA POPULAR (Keiko Fujimori) ---
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Empleo Rápido",
            "Texto": "Mecanismo de empleo rápido mediante pequeñas obras de infraestructura en zonas rurales y periféricas con contratación formal.",
            "Tipo": "Programa"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Licencia 0 MYPE",
            "Texto": "Eliminar barreras de entrada estableciendo la 'Licencia 0' y una ventanilla única electrónica para emprendedores.",
            "Tipo": "Decreto"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Prompyme",
            "Texto": "Crear 'Prompyme' con rango viceministerial para concentrar programas de apoyo y promover mercados.",
            "Tipo": "Institucional"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Gobernanza", "Subtema": "Formalización",
            "Texto": "Crear la Comisión Nacional para la Formalización para unificar esfuerzos del Estado.",
            "Tipo": "Comisión"
        },

        # --- RENOVACIÓN POPULAR (Rafael López Aliaga) ---
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Lucha Anticorrupción",
            "Texto": "Crear una Central de Lucha Contra la Corrupción (CCC) con poder para detectar delito in fraganti y verificar patrimonio.",
            "Tipo": "Institucional"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Reforma del Estado",
            "Texto": "Reducir número de ministerios por ineficiencia y descentralizar sedes del Ejecutivo.",
            "Tipo": "Reforma"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Servicio Civil",
            "Texto": "Implementar el 'CÓDIGO DEL SERVICIO PÚBLICO': ingreso por méritos y eliminación de barreras burocráticas.",
            "Tipo": "Ley"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Justicia Comercial",
            "Texto": "Ley para que controversias comerciales mayores a 10 UIT se tramiten exclusivamente por vía arbitral.",
            "Tipo": "Ley"
        },

        # --- SOMOS PERÚ (George Forsyth) ---
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Reforma Política",
            "Texto": "Eliminar inmunidad parlamentaria y restituir rol sancionador de la Contraloría.",
            "Tipo": "Reforma Const."
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Reforma Judicial",
            "Texto": "Crear una 'Escuela Judicial Peruana' en reemplazo de la Academia de la Magistratura.",
            "Tipo": "Institucional"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Transparencia",
            "Texto": "Sistema de Seguimiento de Promesas Presidenciales para vigilancia ciudadana.",
            "Tipo": "Tecnológico"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Descentralización",
            "Texto": "Nueva Ley de Descentralización Fiscal y Gobierno Electrónico en ministerios.",
            "Tipo": "Ley"
        },
         # --- ALIANZA PARA EL PROGRESO (César Acuña) ---
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Seguridad", "Subtema": "Tecnología y Barrio Seguro",
            "Texto": "Implementación de sistemas de videovigilancia integrados y fortalecimiento del patrullaje municipal en coordinación con la PNP.",
            "Tipo": "Inversión"
        },
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Infraestructura", "Subtema": "Carreteras",
            "Texto": "Mejoramiento de la red vial nacional y caminos vecinales para conectar a los agricultores con los mercados.",
            "Tipo": "Obra"
        },
        
        # --- AVANZA PAÍS (Phillip Butters) ---
        {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Economía", "Subtema": "Libre Mercado",
            "Texto": "Defensa irrestricta de la propiedad privada y reducción del aparato estatal para fomentar la inversión privada.",
            "Tipo": "Política"
        }
    ]

    # --- LOGICA DE RELLENO (FALLBACK PROFESIONAL) ---
    # Lista de todos los candidatos actuales para asegurar que aparezcan en el selector
    todos_candidatos = [
        "Alfonso López-Chau", "César Acuña", "Carlos Álvarez", "Phillip Butters", 
        "Wolfgang Grozo", "Walter Chirinos", "Álvaro Paz de la Barra", "Herbert Caller", 
        "Armando Massé", "Mesías Guevara", "Roberto Sánchez", "Rafael Belaunde Llosa", 
        "Ricardo Belmont", "Alex González", "Javier Velázquez Quesquén", "Paul Jaimes", 
        "José Renynaldo", "Mario Vizcarra", "Rosario Fernández", "Miguel del Castillo", 
        "Morgan Quero", "Mariano González", "Fernando Olivera", "Vladimir Cerrón", 
        "José Luna Gálvez", "Yonhy Lescano", "Carlos Espá", "Jorge Nieto", 
        "Charlie Carrasco", "Fiorella Molinelli", "Roberto Chiabra", "Vicente Alanoca"
    ]

    ejes_principales = ["Economía", "Seguridad", "Salud", "Educación", "Gobernanza"]
    
    # Si el candidato no tiene propuestas específicas arriba, generamos el mensaje de "En proceso"
    candidatos_con_data = set(d['Candidato'] for d in data)
    
    for cand in todos_candidatos:
        if cand not in candidatos_con_data:
            for eje in ejes_principales:
                data.append({
                    "Candidato": cand,
                    "Partido": "N/A",
                    "Eje": eje,
                    "Subtema": "Información en Proceso",
                    "Texto": "El equipo técnico de Monitor Electoral está procesando el plan de gobierno oficial de este candidato para extraer sus propuestas principales en este eje. La información se actualizará en breve.",
                    "Tipo": "Pendiente"
                })

    return pd.DataFrame(data)
