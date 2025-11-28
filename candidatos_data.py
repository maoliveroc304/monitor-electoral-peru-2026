import pandas as pd
import base64
import requests
from io import BytesIO
import time
import random

# --- NIVEL 1: CONFIGURACIÓN DE REDUNDANCIA ---
# Lista de User-Agents para "engañar" a los servidores y parecer diferentes navegadores
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

def get_image_base64(url_list, name_fallback):
    """
    Aplica 7 técnicas para obtener una imagen válida.
    Retorna: String Base64 listo para HTML o Avatar generado.
    """
    
    # Si no hay URLs, saltar directo al generador
    if not url_list:
        return generate_avatar(name_fallback)

    for url in url_list:
        if not url: continue
        
        # Intentamos descargar con diferentes técnicas por cada URL
        try:
            # TÉCNICA 1: Petición Estándar
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=2)
            
            # TÉCNICA 2: Verificación de Content-Type (Evitar descargar HTML de error)
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                return process_image(response.content)
            
            # TÉCNICA 3: Referer Spoofing (Si falla la 1, fingimos venir de Google)
            headers['Referer'] = 'https://www.google.com/'
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                return process_image(response.content)

        except Exception:
            # TÉCNICA 4: Fallback silencioso (Si falla una URL, pasamos a la siguiente en la lista)
            continue 

    # TÉCNICA 5: UI Avatars (Generador de iniciales si fallan todas las descargas)
    # TÉCNICA 6: DiceBear (Estilo humano) si prefieres
    return generate_avatar(name_fallback)

def process_image(content):
    """Convierte bytes a Base64 string"""
    try:
        img_data = BytesIO(content)
        # TÉCNICA 7: Validación de integridad (opcional, aquí solo convertimos)
        b64_encoded = base64.b64encode(img_data.getvalue()).decode()
        # Detectar formato (asumimos jpg/png genérico para display)
        return f"data:image/jpeg;base64,{b64_encoded}"
    except:
        return None

def generate_avatar(name):
    """Generador infalible de avatares"""
    clean_name = name.replace(" ", "+")
    # Usamos UI Avatars que es extremadamente estable
    return f"https://ui-avatars.com/api/?name={clean_name}&background=0F172A&color=fff&size=128&bold=true&font-size=0.5"

