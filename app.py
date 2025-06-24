# app.py
import streamlit as st
import pandas as pd
import io
import zipfile
import pypdf
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
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{eso-pic}
\usepackage[landscape, margin=2.5cm]{geometry}
\pagestyle{empty}
\setmainfont{tgheros} % Fuente similar a futura
\renewcommand{\familydefault}{\sfdefault}
\definecolor{verdeSMIG}{HTML}{006c65}
\begin{document}
"""
            ending = r"\end{document}"

            body = ""
            for _, row in df.iterrows():
                quien = row.get("Quien", "")
                que = row.get("Que", "")
                tipo = row.get("Tipo", "")
                para = row.get("Para", "")
                nombre = row.get("Nombre", "")
                participacion = row.get("Participacion", "")
                evento = row.get("Evento", "")
                donde = row.get("Donde", "")
                cuando = row.get("Cuando", "")
            
                body += rf"""
            \AddToShipoutPictureBG*{{\includegraphics[width=\paperwidth,height=\paperheight]{{plantilla.pdf}}}}
            
            \begin{{textblock*}}{{22.5cm}}(0cm, 1.5cm)  % ancho del bloque, posición (x, y)
\begin{{minipage}}{{\textwidth}}
\centering

{quien} \\[0.4cm]

{que} \\[0.4cm]

{{\color{{verdeSMIG}} \fontsize{{23}}{{28}}\selectfont \textbf{{{tipo}}}}} \\[0.4cm]

{para} \\[0.4cm]

{{\color{{verdeSMIG}} \fontsize{{23}}{{28}}\selectfont \textbf{{{nombre}}}}} \\[0.4cm]

{participacion} \\[0.4cm]

\textbf{{{evento}}}}} \\[0.4cm]

{donde} \\[0.4cm]
{cuando} \\[0.4cm]

\end{{minipage}}
\end{{textblock*}}

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
        
def split_pdf_by_names(pdf_bytes, names):
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for i, name in enumerate(names):
            writer = pypdf.PdfWriter()
            writer.add_page(reader.pages[i])
            pdf_page = io.BytesIO()
            writer.write(pdf_page)
            pdf_page.seek(0)
            zipf.writestr(f"{name}.pdf", pdf_page.read())

    zip_buffer.seek(0)
    return zip_buffer

st.title("Dividir PDF de certificados")

uploaded_pdf = st.file_uploader("Sube el PDF con todos los certificados", type=["pdf"])
uploaded_xlsx = st.file_uploader("Sube Excel con lista de nombres", type=["xlsx"])

if uploaded_pdf and uploaded_xlsx:
    df = pd.read_excel(uploaded_xlsx)
    names = df['Nombre'].tolist()
    zip_file = split_pdf_by_names(uploaded_pdf.read(), names)
    st.download_button("Descargar certificados separados", zip_file, file_name="certificados_individuales.zip")
