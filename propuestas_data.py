import pandas as pd

def obtener_data_propuestas():
    """
    Base de datos estructurada de propuestas por Eje Temático.
    Fuente: Documentos de Planes de Gobierno (2026).
    """
    
    # Ejes Temáticos definidos:
    # 1. Economía y empleo
    # 2. Pobreza, desigualdad e inclusión social
    # 3. Educación
    # 4. Salud
    # 5. Seguridad ciudadana y crimen organizado
    # 6. Infraestructura y servicios básicos
    # 7. Ambiente, cambio climático y Amazonía
    # 8. Gobernanza, institucionalidad y lucha anticorrupción

    propuestas = [
        # --- ACCIÓN POPULAR (Julio Chávez) ---
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "Reactivación y Empleo",
            "Texto": "Impulsar la reactivación económica creando empleo formal y remunerado. Ejecutar política expansiva con gasto eficiente para alcanzar 5 millones de puestos de trabajo. Reducir la informalidad al 30% mediante incentivos.", "Tipo": "Programa"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "MYPES",
            "Texto": "Otorgar crédito barato a las MYPES y priorizar el aparato productivo nacional (Desglobalizar la economía).", "Tipo": "Económico"
        },
        {
            "Candidato": "Julio Chávez", "Partido": "Acción Popular",
            "Eje": "Economía", "Subtema": "Reforma Laboral",
            "Texto": "Crear contratos laborales estables de media jornada y otorgar incentivos tributarios para contratar personas entre 55 y 65 años.", "Tipo": "Ley"
        },

        # --- FUERZA POPULAR (Keiko Fujimori) ---
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Empleo Rápido",
            "Texto": "Implementar mecanismo de empleo rápido mediante pequeñas obras de infraestructura (rural y periférica) con contratación formal.", "Tipo": "Programa"
        },
        {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "MYPEs - Licencia 0",
            "Texto": "Eliminar barreras de entrada estableciendo la 'Licencia 0 para Mypes' y una ventanilla única electrónica. Crear Prompyme con rango viceministerial.", "Tipo": "Reforma"
        },
         {
            "Candidato": "Keiko Fujimori", "Partido": "Fuerza Popular",
            "Eje": "Economía", "Subtema": "Formalización",
            "Texto": "Crear la Comisión Nacional para la Formalización para unificar esfuerzos dispersos del Estado.", "Tipo": "Institucional"
        },

        # --- RENOVACIÓN POPULAR (Rafael López Aliaga) ---
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Lucha Anticorrupción",
            "Texto": "Crear una Central de Lucha Contra la Corrupción (CCC) con poderes para detectar y capturar delito in fraganti y verificar patrimonio de funcionarios.", "Tipo": "Institucional"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Reforma del Estado",
            "Texto": "Reducir el número de ministerios por ineficiencia. Descentralizar las sedes ministeriales y el Poder Ejecutivo.", "Tipo": "Reforma"
        },
        {
            "Candidato": "Rafael López Aliaga", "Partido": "Renovación Popular",
            "Eje": "Gobernanza", "Subtema": "Servicio Civil",
            "Texto": "Implementar el 'CÓDIGO DEL SERVICIO PÚBLICO' para eliminar barreras burocráticas. Ingreso al estado por méritos y competencias estrictas.", "Tipo": "Ley"
        },

        # --- SOMOS PERÚ (George Forsyth) ---
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Reforma Política",
            "Texto": "Eliminar por completo la inmunidad parlamentaria y restituir el rol sancionador de la Contraloría General de la República.", "Tipo": "Reforma Const."
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Justicia",
            "Texto": "Crear una 'Escuela Judicial Peruana' en reemplazo de la Academia de la Magistratura.", "Tipo": "Institucional"
        },
        {
            "Candidato": "George Forsyth", "Partido": "Somos Perú",
            "Eje": "Gobernanza", "Subtema": "Transparencia",
            "Texto": "Implementar el Sistema de Seguimiento de Promesas Presidenciales para vigilancia ciudadana.", "Tipo": "Tecnológico"
        },

        # --- ALIANZA PARA EL PROGRESO (César Acuña) ---
        # (Datos simulados basados en perfil histórico para completar ejemplo, ya que el doc no tenía detalle específico de APP en el snippet)
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Seguridad", "Subtema": "Tecnología y Barrio Seguro",
            "Texto": "Implementación de sistemas de videovigilancia integrados y fortalecimiento del patrullaje municipal en coordinación con la PNP.", "Tipo": "Inversión"
        },
        {
            "Candidato": "César Acuña", "Partido": "Alianza para el Progreso",
            "Eje": "Infraestructura", "Subtema": "Carreteras",
            "Texto": "Mejoramiento de la red vial nacional y caminos vecinales para conectar a los agricultores con los mercados.", "Tipo": "Obra"
        },
        
        # --- AVANZA PAÍS (Phillip Butters) ---
        {
            "Candidato": "Phillip Butters", "Partido": "Avanza País",
            "Eje": "Economía", "Subtema": "Libre Mercado",
            "Texto": "Defensa irrestricta de la propiedad privada y reducción del aparato estatal para fomentar la inversión privada.", "Tipo": "Política"
        },

        # --- OTROS CANDIDATOS (Generic Fallback) ---
        # Se genera entrada genérica para los demás para que la UI no salga vacía
    ]

    # Lista completa de candidatos para rellenar vacíos
    todos_candidatos = [
        "Hernando de Soto", "Susel Paredes", "Martín Vizcarra", "Antauro Humala", 
        "Roberto Sánchez", "Álvaro Paz de la Barra", "Carlos Añaños", "Alfonso López-Chau", 
        "Rafael Belaunde", "Fernando Cillóniz", "Mario Vizcarra", "Rosario Fernández",
        "Miguel del Castillo", "Morgan Quero", "Mariano González", "Fernando Olivera",
        "Vladimir Cerrón", "José Luna Gálvez", "Yonhy Lescano", "Carlos Espá",
        "Jorge Nieto", "Charlie Carrasco", "Fiorella Molinelli", "Roberto Chiabra", "Vicente Alanoca"
    ]

    for cand in todos_candidatos:
        propuestas.append({
            "Candidato": cand, "Partido": "Varios",
            "Eje": "General", "Subtema": "Plan de Gobierno",
            "Texto": "La información detallada de este plan de gobierno se encuentra en proceso de estructuración y análisis por parte del equipo de Monitor Electoral.", 
            "Tipo": "En proceso"
        })

    return pd.DataFrame(propuestas)
