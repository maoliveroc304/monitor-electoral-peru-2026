import pandas as pd

def obtener_data_candidatos():
    """
    Retorna el DataFrame con la información real de los partidos y sus precandidatos
    basado en las fichas del JNE y reportes de prensa (Fuente: Imágenes proporcionadas).
    """
    data = [
        {
            "Nombre": "Keiko Fujimori",
            "Partido": "Fuerza Popular",
            "Estado": "Precandidata Única",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Keiko_Fujimori_en_agosto_de_2021.jpg/220px-Keiko_Fujimori_en_agosto_de_2021.jpg"
        },
        {
            "Nombre": "Rafael López Aliaga",
            "Partido": "Renovación Popular",
            "Estado": "Precandidato Único",
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
            "Estado": "Precandidato Único",
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
            "Nombre": "Alfonso López-Chau",
            "Partido": "Ahora Nación",
            "Estado": "Precandidato",
            "Foto": "https://e.rpp-noticias.io/xlarge/2023/07/19/292729_1452932.webp" # Fuente RPP
        },
        {
            "Nombre": "Susel Paredes",
            "Partido": "Primero la Gente",
            "Estado": "Precandidata",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Susel_Paredes_en_2020.jpg/220px-Susel_Paredes_en_2020.jpg"
        },
        {
            "Nombre": "Rafael Belaunde",
            "Partido": "Libertad Popular",
            "Estado": "Precandidato",
            "Foto": "https://img.canaln.pe/s/files/styles/landscape_1024/public/2020/07/15/5f0f393345436d000a684f04.jpg" 
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
            "Foto": "https://via.placeholder.com/150?text=CA" # Placeholder temporal
        },
        {
            "Nombre": "Por definir (Elección Interna)",
            "Partido": "Acción Popular",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Acci%C3%B3n_Popular_logo.svg/100px-Acci%C3%B3n_Popular_logo.svg.png"
        },
        {
            "Nombre": "Por definir (Elección Interna)",
            "Partido": "Partido Morado",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Partido_Morado.svg/100px-Partido_Morado.svg.png"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Partido Aprista Peruano",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Partido_Aprista_Peruano_logo.svg/100px-Partido_Aprista_Peruano_logo.svg.png"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Somos Perú",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Somos_Peru_logo.svg/100px-Somos_Peru_logo.svg.png"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Podemos Perú",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Podemos_Per%C3%BA_logo.svg/100px-Podemos_Per%C3%BA_logo.svg.png"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Avanza País",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Avanza_Pais_logo.svg/100px-Avanza_Pais_logo.svg.png"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Frepap",
            "Estado": "Sin candidato oficial",
            "Foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Frepap_logo.svg/100px-Frepap_logo.svg.png"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Salvemos al Perú",
            "Estado": "Sin candidato oficial",
            "Foto": "https://api.dicebear.com/7.x/initials/svg?seed=SP"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Sicuy",
            "Estado": "Sin candidato oficial",
            "Foto": "https://api.dicebear.com/7.x/initials/svg?seed=SI"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Principios",
            "Estado": "Sin candidato oficial",
            "Foto": "https://api.dicebear.com/7.x/initials/svg?seed=PR"
        },
        {
            "Nombre": "Por definir",
            "Partido": "Pueblo Consciente",
            "Estado": "Sin candidato oficial",
            "Foto": "https://api.dicebear.com/7.x/initials/svg?seed=PC"
        }
    ]
    
    return pd.DataFrame(data)
