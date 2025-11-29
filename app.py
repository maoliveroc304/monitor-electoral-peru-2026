import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import wb
import datetime
import numpy as np
import os
from streamlit_option_menu import option_menu

# IMPORTAR DATOS EXTERNOS
try:
    from candidatos_data import obtener_data_candidatos
except ImportError:
    def obtener_data_candidatos():
        return pd.DataFrame({'Nombre': [], 'Partido': [], 'Foto': []})

# --- 1. CONFIGURACIÓN TÉCNICA ---
st.set_page_config(
    layout="wide", 
    page_title="Monitor Electoral Perú 2026",
    initial_sidebar_state="expanded",
    page_icon="🇵🇪"
)

# --- CSS PERSONALIZADO ---
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

        /* Títulos */
        h1 { font-weight: 800; color: #0F172A; font-size: 2.2rem; margin-bottom: 0.5rem; }
        .intro-text { color: #64748B; font-size: 1rem; line-height: 1.6; margin-bottom: 2rem; }

        /* KPI CARDS */
        .kpi-card {
            background-color: #FFFFFF; padding: 20px; border-radius: 12px;
            border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            height: 100%; display: flex; flex-direction: column; justify-content: center;
        }
        .kpi-label { color: #64748B; font-size: 0.85rem; font-weight: 500; margin-bottom: 8px; }
        .kpi-value { color: #0F172A; font-size: 1.5rem; font-weight: 700; }
        .kpi-subtitle { font-size: 0.75rem; color: #94A3B8; margin-top: 4px; font-weight: 400; }

        /* TABLA DE CANDIDATOS (HOME) */
        .table-header { display: flex; padding: 12px 16px; border-bottom: 1px solid #F1F5F9; background-color: #FAFAF9; border-top-left-radius: 12px; border-top-right-radius: 12px; margin-top: 20px; }
        .col-header { font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
        .candidate-row-clean { display: flex; align-items: center; padding: 16px; background-color: #FFFFFF; border-bottom: 1px solid #F1F5F9; transition: background 0.2s; }
        .candidate-row-clean:last-child { border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; border-bottom: none; }
        .candidate-row-clean:hover { background-color: #F8FAFC; }
        .cand-name { font-weight: 600; color: #0F172A; font-size: 0.95rem; }
        .cand-party { color: #64748B; font-size: 0.9rem; }
        .btn-link { color: #2563EB; font-weight: 600; font-size: 0.85rem; text-decoration: none; cursor: pointer; }

        /* GRID CANDIDATOS */
        .cand-grid-card {
            background-color: #FFFFFF; padding: 24px; border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #F1F5F9;
            margin-bottom: 20px; text-align: center; height: 100%; transition: transform 0.2s;
        }
        .cand-grid-card:hover { transform: translateY(-3px); border-color: #3B82F6; }
        .cand-grid-btn { display: block; width: 100%; padding: 10px; margin-top: 15px; background-color: #EFF6FF; color: #2563EB; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
        .cand-grid-btn:hover { background-color: #DBEAFE; }

        /* PROPUESTAS */
        .prop-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #F1F5F9; box-shadow: 0 2px 4px rgba(0,0,0,0.02); height: 100%; }
        .prop-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-bottom: 10px; background-color: #F1F5F9; color: #475569; }

        /* RADIOGRAFÍA CARDS */
        .radio-card { background-color: #FFFFFF; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; }
        .radio-title { font-size: 1rem; font-weight: 600; color: #0F172A; margin-bottom: 10px; }
        
        /* EXTRAS */
        .video-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; margin-bottom: 20px; }
        .video-title { padding: 12px 16px; font-weight: 600; font-size: 0.95rem; color: #0F172A; border-bottom: 1px solid #F1F5F9; }
        .bottom-card { background: #FAFAFA; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .bottom-title { font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 5px; }
        .bottom-desc { font-size: 0.85rem; color: #64748B; }

        /* SIDEBAR */
        .sidebar-header { padding: 20px 10px 30px 10px; display: flex; align-items: center; }
        .sidebar-logo { width: 40px; height: 40px; background: #0F172A; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; font-weight: bold; margin-right: 12px; }
        .sidebar-main-title { font-weight: 700; color: #0F172A; font-size: 15px; }
        .sidebar-subtitle { font-size: 12px; color: #64748B; }

    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. GESTIÓN DE DATOS ---
@st.cache_data(ttl=3600)
def load_data():
    # --- A. DATOS BANCO MUNDIAL (API EN VIVO) ---
    try:
        indicators = {
            'NY.GDP.MKTP.KD.ZG': 'PIB', 
            'SL.UEM.TOTL.ZS': 'Desempleo', 
            'SI.POV.NAHC': 'Pobreza',
            'SI.POV.GINI': 'Gini'
        }
        wb_data = wb.download(indicator=list(indicators.keys()), country=['PE'], start=2000, end=datetime.datetime.now().year)
        wb_data = wb_data.reset_index().rename(columns=indicators).sort_values('year')
        status = "✅ Online"
    except:
        wb_data = pd.DataFrame()
        status = "⚠️ Offline (WB)"

    # --- B. DATOS ARCHIVOS CSV (CARPETA data/) ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data')
    
    # Inicializamos todos los dataframes vacíos
    df_anemia = pd.DataFrame()
    df_medicos = pd.DataFrame()
    df_inseguridad = pd.DataFrame()
    df_victimizacion = pd.DataFrame()
    df_servicios_basicos = pd.DataFrame() # Nuevo
    df_internet_quintiles = pd.DataFrame() # Nuevo
    df_bosques = pd.DataFrame() # Nuevo
    df_co2 = pd.DataFrame() # Nuevo
    df_gobernanza = pd.DataFrame() # Nuevo

    try:
        # 1. ANEMIA
        file_anemia = os.path.join(data_path, "anemia.csv")
        if os.path.exists(file_anemia):
            try: df_anemia = pd.read_csv(file_anemia)
            except: df_anemia = pd.read_csv(file_anemia, encoding='latin-1')
            if 'Anemia' in df_anemia.columns and 'Evaluados' in df_anemia.columns:
                 df_anemia = df_anemia.groupby('Año')[['Anemia', 'Evaluados']].sum().reset_index()
                 df_anemia['Porcentaje'] = (df_anemia['Anemia'] / df_anemia['Evaluados']) * 100

        # 2. MÉDICOS
        file_medicos = os.path.join(data_path, "medicos.csv")
        if os.path.exists(file_medicos):
            df_medicos_raw = None
            try: df_medicos_raw = pd.read_csv(file_medicos, header=4)
            except: pass
            if df_medicos_raw is None:
                try: df_medicos_raw = pd.read_csv(file_medicos, header=4, encoding='latin-1')
                except: pass
            
            if df_medicos_raw is not None and 'Departamento' in df_medicos_raw.columns:
                df_medicos = df_medicos_raw[df_medicos_raw['Departamento'].str.contains('Total', case=False, na=False)]
                if not df_medicos.empty:
                    df_medicos = df_medicos.melt(id_vars=['Departamento'], var_name='Año', value_name='Habitantes')
                    df_medicos['Año'] = pd.to_numeric(df_medicos['Año'], errors='coerce')
                    df_medicos['Habitantes'] = pd.to_numeric(df_medicos['Habitantes'], errors='coerce')
                    df_medicos = df_medicos.dropna(subset=['Año', 'Habitantes']).sort_values('Año')
        
        # 3. INSEGURIDAD
        file_inseguridad = os.path.join(data_path, "inseguridad.csv")
        if os.path.exists(file_inseguridad):
            try: df_inseguridad = pd.read_csv(file_inseguridad, header=1)
            except: df_inseguridad = pd.read_csv(file_inseguridad, header=1, encoding='latin-1')
        
        # 4. VICTIMIZACIÓN
        file_victimizacion = os.path.join(data_path, "victimizacion.csv")
        if os.path.exists(file_victimizacion):
            try: df_victimizacion = pd.read_csv(file_victimizacion, header=1)
            except: df_victimizacion = pd.read_csv(file_victimizacion, header=1, encoding='latin-1')

        # --- NUEVOS ARCHIVOS (SECCIONES 6, 7, 8) CON CARGA ROBUSTA ---
        # El truco: Leer header=1 para saltar el título, y forzar nombres de columnas
        
        # 5. SERVICIOS BÁSICOS
        file_servicios = os.path.join(data_path, "seccion6.1.csv")
        if os.path.exists(file_servicios):
            try: 
                df_servicios_basicos = pd.read_csv(file_servicios, header=1) # Saltar título
                if len(df_servicios_basicos.columns) >= 2:
                    df_servicios_basicos = df_servicios_basicos.iloc[:, :2] # Solo 2 columnas
                    df_servicios_basicos.columns = ['Servicio', 'Porcentaje'] # Renombrar a lo seguro
            except: pass

        # 6. INTERNET QUINTILES
        file_internet = os.path.join(data_path, "seccion6.2.csv")
        if os.path.exists(file_internet):
            try: 
                df_internet_quintiles = pd.read_csv(file_internet, header=1)
                if len(df_internet_quintiles.columns) >= 2:
                    df_internet_quintiles = df_internet_quintiles.iloc[:, :2]
                    df_internet_quintiles.columns = ['Quintil', 'Porcentaje']
            except: pass

        # 7. BOSQUES
        file_bosques = os.path.join(data_path, "seccion7.1.csv")
        if os.path.exists(file_bosques):
            try: 
                df_bosques = pd.read_csv(file_bosques, header=1)
                if len(df_bosques.columns) >= 2:
                    df_bosques = df_bosques.iloc[:, :2]
                    df_bosques.columns = ['Año', 'Hectareas']
            except: pass

        # 8. CO2
        file_co2 = os.path.join(data_path, "seccion7.2.csv")
        if os.path.exists(file_co2):
            try: 
                df_co2 = pd.read_csv(file_co2, header=1)
                if len(df_co2.columns) >= 2:
                    df_co2 = df_co2.iloc[:, :2]
                    df_co2.columns = ['Año', 'Megatoneladas']
            except: pass

        # 9. GOBERNANZA
        file_gob = os.path.join(data_path, "seccion8.1.csv")
        if os.path.exists(file_gob):
            try: 
                df_gobernanza = pd.read_csv(file_gob, header=1)
                if len(df_gobernanza.columns) >= 2:
                    df_gobernanza = df_gobernanza.iloc[:, :2]
                    df_gobernanza.columns = ['Indicador', 'Puntaje']
            except: pass
        
    except Exception as e:
        print(f"Error cargando CSVs: {e}")

    # --- C. DATOS MANUALES (Educación) ---
    df_edu_analfa = pd.DataFrame({
        'year': [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        'Tasa': [6.2, 6.0, 5.9, 5.9, 5.8, 5.6, 5.5, 5.5, 5.2, 5.1]
    })
    df_edu_deficit = pd.DataFrame({
        'Año': [2016, 2018, 2020, 2022],
        'Servicios': [1200, 1150, 1100, 1050]
    })

    # --- D. CANDIDATOS ---
    try:
        df_cand = obtener_data_candidatos()
    except Exception:
        df_cand = pd.DataFrame({'Nombre': [], 'Partido': [], 'Foto': []})

    # 2. PROPUESTAS 
    df_prop = pd.DataFrame({
        'Candidato': ['Keiko Fujimori', 'Rafael López Aliaga', 'César Acuña', 'Hernando de Soto', 'Susel Paredes'],
        'Eje': ['Economía', 'Seguridad', 'Educación', 'Economía', 'Derechos Civiles'],
        'Subtema': ['Plan Rescate 2026', 'Plan Bukele', 'Plata como Cancha para Educar', 'Capitalismo Popular', 'Unión Civil'],
        'Texto': [
            'Propuesta de shock de inversiones y desbloqueo minero inmediato.',
            'Creación de cárceles de máxima seguridad en zonas aisladas.',
            'Inversión del 6% del PBI en infraestructura educativa universitaria.',
            'Titulación masiva de propiedades informales para acceso a crédito.',
            'Reconocimiento legal de uniones de hecho para parejas del mismo sexo.'
        ],
        'Tipo': ['Decreto', 'Infraestructura', 'Ley', 'Programa', 'Ley']
    })

    return df_cand, df_prop, wb_data, df_anemia, df_medicos, df_inseguridad, df_victimizacion, df_edu_analfa, df_edu_deficit, df_servicios_basicos, df_internet_quintiles, df_bosques, df_co2, df_gobernanza, status

# Desempaquetar todas las variables
df_cand, df_prop, df_wb, df_anemia, df_medicos, df_inseguridad, df_victimizacion, df_edu_analfa, df_edu_deficit, df_servicios, df_internet, df_bosques, df_co2, df_gob, status_msg = load_data()

# --- 3. COMPONENTES VISUALES ---

def kpi_box(label, value, subtitle=None):
    subtitle_html = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_candidate_table_row(img, name, party):
    st.markdown(f"""
    <div class="candidate-row-clean">
        <div style="width: 50px; margin-right: 15px;">
            <img src="{img}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">
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

def render_section_header(title, subtitle):
    st.markdown(f"## {title}")
    st.markdown(f"<p style='color: #64748B; margin-top: -10px; margin-bottom: 25px;'>{subtitle}</p>", unsafe_allow_html=True)

def render_proposal_card(subtema, tipo, texto):
    st.markdown(f"""
    <div class="prop-card">
        <div class="prop-badge">{tipo}</div>
        <h4 style="margin:0; font-size:1.1rem; color:#0F172A;">{subtema}</h4>
        <p style="color:#334155; margin-top:10px; font-size:0.95rem; line-height:1.5;">{texto}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. VISTAS ---

def view_inicio():
    st.markdown("# Monitor Electoral Perú 2026")
    st.markdown("<div style='color:#64748B; margin-top:-10px; margin-bottom:20px;'>Tu plataforma para un voto informado.</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
    Bienvenido a Monitor Electoral Perú 2026. Nuestra misión es centralizar y simplificar el acceso a la información electoral, 
    promoviendo la transparencia y la participación ciudadana informada para las próximas elecciones.
    </div>
    """, unsafe_allow_html=True)

    # KPIS
    today = datetime.date.today()
    election_date = datetime.date(2026, 4, 12)
    days_left = (election_date - today).days
    
    c1, c2, c3 = st.columns(3)
    with c1: kpi_box("Enlaces Oficiales", "JNE, ONPE")
    with c2: kpi_box("Partidos en Carrera", f"{len(df_cand)}")
    with c3: kpi_box("Días para la elección", f"{days_left}", "12 de Abril, 2026") 
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Candidatos Presidenciales (Vista Previa)")
    st.markdown("""
    <div class="table-header">
        <div style="width: 50px; margin-right: 15px;"></div>
        <div class="col-header" style="width: 30%;">Candidato</div>
        <div class="col-header" style="width: 50%;">Partido Político</div>
        <div class="col-header" style="width: 20%; text-align: right;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="background: white; border: 1px solid #E2E8F0; border-top: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">', unsafe_allow_html=True)
    for _, row in df_cand.head(5).iterrows():
        render_candidate_table_row(row['Foto'], row['Nombre'], row['Partido'])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Biblioteca de Videos")
    col_vid1, col_vid2 = st.columns(2)
    with col_vid1:
        st.markdown('<div class="video-card">', unsafe_allow_html=True)
        st.markdown('<div class="video-title">🗳️ Cédula de votación y cómo votar</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=cJ5UuJJRfNQ")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_vid2:
        st.markdown('<div class="video-card">', unsafe_allow_html=True)
        st.markdown('<div class="video-title">🚫 #EleccionesSinFake | 6 recomendaciones</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=n44WJaYtZrs")
        st.markdown('</div>', unsafe_allow_html=True)

    c_bottom1, c_bottom2 = st.columns(2)
    with c_bottom1: render_bottom_card("Análisis de Propuestas Electorales", "Expertos debaten los planes de gobierno.")
    with c_bottom2: render_bottom_card("¿Cómo funciona el Voto Electrónico?", "Una guía paso a paso para el elector.")


def view_candidatos():
    render_section_header("Candidatos", "Directorio completo de aspirantes a la presidencia.")
    cols = st.columns(3)
    for idx, row in df_cand.iterrows():
        with cols[idx % 3]: 
            st.markdown(f"""
            <div class="cand-grid-card">
                <img src="{row['Foto']}" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 15px; object-fit: cover;">
                <h4 style="margin:0; font-size:1.1rem; color: #0F172A; font-weight: 700;">{row['Nombre']}</h4>
                <p style="color: #64748B; font-size:0.9rem; margin-bottom: 15px;">{row['Partido']}</p>
                <div style="font-size:0.8rem; color:#2563EB; margin-bottom:10px;">{row.get('Estado', '')}</div>
                <a href="#" class="cand-grid-btn">Ver Plan de Gobierno</a>
            </div>
            """, unsafe_allow_html=True)

def view_planes():
    render_section_header("Planes de Gobierno", "Comparador inteligente de propuestas electorales.")
    
    with st.container():
        st.markdown('<div style="background:white; padding:20px; border-radius:12px; border:1px solid #E2E8F0; margin-bottom:20px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: cand_a = st.selectbox("Candidato A", df_prop['Candidato'].unique(), index=0)
        with c2: cand_b = st.selectbox("Candidato B", df_prop['Candidato'].unique(), index=1)
        with c3: eje = st.selectbox("Eje Temático", df_prop['Eje'].unique())
        st.markdown('</div>', unsafe_allow_html=True)
        
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"### {cand_a}")
        prop_a = df_prop[(df_prop['Candidato'] == cand_a) & (df_prop['Eje'] == eje)]
        if not prop_a.empty:
            row = prop_a.iloc[0]
            render_proposal_card(row['Subtema'], row['Tipo'], row['Texto'])
        else:
            st.warning("Sin propuestas en este eje.")

    with col_b:
        st.markdown(f"### {cand_b}")
        prop_b = df_prop[(df_prop['Candidato'] == cand_b) & (df_prop['Eje'] == eje)]
        if not prop_b.empty:
            row = prop_b.iloc[0]
            render_proposal_card(row['Subtema'], row['Tipo'], row['Texto'])
        else:
            st.warning("Sin propuestas en este eje.")


def view_indicadores():
    st.markdown("<h1>Radiografía del Perú</h1>", unsafe_allow_html=True)
    st.markdown("<p class='intro-text'>Datos oficiales clave para comprender el estado actual del país.</p>", unsafe_allow_html=True)
    
    tabs = st.tabs([
        "1. Economía", "2. Pobreza y Social", "3. Educación", 
        "4. Salud", "5. Seguridad", "6. Infraestructura", 
        "7. Ambiente", "8. Gobernanza"
    ])
    
    # 1. ECONOMÍA
    with tabs[0]: 
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Crecimiento del PBI (% anual)</div>', unsafe_allow_html=True)
            if not df_wb.empty:
                fig = px.line(df_wb, x='year', y='PIB', template='plotly_white')
                fig.update_traces(line_color='#2563EB', line_width=3)
                fig.add_hline(y=0, line_dash="dash", line_color="gray")
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Desempleo Total (% fuerza laboral)</div>', unsafe_allow_html=True)
            if not df_wb.empty:
                fig2 = px.bar(df_wb.tail(10), x='year', y='Desempleo', template='plotly_white')
                fig2.update_traces(marker_color='#3B82F6')
                st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Fuente: Banco Mundial (API)")

    # 2. POBREZA
    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Pobreza Monetaria Nacional (%)</div>', unsafe_allow_html=True)
            if not df_wb.empty and 'Pobreza' in df_wb.columns:
                df_pov = df_wb.dropna(subset=['Pobreza'])
                if not df_pov.empty:
                    fig3 = px.area(df_pov, x='year', y='Pobreza', template='plotly_white')
                    fig3.update_traces(line_color='#EF4444', fillcolor="rgba(239, 68, 68, 0.1)")
                    st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Índice de Gini (Desigualdad)</div>', unsafe_allow_html=True)
            if not df_wb.empty and 'Gini' in df_wb.columns:
                df_gini = df_wb.dropna(subset=['Gini'])
                if not df_gini.empty:
                    fig4 = px.line(df_gini, x='year', y='Gini', template='plotly_white', markers=True)
                    fig4.update_traces(line_color='#8B5CF6')
                    st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # 3. EDUCACIÓN
    with tabs[2]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Tasa de Analfabetismo (15+ años)</div>', unsafe_allow_html=True)
            if not df_edu_analfa.empty:
                fig_edu = px.line(df_edu_analfa, x='year', y='Tasa', template='plotly_white', markers=True)
                fig_edu.update_traces(line_color='#F59E0B')
                st.plotly_chart(fig_edu, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Déficit Servicios Secundaria Rural</div>', unsafe_allow_html=True)
            if not df_edu_deficit.empty:
                fig_def = px.bar(df_edu_deficit, x='Año', y='Servicios', template='plotly_white')
                fig_def.update_traces(marker_color='#F59E0B')
                st.plotly_chart(fig_def, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Fuente: ESCALE - MINEDU")

    # 4. SALUD
    with tabs[3]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Anemia Infantil (6 a 35 meses)</div>', unsafe_allow_html=True)
            if not df_anemia.empty:
                fig_anemia = px.line(df_anemia, x='Año', y='Porcentaje', template='plotly_white', markers=True)
                fig_anemia.update_traces(line_color='#DC2626', line_width=3)
                st.plotly_chart(fig_anemia, use_container_width=True)
            else: st.info("Sube 'anemia.csv' a data/")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Habitantes por Médico (Nacional)</div>', unsafe_allow_html=True)
            if not df_medicos.empty:
                fig_med = px.line(df_medicos, x='Año', y='Habitantes', template='plotly_white', markers=True)
                fig_med.update_traces(line_color='#059669', line_width=3)
                st.plotly_chart(fig_med, use_container_width=True)
            else: st.info("Sube 'medicos.csv' a data/")
            st.markdown('</div>', unsafe_allow_html=True)

    # 5. SEGURIDAD
    with tabs[4]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Percepción de Inseguridad (2024)</div>', unsafe_allow_html=True)
            if not df_inseguridad.empty and 'DEPARTAMENTO' in df_inseguridad.columns:
                df_ins_top = df_inseguridad.sort_values('VALOR', ascending=False).head(7)
                fig_ins = px.bar(df_ins_top, x='VALOR', y='DEPARTAMENTO', orientation='h', template='plotly_white')
                fig_ins.update_traces(marker_color='#374151')
                fig_ins.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_ins, use_container_width=True)
            else: st.info("Verificando 'inseguridad.csv' en data/...")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Victimización Nacional (Histórico)</div>', unsafe_allow_html=True)
            if not df_victimizacion.empty:
                fig_vic = px.line(df_victimizacion, x='AÑO', y='VALOR', template='plotly_white', markers=True)
                fig_vic.update_traces(line_color='#9F1239')
                st.plotly_chart(fig_vic, use_container_width=True)
            else: st.info("Verificando 'victimizacion.csv' en data/...")
            st.markdown('</div>', unsafe_allow_html=True)

    # 6. INFRAESTRUCTURA
    with tabs[5]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Servicios Básicos (Vivienda)</div>', unsafe_allow_html=True)
            if not df_servicios.empty:
                fig_serv = px.bar(df_servicios, x='Porcentaje', y='Servicio', orientation='h', template='plotly_white')
                fig_serv.update_traces(marker_color='#0EA5E9')
                st.plotly_chart(fig_serv, use_container_width=True)
            else: st.info("Sube 'seccion6.1.csv' a data/")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Internet por Quintil</div>', unsafe_allow_html=True)
            if not df_internet.empty:
                fig_net = px.bar(df_internet, x='Quintil', y='Porcentaje', template='plotly_white')
                fig_net.update_traces(marker_color='#6366F1')
                st.plotly_chart(fig_net, use_container_width=True)
            else: st.info("Sube 'seccion6.2.csv' a data/")
            st.markdown('</div>', unsafe_allow_html=True)

    # 7. AMBIENTE
    with tabs[6]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Pérdida de Bosques (Ha)</div>', unsafe_allow_html=True)
            if not df_bosques.empty:
                fig_bosq = px.bar(df_bosques, x='Año', y='Hectareas', template='plotly_white')
                fig_bosq.update_traces(marker_color='#166534')
                st.plotly_chart(fig_bosq, use_container_width=True)
            else: st.info("Sube 'seccion7.1.csv' a data/")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Emisiones CO2 (Mt)</div>', unsafe_allow_html=True)
            if not df_co2.empty:
                fig_co2 = px.line(df_co2, x='Año', y='Megatoneladas', template='plotly_white', markers=True)
                fig_co2.update_traces(line_color='#64748B')
                st.plotly_chart(fig_co2, use_container_width=True)
            else: st.info("Sube 'seccion7.2.csv' a data/")
            st.markdown('</div>', unsafe_allow_html=True)

    # 8. GOBERNANZA
    with tabs[7]:
        st.markdown('<div class="radio-card"><div class="radio-title">Indicadores de Gobernanza (0-100)</div>', unsafe_allow_html=True)
        if not df_gob.empty:
            fig_gob = px.bar(df_gob, x='Puntaje', y='Indicador', orientation='h', range_x=[0,100], template='plotly_white')
            fig_gob.update_traces(marker_color='#7C3AED')
            fig_gob.update_layout(height=300)
            st.plotly_chart(fig_gob, use_container_width=True)
        else: st.info("Sube 'seccion8.1.csv' a data/")
        st.markdown('</div>', unsafe_allow_html=True)

def view_participacion():
    st.title("Participación")
    st.text_area("Deja tu comentario")

def view_fuente():
    st.json({"Fuente": "Banco Mundial + JNE + INEI + CEPAL + GFW"})

# --- 5. NAVEGACIÓN ---
st.sidebar.markdown("""<div class="sidebar-header"><div class="sidebar-logo">ME</div><div><div class="sidebar-main-title">Monitor Electoral</div><div class="sidebar-subtitle">Perú 2026</div></div></div>""", unsafe_allow_html=True)

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

if selected == "Inicio": view_inicio()
elif selected == "Candidatos": view_candidatos()
elif selected == "Planes de Gobierno": view_planes()
elif selected == "Indicadores Nacionales": view_indicadores()
elif selected == "Participación Ciudadana": view_participacion()
elif selected == "Fuente de Datos": view_fuente()
