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
    initial_sidebar_state="expanded", # Barra lateral abierta por defecto
    page_icon="🇵🇪"
)

# --- CSS PERSONALIZADO (ESTILO VISUAL) ---
def local_css():
    st.markdown("""
    <style>
        /* Importar fuente Inter (Estándar moderno) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #0F172A;
            background-color: #F8FAFC; /* Fondo gris muy suave */
        }
        
        /* Limpiar interfaz por defecto de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Ajuste del Sidebar nativo para que sea blanco puro */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        /* Estilos de Tarjetas (Cards) */
        .st-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #F1F5F9;
            margin-bottom: 20px;
        }

        /* CABECERA DEL SIDEBAR PERSONALIZADA */
        .sidebar-header {
            display: flex;
            align-items: center;
            padding: 20px 10px 30px 10px;
        }
        .sidebar-logo {
            width: 42px;
            height: 42px;
            background-color: #0F172A; /* Azul muy oscuro */
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 16px;
            margin-right: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .sidebar-content {
            display: flex;
            flex-direction: column;
        }
        .sidebar-main-title {
            font-weight: 700;
            font-size: 16px;
            color: #0F172A;
            line-height: 1.1;
        }
        .sidebar-subtitle {
            font-weight: 400;
            font-size: 13px;
            color: #64748B;
            margin-top: 2px;
        }
        
        /* Botón de perfil candidato */
        .btn-profile {
            display: inline-block;
            color: #2563EB;
            font-weight: 600;
            text-decoration: none;
            padding: 8px 16px;
            background: #EFF6FF;
            border-radius: 8px;
            font-size: 0.85rem;
            transition: background 0.2s;
        }
        .btn-profile:hover {
            background: #DBEAFE;
        }

        /* Estilo para items de lista de candidatos */
        .candidate-item {
            display: flex;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #F1F5F9;
        }
        .candidate-item:last-child {
            border-bottom: none;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. GESTIÓN DE DATOS ---
@st.cache_data(ttl=3600)
def load_data():
    # A. BANCO MUNDIAL (Datos reales)
    try:
        indicators = {
            'NY.GDP.MKTP.KD.ZG': 'Crecimiento PIB (%)',     
            'SL.UEM.TOTL.ZS': 'Desempleo Total (%)',        
            'SI.POV.NAHC': 'Pobreza Monetaria Nacional (%)',
        }
        end_year = datetime.datetime.now().year
        wb_data = wb.download(indicator=list(indicators.keys()), country=['PE'], start=2000, end=end_year)
        wb_data = wb_data.reset_index().rename(columns=indicators)
        wb_data['year'] = wb_data['year'].astype(int).sort_values()
        status_msg = "✅ En línea (Banco Mundial)"
    except:
        wb_data = pd.DataFrame(columns=['year', 'Crecimiento PIB (%)'])
        status_msg = "⚠️ Modo Offline"

    # B. DATOS SIMULADOS (Candidatos)
    # Usamos DiceBear API para generar avatares consistentes sin subir archivos
    df_candidatos = pd.DataFrame({
        'Nombre': ['Ana García', 'Luis Martínez', 'Carla Torres', 'Jorge Quispe', 'Elena Vasquez'],
        'Partido': ['Partido del Progreso', 'Frente Democrático', 'Renovación Nacional', 'Unidad Peruana', 'Alianza Futuro'],
        'Foto': [
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Ana&backgroundColor=b6e3f4', 
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Luis&backgroundColor=c0aede',
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Carla&backgroundColor=ffdfbf',
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Jorge&backgroundColor=d1d4f9',
            'https://api.dicebear.com/7.x/avataaars/svg?seed=Elena&backgroundColor=ffd5dc'
        ],
        'Link': ['#', '#', '#', '#', '#']
    })
    
    # C. DATOS SIMULADOS (Propuestas)
    df_propuestas = pd.DataFrame({
        'Candidato': ['Ana García', 'Luis Martínez', 'Carla Torres', 'Ana García', 'Luis Martínez'],
        'Eje': ['Salud', 'Salud', 'Seguridad', 'Economía', 'Economía'],
        'Subtema': ['Reforma del SIS', 'Telemedicina', 'Plan Bukele', 'Impuestos', 'Inversión Minera'],
        'Texto': [
            'Unificación del sistema de salud bajo un único pagador y digitalización al 100% de historias clínicas.',
            'Implementación de 5,000 postas médicas digitales en zonas rurales conectadas con internet satelital.',
            'Construcción de megacárceles de alta seguridad y reforma del código penal.',
            'Reducción temporal del IGV al 16% para reactivar el consumo.',
            'Desbloqueo inmediato de proyectos mineros con nuevo esquema de canon comunal.'
        ],
        'Tipo': ['Ley', 'Programa', 'Infraestructura', 'Decreto', 'Gestión']
    })

    # D. DATOS MANUALES (Indicadores que no están en WB API)
    years = np.arange(2018, 2025)
    df_manual = pd.DataFrame({
        'year': years,
        'Homicidios': [6.5, 6.8, 7.2, 8.1, 9.5, 10.2, 11.0], # Tendencia simulada
        'Victimizacion': [26.0, 26.5, 27.0, 22.0, 25.5, 28.0, 30.5]
    })
        
    return df_candidatos, df_propuestas, wb_data, df_manual, status_msg

df_candidatos, df_propuestas, df_wb, df_manual, status_msg = load_data()

# --- 3. HELPER FUNCTIONS (COMPONENTES VISUALES) ---

def render_sidebar_header():
    """Renderiza el encabezado del menú lateral igual a tu diseño"""
    st.sidebar.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-logo">ME</div>
            <div class="sidebar-content">
                <div class="sidebar-main-title">Monitor Electoral</div>
                <div class="sidebar-subtitle">Perú 2026</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, icon="📊"):
    st.markdown(f"""
    <div class="st-card" style="padding: 20px; text-align: center; height: 100%;">
        <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
        <div style="font-size: 0.85rem; color: #64748B; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">{label}</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: #0F172A; margin-top: 5px;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_section_header(title, subtitle):
    st.markdown(f"## {title}")
    st.markdown(f"<p style='color: #64748B; margin-top: -10px; margin-bottom: 25px;'>{subtitle}</p>", unsafe_allow_html=True)

# --- 4. VISTAS (PÁGINAS) ---

def view_inicio():
    render_section_header("Inicio", "Resumen general del estado del proceso electoral.")
    
    # KPIs Superiores
    c1, c2, c3 = st.columns(3)
    with c1: render_kpi_card("Días Restantes", "532", "⏳")
    with c2: render_kpi_card("Partidos Inscritos", "28", "🏛️")
    with c3: render_kpi_card("Estado Proceso", "Convocado", "✅")

    st.markdown("### Candidatos Destacados")
    st.markdown('<div class="st-card" style="padding: 0px;">', unsafe_allow_html=True)
    
    # Lista de candidatos limpia
    for _, row in df_candidatos.head(3).iterrows(): # Solo mostramos 3
        st.markdown(f"""
        <div class="candidate-item">
            <img src="{row['Foto']}" style="width: 48px; height: 48px; border-radius: 50%; margin-right: 16px; border: 1px solid #E2E8F0;">
            <div style="flex-grow: 1;">
                <h4 style="margin:0; font-size:1rem; font-weight: 600;">{row['Nombre']}</h4>
                <p style="margin:0; color: #64748B; font-size:0.85rem;">{row['Partido']}</p>
            </div>
            <a href="#" class="btn-profile">Ver Perfil</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def view_candidatos():
    render_section_header("Candidatos", "Directorio completo de aspirantes a la presidencia.")
    
    # Grid de tarjetas
    cols = st.columns(3)
    for idx, row in df_candidatos.iterrows():
        with cols[idx % 3]: # Distribuye en 3 columnas
            st.markdown(f"""
            <div class="st-card" style="text-align: center;">
                <img src="{row['Foto']}" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 15px;">
                <h4 style="margin:0; font-size:1.1rem;">{row['Nombre']}</h4>
                <p style="color: #64748B; font-size:0.9rem; margin-bottom: 15px;">{row['Partido']}</p>
                <a href="#" class="btn-profile" style="width: 100%; display: block; box-sizing: border-box;">Ver Plan de Gobierno</a>
            </div>
            """, unsafe_allow_html=True)

def view_planes():
    render_section_header("Planes de Gobierno", "Comparador inteligente de propuestas electorales.")
    
    # Selector Estilizado
    with st.container():
        st.markdown('<div class="st-card" style="padding: 20px;">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: selected_cand = st.selectbox("Seleccionar Candidato", df_propuestas['Candidato'].unique())
        with c2: selected_eje = st.selectbox("Seleccionar Eje Temático", df_propuestas['Eje'].unique())
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Resultados
    props = df_propuestas[(df_propuestas['Candidato'] == selected_cand) & (df_propuestas['Eje'] == selected_eje)]
    
    if not props.empty:
        for _, row in props.iterrows():
            st.markdown(f"""
            <div class="st-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="background:#EFF6FF; color:#2563EB; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600;">{row['Eje']}</span>
                    <span style="color:#64748B; font-size:0.8rem;">Tipo: {row['Tipo']}</span>
                </div>
                <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">{row['Subtema']}</h3>
                <p style="color: #334155; line-height: 1.6;">{row['Texto']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No se encontraron propuestas con los filtros seleccionados.")

def view_indicadores():
    render_section_header("Indicadores Nacionales", f"Datos clave para el contexto país. Fuente: {status_msg}")
    
    tabs = st.tabs(["💰 Economía", "🛡️ Seguridad", "🏥 Social"])
    
    with tabs[0]:
        st.markdown('<div class="st-card">', unsafe_allow_html=True)
        df_pib = df_wb.dropna(subset=['Crecimiento PIB (%)'])
        if not df_pib.empty:
            fig = px.line(df_pib, x='year', y='Crecimiento PIB (%)', title="Crecimiento del PBI (%)", template="plotly_white")
            fig.update_traces(line_color="#2563EB", line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tabs[1]:
        st.markdown('<div class="st-card">', unsafe_allow_html=True)
        fig = px.area(df_manual, x='year', y='Homicidios', title="Tasa de Homicidios (x 100k habitantes)", template="plotly_white")
        fig.update_traces(line_color="#EF4444", fillcolor="rgba(239, 68, 68, 0.1)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tabs[2]:
        st.markdown('<div class="st-card">', unsafe_allow_html=True)
        st.info("Datos sociales en desarrollo para esta vista.")
        st.markdown('</div>', unsafe_allow_html=True)

def view_participacion():
    render_section_header("Participación Ciudadana", "Tu voz es importante para mejorar la transparencia.")
    
    st.markdown("""
    <div class="st-card">
        <h3 style="margin-top:0;">Déjanos tu opinión</h3>
        <p style="color:#64748B;">¿Qué tema crees que falta discutir en la agenda electoral?</p>
        <form>
            <input type="text" placeholder="Tu nombre (Opcional)" style="width: 100%; padding: 12px; margin-bottom: 10px; border: 1px solid #E2E8F0; border-radius: 8px;">
            <textarea placeholder="Escribe tu comentario aquí..." style="width: 100%; padding: 12px; height: 100px; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 15px;"></textarea>
            <div style="text-align: right;">
                <a href="#" style="background-color: #0F172A; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600;">Enviar Comentario</a>
            </div>
        </form>
    </div>
    """, unsafe_allow_html=True)

def view_fuente():
    render_section_header("Fuente de Datos", "Transparencia sobre el origen de la información.")
    st.markdown('<div class="st-card">', unsafe_allow_html=True)
    st.json({
        "Indicadores Económicos": "API del Banco Mundial (Tiempo Real)",
        "Datos de Seguridad": "Estimaciones basadas en reportes históricos INEI",
        "Candidatos y Planes": "Jurado Nacional de Elecciones (Simulado para Demo)",
        "Desarrollo": "Streamlit + Python"
    })
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. NAVEGACIÓN Y MENU LATERAL (LA JOYA DEL DISEÑO) ---

# 1. Renderizamos el Header personalizado (Logo + Título)
render_sidebar_header()

# 2. Renderizamos el Menú con option_menu
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # Ocultamos el título nativo porque ya hicimos uno personalizado arriba
        options=["Inicio", "Candidatos", "Planes de Gobierno", "Indicadores Nacionales", "Participación Ciudadana", "Fuente de Datos"],
        icons=["house-door-fill", "people-fill", "file-text-fill", "bar-chart-fill", "chat-text-fill", "database-fill"], # Íconos de Bootstrap
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff"},
            "icon": {"color": "#64748B", "font-size": "16px"}, 
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "margin-bottom": "5px",
                "padding": "10px 15px",
                "color": "#334155",
                "font-weight": "500",
            },
            "nav-link-selected": {
                "background-color": "#EFF6FF",  # El fondo azul claro de tu imagen
                "color": "#2563EB",             # El texto azul fuerte de tu imagen
                "font-weight": "600",
                "border-left": "3px solid #2563EB"
            }
        }
    )
    
    # Pie de página del sidebar
    st.markdown("---")
    st.caption("© 2026 Monitor Electoral v2.1")

# 3. Enrutador de Vistas
if selected == "Inicio":
    view_inicio()
elif selected == "Candidatos":
    view_candidatos()
elif selected == "Planes de Gobierno":
    view_planes()
elif selected == "Indicadores Nacionales":
    view_indicadores()
elif selected == "Participación Ciudadana":
    view_participacion()
elif selected == "Fuente de Datos":
    view_fuente()
