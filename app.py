import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import wb
import datetime
import numpy as np
import os
from streamlit_option_menu import option_menu
from candidatos_data import obtener_data_candidatos

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
    
    # Inicializamos vacíos
    df_anemia = pd.DataFrame()
    df_medicos = pd.DataFrame()
    df_inseguridad = pd.DataFrame()
    df_victimizacion = pd.DataFrame()

    try:
        # 1. ANEMIA
        file_anemia = os.path.join(data_path, "anemia.csv")
        if os.path.exists(file_anemia):
            # Intentar diferentes encodings
            try:
                df_anemia = pd.read_csv(file_anemia)
            except:
                df_anemia = pd.read_csv(file_anemia, encoding='latin-1')
            
            if 'Anemia' in df_anemia.columns and 'Evaluados' in df_anemia.columns:
                 df_anemia = df_anemia.groupby('Año')[['Anemia', 'Evaluados']].sum().reset_index()
                 df_anemia['Porcentaje'] = (df_anemia['Anemia'] / df_anemia['Evaluados']) * 100

        # 2. MÉDICOS (Lógica Blindada)
        file_medicos = os.path.join(data_path, "medicos.csv")
        if os.path.exists(file_medicos):
            df_medicos_raw = None
            # Estrategia 1: Carga estándar UTF-8, header 4
            try:
                df_medicos_raw = pd.read_csv(file_medicos, header=4)
            except:
                pass
            
            # Estrategia 2: Encoding Latin-1 si falló lo anterior
            if df_medicos_raw is None:
                try:
                    df_medicos_raw = pd.read_csv(file_medicos, header=4, encoding='latin-1')
                except:
                    pass
            
            # Estrategia 3: Separador de punto y coma (común en latam)
            if df_medicos_raw is None or 'Departamento' not in df_medicos_raw.columns:
                try:
                    df_medicos_raw = pd.read_csv(file_medicos, header=4, sep=';', encoding='latin-1')
                except:
                    pass

            # Procesamiento si cargó
            if df_medicos_raw is not None and 'Departamento' in df_medicos_raw.columns:
                # Buscamos la fila Total
                df_medicos = df_medicos_raw[df_medicos_raw['Departamento'].str.contains('Total', case=False, na=False)]
                if not df_medicos.empty:
                    df_medicos = df_medicos.melt(id_vars=['Departamento'], var_name='Año', value_name='Habitantes')
                    df_medicos['Año'] = pd.to_numeric(df_medicos['Año'], errors='coerce')
                    df_medicos['Habitantes'] = pd.to_numeric(df_medicos['Habitantes'], errors='coerce')
                    df_medicos = df_medicos.dropna(subset=['Año', 'Habitantes'])
                    df_medicos = df_medicos.sort_values('Año')
                else:
                    print("Aviso: No se encontró la fila 'Total' en medicos.csv")
        
        # 3. INSEGURIDAD
        file_inseguridad = os.path.join(data_path, "inseguridad.csv")
        if os.path.exists(file_inseguridad):
            try:
                df_inseguridad = pd.read_csv(file_inseguridad, header=1)
            except:
                df_inseguridad = pd.read_csv(file_inseguridad, header=1, encoding='latin-1')
        
        # 4. VICTIMIZACIÓN
        file_victimizacion = os.path.join(data_path, "victimizacion.csv")
        if os.path.exists(file_victimizacion):
            try:
                df_victimizacion = pd.read_csv(file_victimizacion, header=1)
            except:
                df_victimizacion = pd.read_csv(file_victimizacion, header=1, encoding='latin-1')
        
    except Exception as e:
        print(f"Error global cargando CSVs: {e}")

    # --- C. DATOS MANUALES (Educación) ---
    df_edu_analfa = pd.DataFrame({
        'year': [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        'Tasa': [6.2, 6.0, 5.9, 5.9, 5.8, 5.6, 5.5, 5.5, 5.2, 5.1]
    })
    
    df_edu_deficit = pd.DataFrame({
        'Año': [2016, 2018, 2020, 2022],
        'Servicios': [1200, 1150, 1100, 1050]
    })

    # --- D. CANDIDATOS Y PROPUESTAS ---
    # 1. CARGA DE CANDIDATOS REALES DESDE EL ARCHIVO EXTERNO
    try:
        df_cand = obtener_data_candidatos()
    except Exception as e:
        st.error(f"Error cargando candidatos: {e}")
        # Fallback por si falla el archivo
        df_cand = pd.DataFrame({'Nombre': [], 'Partido': [], 'Foto': []})

    # 2. PROPUESTAS (Ajustamos para que coincidan algunos nombres reales si quieres, o déjalo dummy por ahora)
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

    return df_cand, df_prop, wb_data, df_anemia, df_medicos, df_inseguridad, df_victimizacion, df_edu_analfa, df_edu_deficit, status

df_cand, df_prop, df_wb, df_anemia, df_medicos, df_inseguridad, df_victimizacion, df_edu_analfa, df_edu_deficit, status_msg = load_data()

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
    with c2: kpi_box("Partidos en Carrera", "15")
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
    for _, row in df_cand.head(3).iterrows():
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
                <img src="{row['Foto']}" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 15px;">
                <h4 style="margin:0; font-size:1.1rem; color: #0F172A; font-weight: 700;">{row['Nombre']}</h4>
                <p style="color: #64748B; font-size:0.9rem; margin-bottom: 15px;">{row['Partido']}</p>
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
    # --- VISTA CENTRAL DE INDICADORES (CONECTADA A TODOS LOS DATOS) ---
    st.markdown("<h1>Radiografía del Perú</h1>", unsafe_allow_html=True)
    st.markdown("<p class='intro-text'>Datos oficiales clave para comprender el estado actual del país.</p>", unsafe_allow_html=True)
    
    tabs = st.tabs([
        "1. Economía", "2. Pobreza y Social", "3. Educación", 
        "4. Salud", "5. Seguridad", "6. Infraestructura", 
        "7. Ambiente", "8. Gobernanza"
    ])
    
    # SECCIÓN 1: ECONOMÍA (WB)
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

    # SECCIÓN 2: POBREZA (WB)
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
                else: st.warning("Datos de pobreza no disponibles en el rango reciente.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Índice de Gini (Desigualdad)</div>', unsafe_allow_html=True)
            if not df_wb.empty and 'Gini' in df_wb.columns:
                df_gini = df_wb.dropna(subset=['Gini'])
                if not df_gini.empty:
                    fig4 = px.line(df_gini, x='year', y='Gini', template='plotly_white', markers=True)
                    fig4.update_traces(line_color='#8B5CF6')
                    st.plotly_chart(fig4, use_container_width=True)
                else: st.warning("Datos de Gini no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

    # SECCIÓN 3: EDUCACIÓN (Manual / Links)
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

    # SECCIÓN 4: SALUD (CSVs Locales data/)
    with tabs[3]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Anemia Infantil (6 a 35 meses)</div>', unsafe_allow_html=True)
            if not df_anemia.empty:
                fig_anemia = px.line(df_anemia, x='Año', y='Porcentaje', template='plotly_white', markers=True)
                fig_anemia.update_traces(line_color='#DC2626', line_width=3)
                st.plotly_chart(fig_anemia, use_container_width=True)
            else: st.info("Verificando 'anemia.csv' en data/...")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Habitantes por Médico (Nacional)</div>', unsafe_allow_html=True)
            if not df_medicos.empty:
                fig_med = px.line(df_medicos, x='Año', y='Habitantes', template='plotly_white', markers=True)
                fig_med.update_traces(line_color='#059669', line_width=3)
                st.plotly_chart(fig_med, use_container_width=True)
            else: st.info("Verificando 'medicos.csv' en data/...")
            st.markdown('</div>', unsafe_allow_html=True)

    # SECCIÓN 5: SEGURIDAD (CSVs Locales data/)
    with tabs[4]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Percepción de Inseguridad (2024)</div>', unsafe_allow_html=True)
            if not df_inseguridad.empty and 'DEPARTAMENTO' in df_inseguridad.columns:
                # Top 7 regiones + Nacional
                df_ins_top = df_inseguridad.sort_values('VALOR', ascending=False).head(7)
                fig_ins = px.bar(df_ins_top, x='VALOR', y='DEPARTAMENTO', orientation='h', template='plotly_white')
                fig_ins.update_traces(marker_color='#374151')
                fig_ins.update_layout(yaxis=dict(autorange="reversed")) # Para que el mayor salga arriba
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

    # SECCIONES 6, 7, 8 (Dummy Placeholder)
    with tabs[5]: st.info("Datos de Infraestructura en recopilación.")
    with tabs[6]: st.info("Datos de Ambiente en recopilación.")
    with tabs[7]: st.info("Datos de Gobernanza en recopilación.")


def view_participacion():
    st.title("Participación")
    st.text_area("Deja tu comentario")

def view_fuente():
    st.json({"Fuente": "Banco Mundial + JNE + INEI"})

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
elif selected == "Candidatos": view_candidatos()
elif selected == "Planes de Gobierno": view_planes() 
elif selected == "Indicadores Nacionales": view_indicadores() 
elif selected == "Participación Ciudadana": view_participacion()
elif selected == "Fuente de Datos": view_fuente()
