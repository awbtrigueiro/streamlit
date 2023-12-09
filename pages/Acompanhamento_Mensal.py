import pandas as pd
import streamlit as st


@st.cache_data

def carregar_dados():

    df = pd.read_excel('Vendas.xlsx')

    return df


def color_negative(valor):
    color = 'red' if valor < 0 else 'black'

    return f'color: {color}'


def main():

    # Configuração de Página
    st.set_page_config(page_title='Resultados Mensais', layout='wide', page_icon='📊')

    # Aplicando um título na aplicação
    st.header('Análise dos Registros Mensais 📅')

    # Lendo o dataset
    df = carregar_dados()

    # Adicionando uma barra lateral
    st.sidebar.image('dinheiro.jpg')

    # Modificando o Dataset
    MoM = df.groupby('mes_ano').sum()['Lucro'].reset_index()
    MoM['Ultimo Mês'] = MoM['Lucro'].shift(1)
    MoM['Variação'] = MoM['Lucro'] - MoM['Ultimo Mês']
    MoM['Variação Percentual'] = (MoM['Variação'] / MoM['Ultimo Mês']) * 100
    MoM['Variação Percentual'] = MoM['Variação Percentual'].map('{:.2f}%'.format)
    MoM['Variação Percentual'] = MoM['Variação Percentual'].replace('nan%', '')

    # Aplicando cores nos valores do dataframe
    df_styled = MoM.style.format({
        'Ultimo Mês': 'R$ {:.2f}',
        'Lucro': 'R$ {:.2f}',
        'Variação': 'R$ {:20,.2f}'}).hide(axis='index').applymap(color_negative,
                                                            subset=['Variação'])



    # Escrevendo o dataset na Tela
    st.write(df_styled)



if __name__ == '__main__':
    main()