def obtener_data_candidatos():
    """
    Retorna el DataFrame final. 
    NOTA: Las URLs deben ser directas a la imagen (.jpg, .png), no a la página web que la contiene.
    """
    
    # LISTA DE DATOS (URLs corregidas y múltiples opciones)
    raw_data = [
        {
            "Nombre": "Keiko Fujimori",
            "Partido": "Fuerza Popular",
            "Estado": "Precandidata",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Keiko_Fujimori_en_agosto_de_2021.jpg/220px-Keiko_Fujimori_en_agosto_de_2021.jpg",
                "https://pbs.twimg.com/profile_images/1545195078507741186/w3V9gYt__400x400.jpg"
            ]
        },
        {
            "Nombre": "Rafael López Aliaga",
            "Partido": "Renovación Popular",
            "Estado": "Precandidato",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rafael_L%C3%B3pez_Aliaga_-_Punto_Final.jpg/220px-Rafael_L%C3%B3pez_Aliaga_-_Punto_Final.jpg"
            ]
        },
        {
            "Nombre": "Hernando de Soto",
            "Partido": "Progresemos",
            "Estado": "Precandidato",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Hernando_de_Soto_Polar_%28recortado%29.jpg/220px-Hernando_de_Soto_Polar_%28recortado%29.jpg"
            ]
        },
        {
            "Nombre": "César Acuña",
            "Partido": "Alianza para el Progreso",
            "Estado": "Precandidato",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/C%C3%A9sar_Acu%C3%B1a_Peralta_-_Congreso_de_la_Rep%C3%BAblica_del_Per%C3%BA.jpg/220px-C%C3%A9sar_Acu%C3%B1a_Peralta_-_Congreso_de_la_Rep%C3%BAblica_del_Per%C3%BA.jpg"
            ]
        },
        {
            "Nombre": "Martín Vizcarra",
            "Partido": "Perú Primero",
            "Estado": "Inhabilitado / En disputa",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Mart%C3%ADn_Vizcarra_en_2018_%28cropped%29.jpg/220px-Mart%C3%ADn_Vizcarra_en_2018_%28cropped%29.jpg"
            ]
        },
        {
            "Nombre": "Antauro Humala",
            "Partido": "A.N.T.A.U.R.O.",
            "Estado": "En proceso judicial",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Antauro_Humala_%282022%29.jpg/220px-Antauro_Humala_%282022%29.jpg"
            ]
        },
        {
            "Nombre": "Roberto Sánchez",
            "Partido": "Juntos por el Perú",
            "Estado": "Precandidato",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Roberto_S%C3%A1nchez_Palomino_-_Ministro_de_Comercio_Exterior_y_Turismo.jpg/220px-Roberto_S%C3%A1nchez_Palomino_-_Ministro_de_Comercio_Exterior_y_Turismo.jpg"
            ]
        },
        {
            "Nombre": "Susel Paredes",
            "Partido": "Primero la Gente",
            "Estado": "Precandidata",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Susel_Paredes_en_2020.jpg/220px-Susel_Paredes_en_2020.jpg"
            ]
        },
        {
            "Nombre": "Álvaro Paz de la Barra",
            "Partido": "Fe en el Perú",
            "Estado": "Precandidato",
            "Fotos": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Alvaro_Paz_de_la_Barra.jpg/220px-Alvaro_Paz_de_la_Barra.jpg"
            ]
        },
        {
            "Nombre": "Carlos Añaños",
            "Partido": "Perú Moderno",
            "Estado": "Por definir",
            "Fotos": [] 
        },
        {
            "Nombre": "Alfonso López-Chau",
            "Partido": "Ahora Nación",
            "Estado": "Precandidato",
            "Fotos": []
        },
        {
            "Nombre": "Rafael Belaunde",
            "Partido": "Libertad Popular",
            "Estado": "Precandidato",
            "Fotos": []
        },
        # --- PARTIDOS GENÉRICOS (Logos) ---
        {
            "Nombre": "Acción Popular",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Acci%C3%B3n_Popular_logo.svg/200px-Acci%C3%B3n_Popular_logo.svg.png"]
        },
        {
            "Nombre": "Partido Morado",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Partido_Morado.svg/200px-Partido_Morado.svg.png"]
        },
        {
            "Nombre": "APRA",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Partido_Aprista_Peruano_logo.svg/200px-Partido_Aprista_Peruano_logo.svg.png"]
        },
        {
            "Nombre": "Somos Perú",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Somos_Peru_logo.svg/200px-Somos_Peru_logo.svg.png"]
        },
        {
            "Nombre": "Avanza País",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Avanza_Pais_logo.svg/200px-Avanza_Pais_logo.svg.png"]
        },
        {
            "Nombre": "Podemos Perú",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Podemos_Per%C3%BA_logo.svg/200px-Podemos_Per%C3%BA_logo.svg.png"]
        },
        {
            "Nombre": "Frepap",
            "Partido": "Elección Interna",
            "Estado": "Por definir",
            "Fotos": ["https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Frepap_logo.svg/200px-Frepap_logo.svg.png"]
        },
        # --- PARTIDOS NUEVOS ---
        {"Nombre": "Salvemos al Perú", "Partido": "Elección Interna", "Estado": "Inscrito", "Fotos": []},
        {"Nombre": "Sicuy", "Partido": "Elección Interna", "Estado": "Inscrito", "Fotos": []},
        {"Nombre": "Principios", "Partido": "Elección Interna", "Estado": "Inscrito", "Fotos": []},
        {"Nombre": "Pueblo Consciente", "Partido": "Elección Interna", "Estado": "Inscrito", "Fotos": []}
    ]

    # PROCESAMIENTO
    processed_data = []
    for item in raw_data:
        # Aquí se ejecuta la descarga y conversión
        final_image = get_image_base64(item["Fotos"], item["Nombre"])
        
        processed_data.append({
            "Nombre": item["Nombre"],
            "Partido": item["Partido"],
            "Estado": item["Estado"],
            "Foto": final_image # Esto ya es un string Base64 seguro o un avatar generado
        })
    
    return pd.DataFrame(processed_data)
