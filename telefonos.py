import pandas as pd
import re 

def merge_excels(df,df2):
    headers = ['deudor','facturas','monto','tipo']
    df2.columns = headers
    df_deudores = df2

    columns_to_keep = ['id_cl', 'nombre','nombre_dos', 'tel_nombre', 'tel_numero', 'tipodetelefono']
    df = df[columns_to_keep]

    df['full_name'] = df['nombre'] + ' ' + df['nombre_dos'].fillna('')
    df.drop(columns=['nombre', 'nombre_dos'], inplace=True)

    df_pref = df[df['tipodetelefono'] == 'PREF. CELU'].groupby('id_cl').first().reset_index()
    df_celu = df[df['tipodetelefono'] == 'CELULAR'].groupby('id_cl').first().reset_index()

    df_combined = pd.merge(df_pref[['id_cl', 'tel_numero','tel_nombre',]], df_celu, on='id_cl', how='right', suffixes=('_pref', '_celu'))
    df_combined['tel_numero_pref'] = df_combined['tel_numero_pref'].fillna(df_combined['tel_numero_celu'])
    df_combined['tel_nombre_pref'] = df_combined['tel_nombre_pref'].fillna(df_combined['tel_nombre_celu'])
    df_combined.drop(columns=['tel_numero_celu', 'tel_nombre_celu', 'tipodetelefono'], inplace=True)

    def format_tel_numero(tel_numero):
        tel_numero = re.sub(r'[()\s-]', '', tel_numero)
        tel_numero = re.sub(r'^\d', '+549', tel_numero)
        tel_numero = re.sub(r'15', '', tel_numero, count=1)
        tel_numero = str(tel_numero)
        return tel_numero

    df_combined['tel_numero_pref'] = df_combined['tel_numero_pref'].apply(format_tel_numero)
    df_combined['id_cl'] = df_combined['id_cl'].astype(str)

    df_deudores['id_cl'] = df_deudores['deudor'].str.extract(r'MO-(\d+)/0')
    df_deudores['id_cl'] = df_deudores['id_cl'].astype(str)
    df_deudores.drop('deudor', axis=1, inplace=True)

    merged_df = pd.merge(df_deudores, df_combined, on='id_cl', how='inner')
    merged_df = merged_df[['id_cl'] + [col for col in merged_df.columns if col != 'id_cl']]

    # merged_df.to_csv('data/merged.csv', index=False)
    return merged_df
