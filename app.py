import streamlit as st
import pandas as pd
import os
import subprocess
import shutil
from zipfile import ZipFile

st.set_page_config(page_title="Generador de certificados", layout="centered")

st.title("📜 Generador de certificados")
st.write("Carga un archivo Excel con una columna con los nombres ('Nombre') para generar los certificados personalizados.")

uploaded_file = st.file_uploader("Cargar archivo de Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if 'Nombre' not in df.columns:
        st.error("La columna con los nombres se debe llamar 'Nombre'")
    else:
        st.success(f"Se cargaron {len(df)} nombres.")
        st.dataframe(df)

        if st.button("Generar certificados"):
            # Prepare output directory
            output_dir = "output"
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir, exist_ok=True)

            # Read LaTeX template
            with open("plantilla_certificado.tex", "r", encoding="utf-8") as f:
                template = f.read()

            # Generate PDFs
            for nombre in df["Nombre"]:
                tex_code = template.replace("<<NOMBRE>>", str(nombre))
                tex_file = os.path.join(output_dir, f"{nombre}.tex")
                with open(tex_file, "w", encoding="utf-8") as tf:
                    tf.write(tex_code)
                subprocess.run(["pdflatex", "-output-directory", output_dir, tex_file], stdout=subprocess.DEVNULL)

            # Zip PDFs
            zip_filename = "certificados.zip"
            with ZipFile(zip_filename, "w") as zipf:
                for file in os.listdir(output_dir):
                    if file.endswith(".pdf"):
                        zipf.write(os.path.join(output_dir, file), arcname=file)

            st.success("¡Certificados generados!")

            with open(zip_filename, "rb") as f:
                st.download_button("⬇️ Descarga los certificados", f, file_name="certificados.zip")


