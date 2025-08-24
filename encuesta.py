import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- Configuración de página ---
st.set_page_config(page_title="Resultados de la encuesta", page_icon="🗳️", layout="wide")

# --- Refresco automático cada 10 segundos ---
st_autorefresh(interval=10000, key="refresh")

# --- Título y subtítulo ---
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>Resultados de la encuesta</h1>
    <h3 style='text-align: center; color: #34495E;'>¿Si las elecciones de segunda vuelta fueran mañana, por quien votarías?</h3>
""", unsafe_allow_html=True)

# --- Imagen de los candidatos debajo de la pregunta ---
st.image("candidatos.jpeg", caption="Candidatos", use_container_width=True)

# --- URL del CSV del Google Form ---
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1PL0i07Sl2mYrX3z3fxYwvjGw1za3ICLk09nlpqDDzgl-PffuC0NuT1_4xro8ADCQSrAUBlqdhHal/pub?output=csv"

# --- Botón de actualización manual ---
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🔄 Actualizar resultados"):
    df = pd.read_csv(url)
else:
    df = pd.read_csv(url)
st.markdown("</div>", unsafe_allow_html=True)

# --- Columna de respuestas ---
col_respuesta = df.columns[1]

# --- Conteo y porcentajes ---
conteo = df[col_respuesta].value_counts().reset_index()
conteo.columns = ["Respuesta", "Cantidad"]
conteo["Porcentaje"] = ((conteo["Cantidad"] / conteo["Cantidad"].sum()) * 100).round(1)

# --- Mostrar ganador ---
ganador = conteo.iloc[0]["Respuesta"]
st.markdown(f"<h2 style='text-align: center; color: #E74C3C;'>Gana el candidato {ganador}</h2>", unsafe_allow_html=True)

# --- Barras de progreso por candidato ---
st.subheader("📊 Barras de progreso por candidato")
for idx, row in conteo.iterrows():
    nombre = row["Respuesta"]
    porcentaje = row["Porcentaje"]

    # Colores por candidato
    if nombre.lower() == "tuto":
        color = "linear-gradient(to right, #E74C3C 0%, #3498DB 100%)"  # rojo → azul
    elif nombre.lower() == "rodrigo":
        color = "linear-gradient(to right, #E74C3C 0%, #ffffff 50%, #2ECC71 100%)"  # rojo → blanco → verde
    else:
        color = "#95A5A6"  # gris neutro

    st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <strong>{nombre} ({porcentaje}%)</strong>
            <div style="background-color: #e0e0e0; border-radius: 5px; width: 100%; height: 25px;">
                <div style="width: {porcentaje}%; height: 25px; background: {color}; border-radius: 5px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Última actualización ---
st.markdown(f"<p style='text-align: center; color: gray;'>Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_htm
