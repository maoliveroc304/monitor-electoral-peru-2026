import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import wb
import datetime
import numpy as np
import os
import streamlit.components.v1 as components # Necesario para el chatbot
from streamlit_option_menu import option_menu

# IMPORTAR DATOS EXTERNOS
try:
    from candidatos_data import obtener_data_candidatos
except ImportError:
    def obtener_data_candidatos():
        return pd.DataFrame({'Nombre': [], 'Partido': [], 'Foto': []})

try:
    from propuestas_data import obtener_data_propuestas
except ImportError:
    def obtener_data_propuestas():
        return pd.DataFrame(columns=['Candidato', 'Eje', 'Subtema', 'Texto', 'Tipo'])

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
        
        /* SIDEBAR FIJO Y VISIBLE */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
            min-width: 280px !important;
            width: 280px !important;
        }
        
        [data-testid="collapsedControl"] { display: none; }

        h1 { font-weight: 800; color: #0F172A; font-size: 2rem; margin-bottom: 0.5rem; }
        .intro-text { color: #64748B; font-size: 1rem; line-height: 1.6; margin-bottom: 2rem; }

        .kpi-card {
            background-color: #FFFFFF; padding: 20px; border-radius: 12px;
            border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            height: 100%; display: flex; flex-direction: column; justify-content: center;
        }
        .kpi-label { color: #64748B; font-size: 0.85rem; font-weight: 500; margin-bottom: 8px; }
        .kpi-value { color: #0F172A; font-size: 1.5rem; font-weight: 700; }
        .kpi-subtitle { font-size: 0.75rem; color: #94A3B8; margin-top: 4px; font-weight: 400; }

        .table-header { display: flex; padding: 12px 16px; border-bottom: 1px solid #F1F5F9; background-color: #FAFAF9; border-top-left-radius: 12px; border-top-right-radius: 12px; margin-top: 20px; }
        .col-header { font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
        .candidate-row-clean { display: flex; align-items: center; padding: 16px; background-color: #FFFFFF; border-bottom: 1px solid #F1F5F9; transition: background 0.2s; }
        .candidate-row-clean:last-child { border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; border-bottom: none; }
        .candidate-row-clean:hover { background-color: #F8FAFC; }
        .cand-name { font-weight: 600; color: #0F172A; font-size: 0.95rem; }
        .cand-party { color: #64748B; font-size: 0.9rem; }
        .btn-link { color: #2563EB; font-weight: 600; font-size: 0.85rem; text-decoration: none; cursor: pointer; }

        .cand-grid-card {
            background-color: #FFFFFF; padding: 24px; border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #F1F5F9;
            margin-bottom: 20px; text-align: center; height: 100%; transition: transform 0.2s;
        }
        .cand-grid-card:hover { transform: translateY(-3px); border-color: #3B82F6; }
        
        /* BOTONES VER PLAN */
        div[data-testid="stVerticalBlock"] > div > button {
            width: 100%;
            background-color: #EFF6FF;
            color: #2563EB;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem;
            margin-top: 10px;
            transition: background-color 0.2s;
        }
        div[data-testid="stVerticalBlock"] > div > button:hover {
            background-color: #DBEAFE;
        }

        .prop-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #F1F5F9; box-shadow: 0 2px 4px rgba(0,0,0,0.02); height: 100%; }
        .prop-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-bottom: 10px; background-color: #F1F5F9; color: #475569; }

        .radio-card { background-color: #FFFFFF; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; }
        .radio-title { font-size: 1rem; font-weight: 600; color: #0F172A; margin-bottom: 10px; }
        
        .video-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; margin-bottom: 20px; }
        .video-title { padding: 12px 16px; font-weight: 600; font-size: 0.95rem; color: #0F172A; border-bottom: 1px solid #F1F5F9; }
        .bottom-card { background: #FAFAFA; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .bottom-title { font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 5px; }
        .bottom-desc { font-size: 0.85rem; color: #64748B; }

        .sidebar-header { padding: 20px 10px 30px 10px; display: flex; align-items: center; }
        .sidebar-logo { width: 40px; height: 40px; background: #0F172A; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; font-weight: bold; margin-right: 12px; }
        .sidebar-main-title { font-weight: 700; color: #0F172A; font-size: 15px; }
        .sidebar-subtitle { font-size: 12px; color: #64748B; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. GESTIÓN DE DATOS ---

def smart_read_csv(filepath, expected_columns=None, keyword_search=None):
    if not os.path.exists(filepath):
        return pd.DataFrame()

    df = pd.DataFrame()
    
    try:
        df = pd.read_csv(filepath, header=None, engine='python')
    except:
        try:
            df = pd.read_csv(filepath, header=None, encoding='latin-1', engine='python')
        except:
            return pd.DataFrame()

    if expected_columns:
        if df.shape[1] >= len(expected_columns):
            df = df.iloc[:, :len(expected_columns)]
            df.columns = expected_columns
            value_col = expected_columns[-1]
            df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
            df = df.dropna(subset=[value_col])
            return df
    
    if keyword_search:
        try:
            for i, row in df.head(20).iterrows():
                if row.astype(str).str.contains(keyword_search, case=False).any():
                    try: return pd.read_csv(filepath, header=i)
                    except: return pd.read_csv(filepath, header=i, encoding='latin-1')
        except:
            pass

    return df

@st.cache_data(ttl=3600)
def load_data():
    # A. BANCO MUNDIAL
    try:
        indicators = {'NY.GDP.MKTP.KD.ZG': 'PIB', 'SL.UEM.TOTL.ZS': 'Desempleo', 
                      'SI.POV.NAHC': 'Pobreza', 'SI.POV.GINI': 'Gini'}
        wb_data = wb.download(indicator=list(indicators.keys()), country=['PE'], start=2000, end=datetime.datetime.now().year)
        wb_data = wb_data.reset_index().rename(columns=indicators).sort_values('year')
        status = "✅ Online"
    except:
        wb_data = pd.DataFrame()
        status = "⚠️ Offline"

    # B. CSV LOCALES
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data')
    
    # Inicialización
    df_anemia = pd.DataFrame()
    df_medicos = pd.DataFrame()
    df_inseguridad = pd.DataFrame()
    df_victimizacion = pd.DataFrame()
    df_servicios = pd.DataFrame() 
    df_internet = pd.DataFrame()  
    df_bosques = pd.DataFrame() 
    df_co2 = pd.DataFrame() 
    df_gob = pd.DataFrame()      
    df_deuda = pd.DataFrame()

    try:
        # 1. ANEMIA
        file_anemia = os.path.join(data_path, "anemia.csv")
        df_anemia = smart_read_csv(file_anemia, keyword_search="Año")
        if not df_anemia.empty and 'Anemia' in df_anemia.columns:
             df_anemia = df_anemia.groupby('Año')[['Anemia', 'Evaluados']].sum().reset_index()
             df_anemia['Porcentaje'] = (df_anemia['Anemia'] / df_anemia['Evaluados']) * 100

        # 2. MÉDICOS
        file_medicos = os.path.join(data_path, "medicos.csv")
        if os.path.exists(file_medicos):
            # Lectura manual robusta para header saltado
            try: 
                # Intentar varios headers típicos
                temp = pd.read_csv(file_medicos, header=4) # El formato usual de tus excel
                if 'Departamento' not in temp.columns:
                     temp = pd.read_csv(file_medicos, header=0) # Si está limpio

                if 'Departamento' in temp.columns:
                    temp = temp[temp['Departamento'].str.contains('Total', case=False, na=False)]
                    if not temp.empty:
                        df_medicos = temp.melt(id_vars=['Departamento'], var_name='Año', value_name='Habitantes')
                        df_medicos['Año'] = pd.to_numeric(df_medicos['Año'], errors='coerce')
                        if df_medicos['Habitantes'].dtype == object:
                            df_medicos['Habitantes'] = df_medicos['Habitantes'].astype(str).str.replace(' ', '', regex=False)
                        df_medicos['Habitantes'] = pd.to_numeric(df_medicos['Habitantes'], errors='coerce')
                        df_medicos = df_medicos.dropna(subset=['Año', 'Habitantes']).sort_values('Año')
            except: pass

        # 3. INSEGURIDAD
        df_inseguridad = smart_read_csv(os.path.join(data_path, "inseguridad.csv"), keyword_search="DEPARTAMENTO")
        
        # 4. VICTIMIZACIÓN
        df_victimizacion = smart_read_csv(os.path.join(data_path, "victimizacion.csv"), keyword_search="AÑO")

        # 5. SERVICIOS (Fix para archivo con 3 columnas: Servicio, Area, Value)
        file_serv = os.path.join(data_path, "servicios_basicos.csv")
        if os.path.exists(file_serv):
            try:
                temp = pd.read_csv(file_serv, header=0)
                # Renombrar si es necesario para estandarizar
                if len(temp.columns) >= 3:
                    df_servicios = temp.iloc[:, [0, 2]] # Tomar col 0 y 2 (Servicio y Valor)
                    df_servicios.columns = ['Servicio', 'Porcentaje']
                    df_servicios['Porcentaje'] = pd.to_numeric(df_servicios['Porcentaje'], errors='coerce')
            except: pass
        
        # 6. INTERNET QUINTILES
        file_internet = os.path.join(data_path, "internet_quintiles.csv")
        if os.path.exists(file_internet):
            try:
                df_temp = pd.read_csv(file_internet, header=0)
                df_temp.columns = df_temp.columns.str.strip()
                if 'Quintil' in df_temp.columns:
                    # Excluir columna Quintil para el melt
                    val_vars = [c for c in df_temp.columns if c != 'Quintil']
                    df_internet = df_temp.melt(id_vars=['Quintil'], value_vars=val_vars, var_name='Área', value_name='Porcentaje')
            except: pass
        
        # 7. BOSQUES
        df_bosques = smart_read_csv(os.path.join(data_path, "bosques.csv"), expected_columns=['Año', 'Hectareas'])
        
        # 8. CO2 (Fix para valores con comas "58,403")
        file_co2 = os.path.join(data_path, "emisions_co2.csv")
        if os.path.exists(file_co2):
            try:
                # Probar header 1
                temp = pd.read_csv(file_co2, header=1)
                if len(temp.columns) >= 2:
                    df_co2 = temp.iloc[:, :2]
                    df_co2.columns = ['Año', 'Megatoneladas']
                    # Limpiar comas
                    if df_co2['Megatoneladas'].dtype == object:
                        df_co2['Megatoneladas'] = df_co2['Megatoneladas'].astype(str).str.replace(',', '').astype(float)
            except: pass
        
        # 9. GOBERNANZA (Fix para serie temporal)
        file_gob = os.path.join(data_path, "eficacia_gobierno.csv")
        if os.path.exists(file_gob):
            try:
                temp = pd.read_csv(file_gob, header=1)
                if len(temp.columns) >= 2:
                    df_gob = temp.iloc[:, :2]
                    df_gob.columns = ['Año', 'Puntuación']
            except: pass

        # 10. DEUDA PÚBLICA
        df_deuda = smart_read_csv(os.path.join(data_path, "deuda_publica.csv"), expected_columns=['Año', 'Soles'])
        
    except Exception as e:
        print(f"Error cargando CSVs: {e}")

    # C. MANUALES
    df_edu_analfa = pd.DataFrame({'year': np.arange(2013, 2023), 'Tasa': [6.2, 6.0, 5.9, 5.9, 5.8, 5.6, 5.5, 5.5, 5.2, 5.1]})
    df_edu_deficit = pd.DataFrame({'Año': [2016, 2018, 2020, 2022], 'Servicios': [1200, 1150, 1100, 1050]})

    # D. CANDIDATOS Y PROPUESTAS
    try: df_cand = obtener_data_candidatos()
    except: df_cand = pd.DataFrame({'Nombre': [], 'Partido': [], 'Foto': []})

    try: df_prop = obtener_data_propuestas()
    except: df_prop = pd.DataFrame(columns=['Candidato', 'Eje', 'Subtema', 'Texto', 'Tipo'])

    return df_cand, df_prop, wb_data, df_anemia, df_medicos, df_inseguridad, df_victimizacion, df_edu_analfa, df_edu_deficit, df_servicios, df_internet, df_bosques, df_co2, df_gob, df_deuda, status

df_cand, df_prop, df_wb, df_anemia, df_medicos, df_inseguridad, df_victimizacion, df_edu_analfa, df_edu_deficit, df_servicios, df_internet, df_bosques, df_co2, df_gob, df_deuda, status_msg = load_data()

# --- 3. HELPERS ---

def kpi_box(label, value, subtitle=None):
    sub = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{sub}</div>', unsafe_allow_html=True)

def render_candidate_table_row(img, name, party):
    st.markdown(f"""
    <div class="candidate-row-clean">
        <img src="{img}" style="width:40px; height:40px; border-radius:50%; margin-right:15px; object-fit:cover;">
        <div style="flex-grow:1;">
            <div class="cand-name">{name}</div>
            <div class="cand-party">{party}</div>
        </div>
        <a href="#" class="btn-link">Ver Perfil</a>
    </div>
    """, unsafe_allow_html=True)

def render_bottom_card(title, desc):
    st.markdown(f'<div class="bottom-card"><div class="bottom-title">{title}</div><div class="bottom-desc">{desc}</div></div>', unsafe_allow_html=True)

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

# HELPER: GRÁFICO CON ZOOM INTELIGENTE
def plot_zoom_chart(df, x_col, y_col, color, chart_type='line'):
    if df.empty: return None
    
    # Conversión explícita a numérico para evitar errores de resta
    df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
    df = df.dropna(subset=[x_col])
    
    if df.empty: return None

    max_x = df[x_col].max()
    min_x = max_x - 5
    
    if chart_type == 'line':
        fig = px.line(df, x=x_col, y=y_col, template='plotly_white')
        fig.update_traces(line_color=color, line_width=3)
    else:
        fig = px.bar(df, x=x_col, y=y_col, template='plotly_white')
        fig.update_traces(marker_color=color)
        
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="linear",
            range=[min_x, max_x + 0.5]
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

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

    today = datetime.date.today()
    days_left = (datetime.date(2026, 4, 12) - today).days
    c1, c2, c3 = st.columns(3)
    with c1: kpi_box("Enlaces Oficiales", "JNE, ONPE")
    with c2: kpi_box("Partidos en Carrera", f"{len(df_cand)}")
    with c3: kpi_box("Días para la elección", f"{days_left}", "12 de Abril, 2026")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Candidatos (Vista Previa)")
    st.markdown("""<div class="table-header"><div style="width: 50px; margin-right: 15px;"></div><div class="col-header" style="width: 30%;">Candidato</div><div class="col-header" style="width: 50%;">Partido Político</div></div>""", unsafe_allow_html=True)
    st.markdown('<div style="background: white; border: 1px solid #E2E8F0; border-top: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">', unsafe_allow_html=True)
    for _, row in df_cand.head(3).iterrows():
        render_candidate_table_row(row['Foto'], row['Nombre'], row['Partido'])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Recursos")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown('<div class="video-card"><div class="video-title">🗳️ Cómo votar</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=cJ5UuJJRfNQ")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2: 
        st.markdown('<div class="video-card"><div class="video-title">🚫 Fake News</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=n44WJaYtZrs")
        st.markdown('</div>', unsafe_allow_html=True)

def view_candidatos():
    render_section_header("Candidatos", "Directorio completo de aspirantes a la presidencia.")
    
    def go_to_plan(name):
        st.session_state['page_selection'] = 'Planes de Gobierno'
        st.session_state['selected_candidate'] = name
        st.rerun()

    cols = st.columns(3)
    for idx, row in df_cand.iterrows():
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="cand-grid-card">
                <img src="{row['Foto']}" style="width:80px; height:80px; border-radius:50%; margin-bottom:15px; object-fit:cover;">
                <h4 style="margin:0; color:#0F172A;">{row['Nombre']}</h4>
                <p style="color:#64748B; font-size:0.9rem;">{row['Partido']}</p>
                <div style="font-size:0.8rem; color:#2563EB; margin-bottom:10px;">{row.get('Estado', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Ver Plan de Gobierno", key=f"btn_{idx}"):
                go_to_plan(row['Nombre'])

def view_planes():
    render_section_header("Planes de Gobierno", "Comparador inteligente de propuestas electorales.")
    
    idx_a = 0
    if 'selected_candidate' in st.session_state and st.session_state['selected_candidate'] in df_prop['Candidato'].unique():
        try:
            idx_a = list(df_prop['Candidato'].unique()).index(st.session_state['selected_candidate'])
        except: pass

    with st.container():
        st.markdown('<div style="background:white; padding:20px; border-radius:12px; border:1px solid #E2E8F0; margin-bottom:20px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: cand_a = st.selectbox("Candidato A", df_prop['Candidato'].unique(), index=idx_a)
        with c2: cand_b = st.selectbox("Candidato B", df_prop['Candidato'].unique(), index=1 if len(df_prop['Candidato'].unique()) > 1 else 0)
        with c3: eje = st.selectbox("Eje Temático", df_prop['Eje'].unique())
        st.markdown('</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    def show_p(cand, col):
        with col:
            st.markdown(f"### {cand}")
            props = df_prop[(df_prop['Candidato'] == cand) & (df_prop['Eje'] == eje)]
            if not props.empty:
                for _, row in props.iterrows():
                    render_proposal_card(row['Subtema'], row['Tipo'], row['Texto'])
            else: st.info("Información en proceso.")

    show_p(cand_a, col_a)
    show_p(cand_b, col_b)

def view_indicadores():
    st.markdown("<h1>Radiografía del Perú</h1>", unsafe_allow_html=True)
    st.markdown("<p class='intro-text'>Datos oficiales clave para comprender el estado actual del país.</p>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Economía", "Social", "Educación", "Salud", "Seguridad", "Infraestructura", "Ambiente", "Gobernanza"])
    
    with tabs[0]: # Economía
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Crecimiento del PBI (% anual)</div>', unsafe_allow_html=True)
            if not df_wb.empty: 
                fig = plot_zoom_chart(df_wb, 'year', 'PIB', '#2563EB', 'line')
                if fig:
                    fig.add_hline(y=0, line_dash="dash", line_color="gray")
                    st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Desempleo Total (% fuerza laboral)</div>', unsafe_allow_html=True)
            if not df_wb.empty: 
                st.plotly_chart(plot_zoom_chart(df_wb, 'year', 'Desempleo', '#3B82F6', 'bar'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]: # Social
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Pobreza Monetaria (%)</div>', unsafe_allow_html=True)
            if not df_wb.empty and 'Pobreza' in df_wb.columns: 
                st.plotly_chart(plot_zoom_chart(df_wb.dropna(subset=['Pobreza']), 'year', 'Pobreza', '#EF4444', 'line'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Desigualdad (Gini)</div>', unsafe_allow_html=True)
            if not df_wb.empty and 'Gini' in df_wb.columns: 
                st.plotly_chart(plot_zoom_chart(df_wb.dropna(subset=['Gini']), 'year', 'Gini', '#8B5CF6', 'line'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]: # Educación
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Analfabetismo (15+ años)</div>', unsafe_allow_html=True)
            if not df_edu_analfa.empty: st.plotly_chart(px.line(df_edu_analfa, x='year', y='Tasa', template='plotly_white').update_traces(line_color='#F59E0B'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Déficit Servicios Sec. Rural</div>', unsafe_allow_html=True)
            if not df_edu_deficit.empty: st.plotly_chart(px.bar(df_edu_deficit, x='Año', y='Servicios', template='plotly_white').update_traces(marker_color='#F59E0B'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]: # Salud
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Anemia Infantil (%)</div>', unsafe_allow_html=True)
            if not df_anemia.empty: st.plotly_chart(plot_zoom_chart(df_anemia, 'Año', 'Porcentaje', '#DC2626', 'line'), use_container_width=True)
            else: st.info("Datos de anemia no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Habitantes por Médico</div>', unsafe_allow_html=True)
            if not df_medicos.empty: st.plotly_chart(plot_zoom_chart(df_medicos, 'Año', 'Habitantes', '#059669', 'line'), use_container_width=True)
            else: st.info("Datos de médicos no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]: # Seguridad
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Percepción de Inseguridad (2024)</div>', unsafe_allow_html=True)
            if not df_inseguridad.empty and 'DEPARTAMENTO' in df_inseguridad.columns:
                st.plotly_chart(px.bar(df_inseguridad.sort_values('VALOR', ascending=False).head(7), x='VALOR', y='DEPARTAMENTO', orientation='h', template='plotly_white').update_traces(marker_color='#374151'), use_container_width=True)
            else: st.info("Datos de inseguridad no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Victimización Nacional</div>', unsafe_allow_html=True)
            if not df_victimizacion.empty: 
                st.plotly_chart(plot_zoom_chart(df_victimizacion, 'AÑO', 'VALOR', '#9F1239', 'line'), use_container_width=True)
            else: st.info("Datos de victimización no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]: # Infraestructura
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Servicios Básicos (Vivienda)</div>', unsafe_allow_html=True)
            if not df_servicios.empty: st.plotly_chart(px.bar(df_servicios, x='Porcentaje', y='Servicio', orientation='h', template='plotly_white').update_traces(marker_color='#0EA5E9'), use_container_width=True)
            else: st.info("Datos de servicios no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Internet por Quintil y Área</div>', unsafe_allow_html=True)
            if not df_internet.empty: 
                fig_net = px.bar(df_internet, x='Quintil', y='Porcentaje', color='Área', barmode='group', template='plotly_white')
                st.plotly_chart(fig_net, use_container_width=True)
            else: st.info("Datos de internet no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[6]: # Ambiente
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Pérdida de Bosques</div>', unsafe_allow_html=True)
            if not df_bosques.empty: st.plotly_chart(plot_zoom_chart(df_bosques, 'Año', 'Hectareas', '#166534', 'bar'), use_container_width=True)
            else: st.info("Datos de bosques no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Emisiones de CO2</div>', unsafe_allow_html=True)
            if not df_co2.empty: 
                fig_co2 = plot_zoom_chart(df_co2, 'Año', 'Megatoneladas', '#64748B', 'line')
                if fig_co2: fig_co2.update_yaxes(fixedrange=False)
                st.plotly_chart(fig_co2, use_container_width=True)
            else: st.info("Datos de CO2 no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[7]: # Gobernanza
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="radio-card"><div class="radio-title">Indicadores de Gobernanza (0-100)</div>', unsafe_allow_html=True)
            if not df_gob.empty: 
                st.plotly_chart(plot_zoom_chart(df_gob, 'Año', 'Puntuación', '#7C3AED', 'line'), use_container_width=True)
            else: st.info("Datos de gobernanza no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="radio-card"><div class="radio-title">Deuda Pública</div>', unsafe_allow_html=True)
            if not df_deuda.empty: st.plotly_chart(plot_zoom_chart(df_deuda, 'Año', 'Soles', '#F59E0B', 'line'), use_container_width=True)
            else: st.info("Datos de deuda no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

def view_participacion():
    st.title("Participación Ciudadana")
    st.markdown("""
    <div class="kpi-card" style="text-align: center; padding: 30px;">
        <h3>¿Quieres recibir actualizaciones semanales?</h3>
        <p style="color: #64748B;">Únete a nuestra lista de difusión para estar informado sobre los candidatos y propuestas.</p>
        <a href="https://script.google.com/macros/s/AKfycbwAd1MlRBtT2SnGxG8DRbmxWZcaEKLJz9gMQcwiuGJ2Zr_wmHmBNfeCh9CAKVf0UpQL/exec" target="_blank" style="display: inline-block; background-color: #2563EB; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 10px;">
            Suscribirme a las Alertas 📩
        </a>
    </div>
    """, unsafe_allow_html=True)

def view_fuente():
    st.markdown("## Fuentes de Datos")
    st.markdown("""
    <div class="kpi-card">
        <h4>Datos Económicos y Sociales</h4>
        <ul>
            <li><b>Banco Mundial:</b> <a href="https://datos.bancomundial.org/indicator/NY.GDP.MKTP.KD.ZG?locations=PE">Crecimiento PIB</a>, <a href="https://datos.bancomundial.org/indicador/SL.UEM.TOTL.ZS?locations=PE">Desempleo</a>, <a href="https://datos.bancomundial.org/tema/pobreza?locations=PE">Pobreza</a>, <a href="https://datos.bancomundial.org/indicador/SI.POV.GINI?locations=PE">Gini</a>.</li>
            <li><b>BCRP:</b> <a href="https://estadisticas.bcrp.gob.pe/estadisticas/series/trimestrales/resultados/PN03371FQ/html">Deuda Pública</a>.</li>
        </ul>
        <h4>Datos Sectoriales</h4>
        <ul>
            <li><b>Educación (MINEDU/ESCALE):</b> <a href="https://escale.minedu.gob.pe/">Tasa de analfabetismo y Déficit de servicios</a>.</li>
            <li><b>Infraestructura (CEPAL):</b> <a href="https://statistics.cepal.org/portal/inequalities/housing-and-basic-services.html?lang=es&indicator=260">Servicios Básicos</a>, <a href="https://statistics.cepal.org/portal/inequalities/housing-and-basic-services.html?lang=es&indicator=4623">Acceso a Internet</a>.</li>
            <li><b>Ambiente:</b> <a href="https://www.globalforestwatch.org/dashboards/country/PER/">Pérdida de Bosques (GFW)</a>, <a href="https://datosmacro.expansion.com/energia-y-medio-ambiente/emisiones-co2/peru">Emisiones CO2</a>.</li>
            <li><b>Gobernanza:</b> <a href="https://www.worldbank.org/en/publication/worldwide-governance-indicators/interactive-data-access">Indicadores WGI</a>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 5. NAVEGACIÓN ---
st.sidebar.markdown("""<div class="sidebar-header"><div class="sidebar-logo">ME</div><div><div class="sidebar-main-title">Monitor Electoral</div><div class="sidebar-subtitle">Perú 2026</div></div></div>""", unsafe_allow_html=True)

# Lógica de Navegación
if 'page_selection' not in st.session_state:
    st.session_state['page_selection'] = 'Inicio'

options = ["Inicio", "Candidatos", "Planes de Gobierno", "Indicadores Nacionales", "Participación Ciudadana", "Fuente de Datos"]
try:
    idx = options.index(st.session_state['page_selection'])
except:
    idx = 0

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=["house-door-fill", "people-fill", "file-text-fill", "bar-chart-fill", "chat-text-fill", "database-fill"],
        default_index=idx,
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff"},
            "icon": {"color": "#64748B", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "padding": "10px 15px", "color": "#334155"},
            "nav-link-selected": {"background-color": "#EFF6FF", "color": "#2563EB", "font-weight": "600", "border-left": "3px solid #2563EB"}
        }
    )
    
    if selected != st.session_state['page_selection']:
        st.session_state['page_selection'] = selected
        st.rerun()

    st.markdown("---")
    st.caption("© 2026 Monitor Electoral")

# Router
if st.session_state['page_selection'] == "Inicio": view_inicio()
elif st.session_state['page_selection'] == "Candidatos": view_candidatos()
elif st.session_state['page_selection'] == "Planes de Gobierno": view_planes()
elif st.session_state['page_selection'] == "Indicadores Nacionales": view_indicadores()
elif st.session_state['page_selection'] == "Participación Ciudadana": view_participacion()
elif st.session_state['page_selection'] == "Fuente de Datos": view_fuente()

# Chatbot
chat_icon = "https://raw.githubusercontent.com/maoliveroc304/monitor-electoral-peru-2026/main/data/fotos/voto_informado.jpg"

components.html(f"""
<script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
<df-messenger
  intent="WELCOME"
  chat-title="Asistente Informado 🤖"
  agent-id="0dc0a346-2828-4cb8-a95e-14c5ba301baa"
  language-code="es"
  chat-icon="{chat_icon}"
></df-messenger>
""", height=600)
