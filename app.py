# app.py
import streamlit as st
import pandas as pd
import io
import zipfile

st.set_page_config(page_title="Generador de Certificados", layout="centered")

st.title("📜 Generador de certificados")
st.write("Carga un archivo Excel con una columna llamada `Nombre`.")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        if "Nombre" not in df.columns:
            st.error("El archivo debe tener una columna llamada 'Nombre'.")
        else:
            st.success(f"Se encontraron {len(df)} nombres.")

            # Generar contenido LaTeX
            preamble = r"""
\documentclass[12pt]{article}
\usepackage[margin=2.5cm]{geometry}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\pagestyle{empty}
\begin{document}
"""
            ending = r"\end{document}"

            body = ""
            for nombre in df["Nombre"]:
                body += rf"""
\begin{{center}}
    \Huge \textbf{{Certificado de Participación}} \\[1.5cm]
    \Large Se otorga a \\[0.5cm]
    \textbf{{\LARGE {nombre}}} \\[0.5cm]
    Por su destacada participación en el evento. \\[2cm]
    Ciudad de México, junio 2025
\end{{center}}

\newpage
"""

            full_tex = preamble + body + ending

            tex_bytes = full_tex.encode("utf-8")
            st.download_button(
                label="📄 Descargar archivo LaTeX (.tex)",
                data=tex_bytes,
                file_name="certificados.tex",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

