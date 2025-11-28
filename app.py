import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import wb
import datetime
import numpy as np

# --- 1. CONFIGURACIÓN TÉCNICA ---
st.set_page_config(
    layout="wide", 
    page_title="Monitor Electoral Perú 2026",
    initial_sidebar_state="expanded"
)

# Estilos CSS para apariencia web profesional
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {color: #2c3e50;}
    h2 {color: #34495e;}
</style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE DATOS (HÍBRIDA) ---

@st.cache_data(ttl=3600) # Se actualiza cada hora automáticamente
def load_data():
    """
    Carga datos de dos fuentes:
    1. Dinámica: API del Banco Mundial para indicadores económicos/sociales.
    2. Estática: Archivo Excel local 'data.xlsx' para candidatos/propuestas (o genera dummy si no existe).
    """
    
    # --- A. DATOS DINÁMICOS (BANCO MUNDIAL) ---
    wb_data = pd.DataFrame()
    wb_status = "Iniciando descarga..."
    
    try:
        # Códigos oficiales del Banco Mundial
        indicators = {
            'NY.GDP.MKTP.KD.ZG': 'Crecimiento PIB (%)',     
            'SL.UEM.TOTL.ZS': 'Desempleo Total (%)',        
            'SI.POV.NAHC': 'Pobreza Monetaria Nacional (%)',
            'SI.POV.GINI': 'Índice Gini'                    
        }
        
        # Descarga rango: año 2000 hasta hoy
        end_year = datetime.datetime.now().year
        wb_data = wb.download(indicator=list(indicators.keys()), country=['PE'], start=2000, end=end_year)
        
        # Limpieza
        wb_data = wb_data.reset_index()
        wb_data = wb_data.rename(columns=indicators)
        wb_data['year'] = wb_data['year'].astype(int)
        wb_data = wb_data.sort_values('year')
        
        wb_status = "✅ Datos conectados en vivo con Banco Mundial."
        
    except Exception as e:
        wb_status = f"⚠️ Error conectando con API Banco Mundial: {e}. Usando datos vacíos."
        wb_data = pd.DataFrame(columns=['year', 'Crecimiento PIB (%)', 'Desempleo Total (%)', 'Pobreza Monetaria Nacional (%)', 'Índice Gini'])

    # --- B. DATOS ESTÁTICOS (EXCEL LOCAL O DUMMY) ---
    try:
        # Intenta leer el Excel local 'data.xlsx'
        df_candidatos = pd.read_excel('data.xlsx', sheet_name='candidatos')
        df_propuestas = pd.read_excel('data.xlsx', sheet_name='propuestas')
        # Si tienes indicadores manuales para los otros tabs (salud, seguridad, etc), cárgalos aquí
        # df_manual_indicators = pd.read_excel('data.xlsx', sheet_name='indicadores') 
        
        # Generamos datos dummy para los tabs que NO son del Banco Mundial (para que no falle si el excel está incompleto)
        years = np.arange(2018, 2025)
        df_manual_indicators = pd.DataFrame({
            'year': years,
            'Gasto_Educacion': np.random.uniform(3, 5, len(years)),
            'Conclusion_Secundaria': np.random.uniform(70, 85, len(years)),
            'Cobertura_Salud': np.random.uniform(80, 95, len(years)),
            'Anemia_Infantil': np.random.uniform(30, 45, len(years)),
            'Tasa_Victimizacion': np.random.uniform(25, 40, len(years)),
            'Homicidios': np.random.uniform(6, 10, len(years)),
            'Acceso_Agua': np.random.uniform(85, 95, len(years)),
            'Acceso_Luz': np.random.uniform(90, 98, len(years)),
            'Acceso_Internet': np.random.uniform(60, 80, len(years)),
            'Deforestacion': np.random.uniform(100000, 150000, len(years)),
            'Emisiones_GEI': np.random.uniform(70, 90, len(years)),
            'Indice_Corrupcion': np.random.uniform(30, 40, len(years)),
            'Ejecucion_Gasto': np.random.uniform(60, 85, len(years))
        })

    except FileNotFoundError:
        # FALLBACK: Genera datos dummy si no existe data.xlsx para que la web funcione
        df_candidatos = pd.DataFrame({
            'ID': [1, 2], 
            'Nombre': ['Candidato Ejemplo 1', 'Candidato Ejemplo 2'],
            'Partido': ['Partido A', 'Partido B'],
            'Cargo': ['Presidente', 'Presidente'],
            '# Cédula': ['111', '222'],
            'Web': ['#', '#'],
            'Link Plan Gobierno': ['#', '#'],
            'Región': ['Lima', 'Cusco']
        })
        
        df_propuestas = pd.DataFrame({
            'Candidato': ['Candidato Ejemplo 1', 'Candidato Ejemplo 2'],
            'Eje': ['Economía', 'Seguridad'],
            'Subtema': ['Empleo', 'Extorsión'],
            'Texto Propuesta': ['Propuesta de prueba...', 'Propuesta de prueba 2...'],
            'Tipo Instrumento': ['Ley', 'Plan'],
            'Grupo Objetivo': ['Jóvenes', 'Comerciantes'],
            'Meta Cuantitativa': ['Sí', 'No']
        })
        
        years = np.arange(2018, 2025)
        df_manual_indicators = pd.DataFrame({
            'year': years,
            'Gasto_Educacion': np.random.uniform(3, 5, len(years)),
            'Conclusion_Secundaria': np.random.uniform(70, 85, len(years)),
            'Cobertura_Salud': np.random.uniform(80, 95, len(years)),
            'Anemia_Infantil': np.random.uniform(30, 45, len(years)),
            'Tasa_Victimizacion': np.random.uniform(25, 40, len(years)),
            'Homicidios': np.random.uniform(6, 10, len(years)),
            'Acceso_Agua': np.random.uniform(85, 95, len(years)),
            'Acceso_Luz': np.random.uniform(90, 98, len(years)),
            'Acceso_Internet': np.random.uniform(60, 80, len(years)),
            'Deforestacion': np.random.uniform(100000, 150000, len(years)),
            'Emisiones_GEI': np.random.uniform(70, 90, len(years)),
            'Indice_Corrupcion': np.random.uniform(30, 40, len(years)),
            'Ejecucion_Gasto': np.random.uniform(60, 85, len(years))
        })
        
    return df_candidatos, df_propuestas, wb_data, df_manual_indicators, wb_status

# Cargamos los datos
df_candidatos, df_propuestas, df_wb, df_manual, status_msg = load_data()

# --- 3. FUNCIONES DE RENDERIZADO ---

def render_inicio():
    st.markdown("---")
    st.title("🗳️ Elecciones Generales Perú 2026")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Fecha Elección", "12 Abril 2026", "Convocada")
    col2.markdown("#### Organismos Oficiales")
    col2.markdown("[Jurado Nacional de Elecciones (JNE)](https://www.jne.gob.pe/)")
    col2.markdown("[ONPE](https://www.onpe.gob.pe/)")
    
    st.markdown("### 👤 Candidatos Presidenciales y Organizaciones")
    if not df_candidatos.empty:
        st.dataframe(
            df_candidatos, 
            use_container_width=True,
            column_config={
                "Link Plan Gobierno": st.column_config.LinkColumn("Plan de Gobierno"),
                "Web": st.column_config.LinkColumn("Sitio Web")
            }
        )
    else:
        st.warning("No hay datos de candidatos cargados.")

def render_propuestas():
    st.markdown("---")
    st.header("🔍 Comparador de Propuestas")
    st.info("Utiliza IA para clasificar y resumir los planes de gobierno. Siempre verifica la fuente original.")
    
    c1, c2 = st.columns(2)
    with c1:
        filtro_cand = st.selectbox("Filtrar por Candidato", ["Todos"] + list(df_propuestas['Candidato'].unique()))
    with c2:
        filtro_eje = st.selectbox("Filtrar por Eje Temático", ["Todos"] + list(df_propuestas['Eje'].unique()))
        
    df_show = df_propuestas.copy()
    if filtro_cand != "Todos":
        df_show = df_show[df_show['Candidato'] == filtro_cand]
    if filtro_eje != "Todos":
        df_show = df_show[df_show['Eje'] == filtro_eje]
        
    for index, row in df_show.iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['Eje']}** | *{row['Subtema']}*")
            st.subheader(row['Candidato'])
            st.write(row['Texto Propuesta'])
            st.caption(f"Instrumento: {row['Tipo Instrumento']} | Objetivo: {row['Grupo Objetivo']} | Meta Cuantitativa: {row['Meta Cuantitativa']}")

def render_radiografia():
    st.markdown("---")
    st.header("🇵🇪 Radiografía del Perú: Indicadores Clave")
    st.caption(status_msg)
    
    tabs = st.tabs([
        "1. Economía y Empleo", 
        "2. Pobreza y Desigualdad", 
        "3. Educación", 
        "4. Salud", 
        "5. Seguridad", 
        "6. Infraestructura", 
        "7. Ambiente", 
        "8. Gobernanza y Gasto"
    ])
    
    # --- TAB 1: ECONOMÍA (DINÁMICO - BANCO MUNDIAL) ---
    with tabs[0]:
        st.subheader("Indicadores Macroeconómicos (Fuente: Banco Mundial)")
        
        # Gráfico PIB
        df_pib = df_wb.dropna(subset=['Crecimiento PIB (%)'])
        if not df_pib.empty:
            fig = px.line(df_pib, x='year', y='Crecimiento PIB (%)', title='Crecimiento del PIB (% Anual)', markers=True)
            fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Recesión")
            st.plotly_chart(fig, use_container_width=True)
            
        # Gráfico Desempleo
        df_des = df_wb.dropna(subset=['Desempleo Total (%)'])
        if not df_des.empty:
            fig2 = px.bar(df_des, x='year', y='Desempleo Total (%)', title='Desempleo Total (% Fuerza Laboral)', color_discrete_sequence=['orange'])
            st.plotly_chart(fig2, use_container_width=True)

    # --- TAB 2: POBREZA (DINÁMICO - BANCO MUNDIAL) ---
    with tabs[1]:
        st.subheader("Indicadores Sociales (Fuente: Banco Mundial)")
        
        # Pobreza
        df_pov = df_wb.dropna(subset=['Pobreza Monetaria Nacional (%)'])
        if not df_pov.empty:
            fig3 = px.area(df_pov, x='year', y='Pobreza Monetaria Nacional (%)', title='Pobreza Monetaria (% Población)', color_discrete_sequence=['red'])
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Datos recientes de pobreza no disponibles en la API del Banco Mundial.")
            
        # Gini
        df_gini = df_wb.dropna(subset=['Índice Gini'])
        if not df_gini.empty:
            fig4 = px.line(df_gini, x='year', y='Índice Gini', title='Índice Gini (Desigualdad)', markers=True, color_discrete_sequence=['purple'])
            st.plotly_chart(fig4, use_container_width=True)
            
    # --- TABS 3-8: MANUALES / EXCEL (PLACEHOLDERS POR AHORA) ---
    with tabs[2]:
        st.subheader("Educación")
        fig = px.line(df_manual, x='year', y='Conclusion_Secundaria', title='Tasa Conclusión Secundaria (%)', markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[3]:
        st.subheader("Salud")
        fig = px.bar(df_manual, x='year', y='Anemia_Infantil', title='Anemia Infantil (%)', color_discrete_sequence=['pink'])
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[4]:
        st.subheader("Seguridad Ciudadana")
        fig = px.line(df_manual, x='year', y='Homicidios', title='Tasa Homicidios (x 100k hab)', markers=True, color_discrete_sequence=['darkred'])
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[5]:
        st.subheader("Infraestructura")
        fig = px.line(df_manual, x='year', y=['Acceso_Agua', 'Acceso_Internet'], title='Acceso a Servicios Básicos (%)')
        st.plotly_chart(fig, use_container_width=True)

    with tabs[6]:
        st.subheader("Ambiente y Amazonía")
        fig = px.area(df_manual, x='year', y='Deforestacion', title='Deforestación (Hectáreas)', color_discrete_sequence=['green'])
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[7]:
        st.subheader("Gobernanza y Gasto Público")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df_manual, x='year', y='Ejecucion_Gasto', title='Ejecución Gasto Público (%)', color_discrete_sequence=['navy'])
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.line(df_manual, x='year', y='Indice_Corrupcion', title='Índice Percepción Corrupción', markers=True)
            st.plotly_chart(fig2, use_container_width=True)

def render_recursos():
    st.markdown("---")
    st.header("📺 Recursos Audiovisuales")
    col1, col2 = st.columns(2)
    with col1:
        st.video("https://www.youtube.com/watch?v=cJ5UuJJRfNQ")
        st.caption("Cómo votar correctamente (Referencia ONPE)")
    with col2:
        st.video("https://www.youtube.com/watch?v=n44WJaYtZrs")
        st.caption("Evita las Fake News (Referencia JNE)")

def render_metodologia():
    st.markdown("---")
    st.header("📋 Metodología")
    st.markdown("""
    **Fuentes de Datos:**
    1. **Dinámicos:** Los indicadores económicos y de pobreza se extraen en tiempo real de la API del Banco Mundial (`pandas-datareader`).
    2. **Estáticos:** La información de candidatos y propuestas se basa en los Planes de Gobierno presentados al JNE.
    
    **Neutralidad:**
    Esta plataforma no tiene afiliación política. Los resúmenes son generados tecnológicamente para facilitar la lectura.
    """)

# --- 4. NAVEGACIÓN (SIDEBAR) ---
with st.sidebar:
    st.title("Monitor Electoral 2026")
    st.image("https://cdn-icons-png.flaticon.com/512/3408/3408546.png", width=100)
    
    opcion = st.radio("Navegación", 
             ["Inicio", "Comparador Propuestas", "Radiografía Perú", "Recursos", "Metodología"])
    
    st.markdown("---")
    st.caption("v1.2 - Conexión API World Bank")

# Enrutador
if opcion == "Inicio":
    render_inicio()
elif opcion == "Comparador Propuestas":
    render_propuestas()
elif opcion == "Radiografía Perú":
    render_radiografia()
elif opcion == "Recursos":
    render_recursos()
elif opcion == "Metodología":
    render_metodologia()
