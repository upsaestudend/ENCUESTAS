import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.title("📊 Resultados del Formulario (auto-actualización cada 10s)")

# URL del CSV de Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1PL0i07Sl2mYrX3z3fxYwvjGw1za3ICLk09nlpqDDzgl-PffuC0NuT1_4xro8ADCQSrAUBlqdhHal/pub?output=csv"

# Contenedor para refrescar contenido
placeholder = st.empty()

# Bucle de actualización
while True:
    df = pd.read_csv(url)

    with placeholder.container():
        # Vista previa de datos
        with st.expander("👀 Ver datos originales"):
            st.dataframe(df)

        # Columna de respuestas (ajustar según formulario)
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

        # Última actualización
        st.caption(f"Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Esperar 10 segundos antes de actualizar
    time.sleep(10)
