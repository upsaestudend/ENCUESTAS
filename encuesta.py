import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- Refrescar cada 10 segundos automáticamente ---
st_autorefresh(interval=10000, key="refresh")

# --- Título y subtítulo ---
st.title("Resultados de la encuesta (actualización automática cada 10s)")
st.subheader("¿Si las elecciones de segunda vuelta fueran mañana, por quien votarías?")

# --- URL del CSV ---
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1PL0i07Sl2mYrX3z3fxYwvjGw1za3ICLk09nlpqDDzgl-PffuC0NuT1_4xro8ADCQSrAUBlqdhHal/pub?output=csv"

# --- Botón actualizar ---
if st.button("🔄 Actualizar resultados"):
    df = pd.read_csv(url)
else:
    df = pd.read_csv(url)

# --- Columna de respuestas ---
col_respuesta = df.columns[1]

# --- Conteo y porcentajes ---
conteo = df[col_respuesta].value_counts().reset_index()
conteo.columns = ["Respuesta", "Cantidad"]
conteo["Porcentaje"] = ((conteo["Cantidad"] / conteo["Cantidad"].sum()) * 100).round(1)

# --- Mostrar ganador ---
ganador = conteo.iloc[0]["Respuesta"]
st.markdown(f"**Gana el candidato {ganador}**")

# --- Mostrar barras de progreso por candidato ---
st.subheader("📊 Distribución de votos")

for idx, row in conteo.iterrows():
    nombre = row["Respuesta"]
    porcentaje = row["Porcentaje"]
    
    # Definir gradiente por candidato
    if nombre.lower() == "tuto":
        color = "linear-gradient(to right, #E74C3C 0%, #3498DB 100%)"  # rojo a azul
    elif nombre.lower() == "rodrigo":
        color = "linear-gradient(to right, #E74C3C 0%, #ffffff 50%, #2ECC71 100%)"  # rojo blanco verde
    else:
        color = "#95A5A6"  # gris para otros

    # Barra de progreso HTML
    st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <strong>{nombre} ({porcentaje}%)</strong>
            <div style="background-color: #e0e0e0; border-radius: 5px; width: 100%; height: 25px;">
                <div style="width: {porcentaje}%; height: 25px; background: {color}; border-radius: 5px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Última actualización ---
st.caption(f"Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
