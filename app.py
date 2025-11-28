import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import wb
import datetime
import numpy as np
from streamlit_option_menu import option_menu

# --- 1. CONFIGURACIÓN TÉCNICA ---
st.set_page_config(
    layout="wide", 
    page_title="Monitor Electoral Perú 2026",
    initial_sidebar_state="expanded",
    page_icon="🇵🇪"
)

# --- CSS PERSONALIZADO (REFINADO PARA IGUALAR TU IMAGEN) ---
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1E293B;
            background-color: #F8FAFC; 
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        /* Títulos Principales */
        h1 {
            font-weight: 800;
            color: #0F172A;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }
        .intro-text {
            color: #64748B;
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 2rem;
        }

        /* TARJETAS KPI (Estilo idéntico a la imagen) */
        .kpi-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            height: 100%;
        }
        .kpi-label {
            color: #64748B;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 8px;
        }
        .kpi-value {
            color: #0F172A;
            font-size: 1.5rem;
            font-weight: 700;
        }

        /* TABLA DE CANDIDATOS (Estilo "Vista Previa") */
        .table-header {
            display: flex;
            padding: 12px 16px;
            border-bottom: 1px solid #F1F5F9;
            background-color: #FAFAF9;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            margin-top: 20px;
        }
        .col-header {
            font-size: 0.75rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .candidate-row-clean {
            display: flex;
            align-items: center;
            padding: 16px;
            background-color: #FFFFFF;
            border-bottom: 1px solid #F1F5F9;
            transition: background 0.2s;
        }
        .candidate-row-clean:last-child {
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
            border-bottom: none; /* Quitar borde al último */
        }
        .candidate-row-clean:hover {
            background-color: #F8FAFC;
        }
        .cand-name {
            font-weight: 600;
            color: #0F172A;
            font-size: 0.95rem;
        }
        .cand-party {
            color: #64748B;
            font-size: 0.9rem;
        }
        .btn-link {
            color: #2563EB;
            font-weight: 600;
            font-size: 0.85rem;
            text-decoration: none;
            cursor: pointer;
        }

        /* VIDEO LIBRARY */
        .video-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        .video-title {
            padding: 12px 16px;
            font-weight: 600;
            font-size: 0.95rem;
            color: #0F172A;
            border-bottom: 1px solid #F1F5F9;
        }

        /* BOTTOM CARDS */
        .bottom-card {
            background: #FAFAFA;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .bottom-title {
            font-weight: 700;
            font-size: 0.95rem;
            color: #0F172A;
            margin-bottom: 5px;
        }
        .bottom-desc {
            font-size: 0.85rem;
            color: #64748B;
        }
        
        /* ESTILOS SIDEBAR (Ya aprobados) */
        .sidebar-header { padding: 20px 10px 30px 10px; display: flex; align-items: center; }
        .sidebar-logo { width: 40px; height: 40px; background: #0F172A; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; font-weight: bold; margin-right: 12px; }
        .sidebar-main-title { font-weight: 700; color: #0F172A; font-size: 15px; }
        .sidebar-subtitle { font-size: 12px; color: #64748B; }

    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. DATOS ---
@st.cache_data(ttl=3600)
def load_data():
    # WB Data
    try:
        indicators = {'NY.GDP.MKTP.KD.ZG': 'PIB', 'SL.UEM.TOTL.ZS': 'Desempleo', 'SI.POV.NAHC': 'Pobreza'}
        wb_data = wb.download(indicator=list(indicators.keys()), country=['PE'], start=2000, end=datetime.datetime.now().year)
        wb_data = wb_data.reset_index().rename(columns=indicators).sort_values('year')
        status = "✅ Online"
    except:
        wb_data = pd.DataFrame()
        status = "⚠️ Offline"

    # Candidatos (Datos para la tabla visual)
    df_cand = pd.DataFrame({
        'Nombre': ['Ana García', 'Luis Martínez', 'Carla Torres', 'Jorge Quispe'],
        'Partido': ['Partido del Progreso', 'Frente Democrático', 'Renovación Nacional', 'Unidad Peruana'],
        'Foto': [
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Ana&backgroundColor=b6e3f4', 
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Luis&backgroundColor=c0aede',
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Carla&backgroundColor=ffdfbf',
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Jorge&backgroundColor=d1d4f9'
        ]
    })
    
    # Propuestas Dummy
    df_prop = pd.DataFrame({
        'Candidato': ['Ana García', 'Luis Martínez'],
        'Eje': ['Salud', 'Seguridad'],
        'Texto': ['Hospitales digitales...', 'Cárceles de alta seguridad...'],
        'Subtema': ['Telemedicina', 'Crimen Organizado'],
        'Tipo': ['Programa', 'Ley']
    })

    # Manual Data
    df_man = pd.DataFrame({'year': np.arange(2018,2025), 'Homicidios': [6,7,8,9,10,11,12]})
    
    return df_cand, df_prop, wb_data, df_man, status

df_cand, df_prop, df_wb, df_man, status_msg = load_data()

# --- 3. COMPONENTES VISUALES ---

def kpi_box(label, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_candidate_table_row(img, name, party):
    st.markdown(f"""
    <div class="candidate-row-clean">
        <div style="width: 50px; margin-right: 15px;">
            <img src="{img}" style="width: 40px; height: 40px; border-radius: 50%;">
        </div>
        <div style="width: 30%;">
            <div class="cand-name">{name}</div>
        </div>
        <div style="width: 50%;">
            <div class="cand-party">{party}</div>
        </div>
        <div style="width: 20%; text-align: right;">
            <a href="#" class="btn-link">Ver Perfil</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_bottom_card(title, desc):
    st.markdown(f"""
    <div class="bottom-card">
        <div class="bottom-title">{title}</div>
        <div class="bottom-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. VISTAS ---

def view_inicio():
    # 1. TÍTULO Y TEXTO INTRODUCTORIO
    st.markdown("# Monitor Electoral Perú 2026")
    st.markdown("<div style='color:#64748B; margin-top:-10px; margin-bottom:20px;'>Tu plataforma para un voto informado.</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
    Bienvenido a Monitor Electoral Perú 2026. Nuestra misión es centralizar y simplificar el acceso a la información electoral, 
    promoviendo la transparencia y la participación ciudadana informada para las próximas elecciones.
    </div>
    """, unsafe_allow_html=True)

    # 2. TARJETAS KPI (ESTILO IMAGEN)
    c1, c2, c3 = st.columns(3)
    with c1: kpi_box("Enlaces Oficiales", "JNE, ONPE")
    with c2: kpi_box("Partidos en Carrera", "15")
    with c3: kpi_box("Días para la elección", "720") # Valor estático como en tu imagen, o usa calc dinámica
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 3. TABLA DE CANDIDATOS (VISTA PREVIA)
    st.markdown("### Candidatos Presidenciales (Vista Previa)")
    
    # Header de la tabla (Falso, hecho con CSS)
    st.markdown("""
    <div class="table-header">
        <div style="width: 50px; margin-right: 15px;"></div>
        <div class="col-header" style="width: 30%;">Candidato</div>
        <div class="col-header" style="width: 50%;">Partido Político</div>
        <div class="col-header" style="width: 20%; text-align: right;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filas de la tabla (Contenedor blanco con bordes)
    st.markdown('<div style="background: white; border: 1px solid #E2E8F0; border-top: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">', unsafe_allow_html=True)
    for _, row in df_cand.head(3).iterrows():
        render_candidate_table_row(row['Foto'], row['Nombre'], row['Partido'])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. BIBLIOTECA DE VIDEOS
    st.markdown("### Biblioteca de Videos")
    
    col_vid1, col_vid2 = st.columns(2)
    
    with col_vid1:
        st.markdown('<div class="video-card">', unsafe_allow_html=True)
        st.markdown('<div class="video-title">🗳️ Cédula de votación y cómo votar</div>', unsafe_allow_html=True)
        # Video A (ONPE)
        st.video("https://www.youtube.com/watch?v=cJ5UuJJRfNQ")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_vid2:
        st.markdown('<div class="video-card">', unsafe_allow_html=True)
        st.markdown('<div class="video-title">🚫 #EleccionesSinFake | 6 recomendaciones</div>', unsafe_allow_html=True)
        # Video B (Fake News)
        st.video("https://www.youtube.com/watch?v=n44WJaYtZrs")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. TARJETAS INFERIORES (TEXTO)
    c_bottom1, c_bottom2 = st.columns(2)
    with c_bottom1:
        render_bottom_card("Análisis de Propuestas Electorales", "Expertos debaten los planes de gobierno.")
    with c_bottom2:
        render_bottom_card("¿Cómo funciona el Voto Electrónico?", "Una guía paso a paso para el elector.")


# --- VISTAS SECUNDARIAS (SIMPLIFICADAS PARA AHORRAR ESPACIO) ---
def view_planes():
    st.title("Planes de Gobierno")
    st.info("Sección en construcción...")

def view_indicadores():
    st.title("Indicadores Nacionales")
    st.plotly_chart(px.line(df_wb, x='year', y='PIB', title="PIB"), use_container_width=True)

def view_participacion():
    st.title("Participación")
    st.text_area("Deja tu comentario")

def view_fuente():
    st.json({"Fuente": "Banco Mundial + JNE"})

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">ME</div>
        <div>
            <div class="sidebar-main-title">Monitor Electoral</div>
            <div class="sidebar-subtitle">Perú 2026</div>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Inicio", "Candidatos", "Planes de Gobierno", "Indicadores Nacionales", "Participación Ciudadana", "Fuente de Datos"],
        icons=["house-door-fill", "people-fill", "file-text-fill", "bar-chart-fill", "chat-text-fill", "database-fill"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff"},
            "icon": {"color": "#64748B", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "padding": "10px 15px", "color": "#334155"},
            "nav-link-selected": {"background-color": "#EFF6FF", "color": "#2563EB", "font-weight": "600", "border-left": "3px solid #2563EB"}
        }
    )
    st.markdown("---")
    st.caption("© 2026 Monitor Electoral")

# ROUTER
if selected == "Inicio": view_inicio()
elif selected == "Candidatos": view_inicio() # Reusamos vista inicio por ahora
elif selected == "Planes de Gobierno": view_planes()
elif selected == "Indicadores Nacionales": view_indicadores()
elif selected == "Participación Ciudadana": view_participacion()
elif selected == "Fuente de Datos": view_fuente()
