import pandas as pd

def obtener_data_candidatos():
    """
    Base de datos de precandidatos y partidos para las Elecciones 2026.
    Fuente de imágenes: Wikimedia Commons (Estables) y UI Avatars (Backup).
    """
    
    # Función auxiliar para generar avatar con iniciales si no hay foto
    def get_placeholder(name):
        return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random&color=fff&size=128"

    data = [
        # --- CANDIDATOS DEFINIDOS / VOCEADOS ---
        {
            "Nombre": "Keiko Fujimori",
            "Partido": "Fuerza Popular",
            "Estado": "Precandidata",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Keiko_Fujimori_en_agosto_de_2021.jpg/220px-Keiko_Fujimori_en_agosto_de_2021.jpg"
        },
        {
            "Nombre": "Rafael López Aliaga",
            "Partido": "Renovación Popular",
            "Estado": "Precandidato",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rafael_L%C3%B3pez_Aliaga_-_Punto_Final.jpg/220px-Rafael_L%C3%B3pez_Aliaga_-_Punto_Final.jpg"
        },
        {
            "Nombre": "Hernando de Soto",
            "Partido": "Progresemos",
            "Estado": "Precandidato",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Hernando_de_Soto_Polar_%28recortado%29.jpg/220px-Hernando_de_Soto_Polar_%28recortado%29.jpg"
        },
        {
            "Nombre": "César Acuña",
            "Partido": "Alianza para el Progreso",
            "Estado": "Precandidato",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/C%C3%A9sar_Acu%C3%B1a_Peralta_-_Congreso_de_la_Rep%C3%BAblica_del_Per%C3%BA.jpg/220px-C%C3%A9sar_Acu%C3%B1a_Peralta_-_Congreso_de_la_Rep%C3%BAblica_del_Per%C3%BA.jpg"
        },
        {
            "Nombre": "Martín Vizcarra",
            "Partido": "Perú Primero",
            "Estado": "Inhabilitado / En disputa",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Mart%C3%ADn_Vizcarra_en_2018_%28cropped%29.jpg/220px-Mart%C3%ADn_Vizcarra_en_2018_%28cropped%29.jpg"
        },
        {
            "Nombre": "Roberto Sánchez",
            "Partido": "Juntos por el Perú",
            "Estado": "Precandidato",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Roberto_S%C3%A1nchez_Palomino_-_Ministro_de_Comercio_Exterior_y_Turismo.jpg/220px-Roberto_S%C3%A1nchez_Palomino_-_Ministro_de_Comercio_Exterior_y_Turismo.jpg"
        },
        {
            "Nombre": "Susel Paredes",
            "Partido": "Primero la Gente",
            "Estado": "Precandidata",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Susel_Paredes_en_2020.jpg/220px-Susel_Paredes_en_2020.jpg"
        },
        {
            "Nombre": "Álvaro Paz de la Barra",
            "Partido": "Fe en el Perú",
            "Estado": "Precandidato",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Alvaro_Paz_de_la_Barra.jpg/220px-Alvaro_Paz_de_la_Barra.jpg"
        },
        {
            "Nombre": "Antauro Humala",
            "Partido": "A.N.T.A.U.R.O.",
            "Estado": "En proceso judicial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Antauro_Humala_%282022%29.jpg/220px-Antauro_Humala_%282022%29.jpg"
        },
        {
            "Nombre": "Carlos Añaños",
            "Partido": "Perú Moderno",
            "Estado": "Renunciante / Por definir",
            "Foto": get_placeholder("Carlos Añaños") # Sin foto estable en commons
        },
        {
            "Nombre": "Alfonso López-Chau",
            "Partido": "Ahora Nación",
            "Estado": "Precandidato",
            "Foto": get_placeholder("Alfonso Lopez")
        },
        {
            "Nombre": "Rafael Belaunde",
            "Partido": "Libertad Popular",
            "Estado": "Precandidato",
            "Foto": get_placeholder("Rafael Belaunde")
        },

        # --- PARTIDOS SIN CANDIDATO CLARO (POR DEFINIR) ---
        {
            "Nombre": "Por Definir (AP)",
            "Partido": "Acción Popular",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Acci%C3%B3n_Popular_logo.svg/200px-Acci%C3%B3n_Popular_logo.svg.png"
        },
        {
            "Nombre": "Por Definir (Morado)",
            "Partido": "Partido Morado",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Partido_Morado.svg/200px-Partido_Morado.svg.png"
        },
        {
            "Nombre": "Por Definir (APRA)",
            "Partido": "Partido Aprista Peruano",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Partido_Aprista_Peruano_logo.svg/200px-Partido_Aprista_Peruano_logo.svg.png"
        },
        {
            "Nombre": "Por Definir (SP)",
            "Partido": "Somos Perú",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Somos_Peru_logo.svg/200px-Somos_Peru_logo.svg.png"
        },
        {
            "Nombre": "Por Definir (PP)",
            "Partido": "Podemos Perú",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Podemos_Per%C3%BA_logo.svg/200px-Podemos_Per%C3%BA_logo.svg.png"
        },
        {
            "Nombre": "Por Definir (Avanza)",
            "Partido": "Avanza País",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Avanza_Pais_logo.svg/200px-Avanza_Pais_logo.svg.png"
        },
        {
            "Nombre": "Por Definir (Frepap)",
            "Partido": "Frepap",
            "Estado": "Elección Interna",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Frepap_logo.svg/200px-Frepap_logo.svg.png"
        },
        
        # --- PARTIDOS NUEVOS (Sin logo en Commons, usamos Placeholder Limpio) ---
        {"Nombre": "Por Definir 1", "Partido": "Salvemos al Perú", "Estado": "Inscrito", "Foto": get_placeholder("Salvemos Perú")},
        {"Nombre": "Por Definir 2", "Partido": "Sicuy", "Estado": "Inscrito", "Foto": get_placeholder("Sicuy")},
        {"Nombre": "Por Definir 3", "Partido": "Principios", "Estado": "Inscrito", "Foto": get_placeholder("Principios")},
        {"Nombre": "Por Definir 4", "Partido": "Pueblo Consciente", "Estado": "Inscrito", "Foto": get_placeholder("Pueblo Consciente")}
    ]
    
    return pd.DataFrame(data)
