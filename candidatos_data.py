import pandas as pd
import base64
import os

def get_local_image_base64(filename):
    """
    Busca la imagen en la carpeta data/fotos/ y la convierte a Base64.
    Si no existe, retorna None.
    """
    # Construir ruta robusta (funciona en Windows, Mac y Linux/Streamlit Cloud)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'fotos', filename)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            
            # Detectar extensión para el header correcto
            ext = filename.split('.')[-1].lower()
            mime_type = "png" if ext == "png" else "jpeg"
            
            return f"data:image/{mime_type};base64,{encoded}"
        except Exception as e:
            print(f"Error leyendo imagen {filename}: {e}")
            return None
    return None

def get_avatar_fallback(name):
    """Generador de avatar si falla la imagen local"""
    clean = name.replace(" ", "+")
    return f"https://ui-avatars.com/api/?name={clean}&background=0F172A&color=fff&size=128&bold=true"

def obtener_data_candidatos():
    """
    Base de datos que lee IMÁGENES LOCALES.
    """
    
    # Mapeo: Nombre del Candidato -> Nombre del Archivo que debes subir
    # Si el archivo no está en la carpeta data/fotos/, saldrá el avatar de letras.
    raw_data = [
        # --- CANDIDATOS ---
        {"Nombre": "Keiko Fujimori", "Partido": "Fuerza Popular", "Estado": "Precandidata", "File": "keiko.jpg"},
        {"Nombre": "Rafael López Aliaga", "Partido": "Renovación Popular", "Estado": "Precandidato", "File": "rla.jpg"},
        {"Nombre": "Hernando de Soto", "Partido": "Progresemos", "Estado": "Precandidato", "File": "desoto.jpg"},
        {"Nombre": "César Acuña", "Partido": "Alianza para el Progreso", "Estado": "Precandidato", "File": "acuna.jpg"},
        {"Nombre": "Martín Vizcarra", "Partido": "Perú Primero", "Estado": "Inhabilitado", "File": "vizcarra.jpg"},
        {"Nombre": "Antauro Humala", "Partido": "A.N.T.A.U.R.O.", "Estado": "En proceso", "File": "antauro.jpg"},
        {"Nombre": "Roberto Sánchez", "Partido": "Juntos por el Perú", "Estado": "Precandidato", "File": "sanchez.jpg"},
        {"Nombre": "Susel Paredes", "Partido": "Primero la Gente", "Estado": "Precandidata", "File": "susel.jpg"},
        {"Nombre": "Álvaro Paz de la Barra", "Partido": "Fe en el Perú", "Estado": "Precandidato", "File": "paz.jpg"},
        {"Nombre": "Carlos Añaños", "Partido": "Perú Moderno", "Estado": "Por definir", "File": "ananos.jpg"},
        {"Nombre": "Alfonso López-Chau", "Partido": "Ahora Nación", "Estado": "Precandidato", "File": "lopez.jpg"},
        {"Nombre": "Rafael Belaunde", "Partido": "Libertad Popular", "Estado": "Precandidato", "File": "belaunde.jpg"},
        {"Nombre": "Fernando Cillóniz", "Partido": "PPC", "Estado": "Precandidato", "File": "cilloniz.jpg"},

        # --- PARTIDOS (Logos) ---
        {"Nombre": "Acción Popular", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_ap.png"},
        {"Nombre": "Partido Morado", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_morado.png"},
        {"Nombre": "APRA", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_apra.png"},
        {"Nombre": "Somos Perú", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_sp.png"},
        {"Nombre": "Avanza País", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_avanza.png"},
        {"Nombre": "Podemos Perú", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_podemos.png"},
        {"Nombre": "Frepap", "Partido": "Elección Interna", "Estado": "Por definir", "File": "logo_frepap.png"},
        
        # --- NUEVOS (Sin logo aún, usarán avatar automático) ---
        {"Nombre": "Salvemos al Perú", "Partido": "Inscrito", "Estado": "Por definir", "File": "x"},
        {"Nombre": "Sicuy", "Partido": "Inscrito", "Estado": "Por definir", "File": "x"},
        {"Nombre": "Principios", "Partido": "Inscrito", "Estado": "Por definir", "File": "x"},
        {"Nombre": "Pueblo Consciente", "Partido": "Inscrito", "Estado": "Por definir", "File": "x"}
    ]

    processed_data = []
    for item in raw_data:
        # 1. Intentar cargar imagen local
        img_src = get_local_image_base64(item["File"])
        
        # 2. Si no existe archivo local, usar generador de avatar
        if img_src is None:
            img_src = get_avatar_fallback(item["Nombre"])
            
        processed_data.append({
            "Nombre": item["Nombre"],
            "Partido": item["Partido"],
            "Estado": item["Estado"],
            "Foto": img_src
        })
    
    return pd.DataFrame(processed_data)
