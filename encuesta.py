import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# --- Refrescar cada 10 segundos ---
st_autorefresh(interval=10000, key="refresh")

# --- Título ---
st.title("📊 Resultados del Formulario (actualización automática cada 10s)")

# --- URL del CSV del Google Form ---
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1PL0i07Sl2mYrX3z3fxYwvjGw1za3ICLk09nlpqDDzgl-PffuC0NuT1_4xro8ADCQSrAUBlqdhHal/pub?output=csv"

# --- Cargar datos ---
try:
    df = pd.read_csv(url)
except Exception as e:
    st.error(f"No se pudo cargar el CSV: {e}")
    st.stop()

# --- Vista previa de los datos ---
with st.expander("👀 Ver datos originales"):
    st.dataframe(df)

# --- Columna de respuestas (ajustar según el formulario) ---
col_respuesta = df.columns[1]

# --- Conteo y porcentajes ---
conteo = df[col_respuesta].value_counts().reset_index()
conteo.columns = ["Respuesta", "Cantidad"]
conteo["Porcentaje"] = (conteo["Cantidad"] / conteo["Cantidad"].sum()) * 100

# --- Tabla de resultados ---
st.subheader("📌 Resultados por respuesta")
st.dataframe(conteo)

# --- Gráfico de barras ---
st.subheader("📊 Gráfico de barras")
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(conteo["Respuesta"], conteo["Cantidad"], color="skyblue", edgecolor="black")
ax.set_ylabel("Cantidad de votos")
ax.set_xlabel("Respuestas")
ax.set_title("Resultados del Formulario")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Última actualización ---
st.caption(f"Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
