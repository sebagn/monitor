import streamlit as st
import pandas as pd
from telefonos import merge_excels

# Title of the app
st.title('Merge excels')

st.write('''Subir el excel de telefonos tal como esta. 
Subir la tabla dinamica de deudores, guardandola como csv SIN HEADERS, incluyendo las primeras 4 columnas.
''')

# File uploader for Excel file
excel_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

# File uploader for CSV file
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

if excel_file is not None:
    df_excel = pd.read_excel(excel_file)
    st.write("Excel file data uploaded")

if csv_file is not None:
    df_csv = pd.read_csv(csv_file, sep=';')
    st.write("CSV file data uploaded")

    st.markdown("---")

if st.button('Merge excels'):
    if excel_file is not None and csv_file is not None:
        df_merged = merge_excels(df_excel, df_csv)
        st.write("Merged data:")
        st.dataframe(df_merged)

        st.markdown("---")

        # Button to download merged data
        st.download_button(
            label="Download Merged Data as CSV",
            data=df_merged.to_csv(index=False).encode('utf-8'),
            file_name='merged_data.csv',
            mime='text/csv',
        )


    else:
        st.write("Please upload both Excel and CSV files to merge.")

