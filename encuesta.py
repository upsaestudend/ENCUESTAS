import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# --- URL del CSV de Google Sheets ---
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1PL0i07Sl2mYrX3z3fxYwvjGw1za3ICLk09nlpqDDzgl-PffuC0NuT1_4xro8ADCQSrAUBlqdhHal/pub?output=csv"

# --- Controlar refresco cada 10s ---
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# Si ya pasaron 10 segundos, recargar
if time.time() - st.session_state.last_refresh > 10:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

# --- Cargar datos ---
df = pd.read_csv(url)

st.title("📊 Resultados del Formulario (auto-actualización cada 10s)")

# Vista previa
with st.expander("👀 Ver datos originales"):
    st.dataframe(df)

# --- Columna de respuestas (ajústala según tu formulario) ---
col_respuesta = df.columns[1]

# Conteo y porcentajes
conteo = df[col_respuesta].value_counts().reset_index()
conteo.columns = ["Respuesta", "Cantidad"]
conteo["Porcentaje"] = (conteo["Cantidad"] / conteo["Cantidad"].sum()) * 100

st.subheader("📌 Resultados por respuesta")
st.dataframe(conteo)

# Gráfico de barras
st.subheader("📊 Gráfico de barras")
fig, ax = plt.subplots()
ax.bar(conteo["Respuesta"], conteo["Cantidad"], color="skyblue", edgecolor="black")
ax.set_ylabel("Cantidad de votos")
ax.set_xlabel("Respuestas")
ax.set_title("Resultados del Formulario")
plt.xticks(rotation=45)
st.pyplot(fig)

st.caption(f"Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
