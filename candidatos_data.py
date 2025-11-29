import pandas as pd
import base64
import os

def get_local_image_base64(filename):
    """
    Busca la imagen en la carpeta data/fotos/ y la convierte a Base64.
    Si no existe, retorna None.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'fotos', filename)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
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
    # Usamos un color neutral para los avatares
    return f"https://ui-avatars.com/api/?name={clean}&background=0F172A&color=fff&size=128&bold=true"

def obtener_data_candidatos():
    """
    Base de datos actualizada con la lista oficial de precandidatos 2026.
    Basado en información periodística reciente y registros del JNE.
    """
    
    raw_data = [
        # --- PARTIDOS CON PRECANDIDATOS DEFINIDOS ---
        {"Nombre": "Julio Chávez", "Partido": "Acción Popular", "Estado": "Precandidato (Lista 1)", "File": "julio_chavez.jpg"},
        {"Nombre": "Alfonso López-Chau", "Partido": "Ahora Nación", "Estado": "Precandidato Único", "File": "lopez_chau.jpg"},
        {"Nombre": "César Acuña", "Partido": "Alianza para el Progreso", "Estado": "Precandidato Único", "File": "cesar_acuna.jpg"},
        {"Nombre": "Carlos Álvarez", "Partido": "País para Todos", "Estado": "Precandidato Único", "File": "carlos_alvarez.jpg"},
        {"Nombre": "Phillip Butters", "Partido": "Avanza País", "Estado": "Precandidato Único", "File": "phillip_butters.jpg"},
        {"Nombre": "Wolfgang Grozo", "Partido": "Integridad Democrática", "Estado": "Precandidato", "File": "wolfgang_grozo.jpg"},
        {"Nombre": "Walter Chirinos", "Partido": "Partido Regionalista de Integración Nacional (PRIN)", "Estado": "Precandidato (Lista 1)", "File": "walter_chirinos.jpg"},
        {"Nombre": "Álvaro Paz de la Barra", "Partido": "Fe en el Perú", "Estado": "Precandidato Único", "File": "alvaro_paz.jpg"},
        {"Nombre": "Keiko Fujimori", "Partido": "Fuerza Popular", "Estado": "Precandidata Única", "File": "keiko_fujimori.jpg"},
        {"Nombre": "Herbert Caller", "Partido": "Partido Patriótico del Perú", "Estado": "Precandidato", "File": "herbert_caller.jpg"},
        {"Nombre": "Armando Massé", "Partido": "Partido Democrático Federal", "Estado": "Precandidato", "File": "armando_masse.jpg"},
        {"Nombre": "Mesías Guevara", "Partido": "Partido Morado", "Estado": "Precandidato (Lista 1)", "File": "mesias_guevara.jpg"},
        {"Nombre": "Roberto Sánchez", "Partido": "Juntos por el Perú", "Estado": "Precandidato", "File": "roberto_sanchez.jpg"},
        {"Nombre": "Rafael Belaunde Llosa", "Partido": "Libertad Popular", "Estado": "Precandidato", "File": "rafael_belaunde.jpg"},
        {"Nombre": "Ricardo Belmont", "Partido": "Partido Cívico Obras", "Estado": "Precandidato", "File": "ricardo_belmont.jpg"},
        {"Nombre": "Alex González", "Partido": "Partido Demócrata Verde", "Estado": "Precandidato", "File": "alex_gonzalez.jpg"},
        {"Nombre": "George Forsyth", "Partido": "Somos Perú", "Estado": "Precandidato", "File": "george_forsyth.jpg"},
        {"Nombre": "Javier Velázquez Quesquén", "Partido": "Partido Aprista Peruano", "Estado": "Precandidato (Lista 1)", "File": "javier_velazquez.jpg"}, # Se asume el primero mencionado
        {"Nombre": "Rafael López Aliaga", "Partido": "Renovación Popular", "Estado": "Precandidato Único", "File": "rafael_lopez_aliaga.jpg"},
        {"Nombre": "Paul Jaimes", "Partido": "Progresemos", "Estado": "Precandidato (Lista 1)", "File": "paul_jaimes.jpg"},
        {"Nombre": "José Renynaldo", "Partido": "Perú Moderno", "Estado": "Precandidato (Lista 1)", "File": "jose_renynaldo.jpg"},
        {"Nombre": "Mario Vizcarra", "Partido": "Perú Primero", "Estado": "Precandidato", "File": "mario_vizcarra.jpg"}, # Martín está inhabilitado, Mario es el presidente
        {"Nombre": "Rosario Fernández", "Partido": "Un Camino Diferente", "Estado": "Precandidata", "File": "rosario_fernandez.jpg"},
        {"Nombre": "Miguel del Castillo", "Partido": "Partido Primero La Gente", "Estado": "Precandidato (Lista 1)", "File": "miguel_del_castillo.jpg"},
        {"Nombre": "Morgan Quero", "Partido": "Partido Ciudadanos por el Perú", "Estado": "Precandidato", "File": "morgan_quero.jpg"},
        {"Nombre": "Mariano González", "Partido": "Salvemos al Perú", "Estado": "Precandidato", "File": "mariano_gonzalez.jpg"},
        {"Nombre": "Fernando Olivera", "Partido": "Frente de la Esperanza", "Estado": "Precandidato Único", "File": "fernando_olivera.jpg"},
        {"Nombre": "Vladimir Cerrón", "Partido": "Perú Libre", "Estado": "Precandidato (Prófugo)", "File": "vladimir_cerron.jpg"},
        {"Nombre": "José Luna Gálvez", "Partido": "Podemos Perú", "Estado": "Precandidato", "File": "jose_luna.jpg"},
        {"Nombre": "Yonhy Lescano", "Partido": "Cooperación Popular", "Estado": "Precandidato", "File": "yonhy_lescano.jpg"},
        {"Nombre": "Carlos Espá", "Partido": "Sí Creo", "Estado": "Precandidato", "File": "carlos_espa.jpg"},
        {"Nombre": "Jorge Nieto", "Partido": "Partido del Buen Gobierno", "Estado": "Precandidato", "File": "jorge_nieto.jpg"},
        {"Nombre": "Charlie Carrasco", "Partido": "Partido Demócrata Unido Perú", "Estado": "Precandidato", "File": "charlie_carrasco.jpg"},
        
        # --- ALIANZAS ---
        {"Nombre": "Fiorella Molinelli", "Partido": "Alianza Fuerza y Libertad", "Estado": "Precandidata (Alianza)", "File": "fiorella_molinelli.jpg"},
        {"Nombre": "Roberto Chiabra", "Partido": "Alianza Unidad Nacional", "Estado": "Precandidato (Alianza)", "File": "roberto_chiabra.jpg"},
        {"Nombre": "Vicente Alanoca", "Partido": "Alianza Venceremos", "Estado": "Precandidato (Alianza)", "File": "vicente_alanoca.jpg"},
    ]

    processed_data = []
    for item in raw_data:
        # 1. Intentar cargar imagen local (si existe en data/fotos/ con ese nombre)
        img_src = get_local_image_base64(item["File"])
        
        # 2. Si no existe archivo local, usar generador de avatar automático
        if img_src is None:
            img_src = get_avatar_fallback(item["Nombre"])
            
        processed_data.append({
            "Nombre": item["Nombre"],
            "Partido": item["Partido"],
            "Estado": item["Estado"],
            "Foto": img_src
        })
    
    return pd.DataFrame(processed_data)
