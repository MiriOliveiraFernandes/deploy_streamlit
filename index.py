import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Análise de Vendas")

upload_file = st.file_uploader("Escolha um arquivo CSV", type='csv')

if upload_file is not None:
    df = pd.read_csv(upload_file, sep=';', decimal=',', thousands='.')
    df.columns = df.columns.str.strip()

    st.write("### Dados carregados:")
    st.dataframe(df.head())

    for col in ['Sales', 'Profit', 'Gross Sales', 'Discounts', 'COGS']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'[^\d,.-]', '', regex=True)
            df[col] = pd.to_numeric(df[col].str.replace('.', '').str.replace(',', '.'), errors='coerce')

    df = df.dropna(subset=['Sales', 'Profit'])

    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    st.write(f"Total geral de vendas: **{total_sales:,.2f}**")
    st.write(f"Lucro total: **{total_profit:,.2f}**")

    vendas_segment_country = df.groupby(['Segment', 'Country'])['Sales'].sum().reset_index()
    st.write("### Vendas totais por Segmento e País:")
    st.dataframe(vendas_segment_country)

    if 'Month Number' not in df.columns:
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        df['Month Number'] = df['Month Name'].map(month_map)

    vendas_por_mes = df.groupby(['Month Number', 'Month Name'])['Sales'].sum().reset_index()
    vendas_por_mes = vendas_por_mes.sort_values('Month Number')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(vendas_por_mes['Month Name'], vendas_por_mes['Sales'], 
            marker='o', color='green', linestyle='-')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Total de Vendas')
    ax.set_title('Vendas por Mês')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(vendas_por_mes['Month Name'], vendas_por_mes['Sales'], color='skyblue')
    ax2.set_xlabel('Mês')
    ax2.set_ylabel('Total de Vendas')
    ax2.set_title('Vendas Mensais (Gráfico de Barras)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)

else:
    st.info("☝️ Faça o upload de um arquivo CSV para visualizar os dados.")