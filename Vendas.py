import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards



# Função para carregar dados
@st.cache_data
def carregar_dados():

    df = pd.read_excel('Vendas.xlsx')

    return df


# Função para rodar a aplicação

def main():

    # Configuração de Página
    st.set_page_config(layout = 'wide', page_title='Relatório Geral', page_icon='📊')

    # Carregando os dados
    df = carregar_dados()

    # Adicionando uma imagem
    st.image('dinheiro.jpg')

    # Aplicando um título na aplicação
    st.title('Dashboard de Vendas 📊')

    # Adicionando uma barra lateral
    st.sidebar.image('dinheiro.jpg')
    ano_filtrado = st.sidebar.selectbox('Filtrar por Ano: ',['Todos', *df['Ano'].unique()])

    # Aplicando o filtro para os casos em que o ano seja diferente do valor 'Todos'
    if ano_filtrado != 'Todos':
        df_filtrado = df[df['Ano'] == ano_filtrado]
    else:
        df_filtrado = df.copy()

    # Adicionando as colunas para os cartões
    col1, col2, col3 = st.columns(3)

    total_custo = df_filtrado["Custo"].sum()
    total_custo = f"R$ {total_custo:,.2f}"

    total_lucro = df_filtrado["Lucro"].sum()
    total_lucro = f"R$ {total_lucro:,.2f}"

    total_clientes = df_filtrado['ID Cliente'].nunique()


    with col1:
        st.metric('Total Custo', total_custo)

    with col2:
        st.metric('Total Lucro', total_lucro)

    with col3:
        st.metric('Total Clientes', total_clientes)


    # Adicionando gráfico de barras horizontais
    col1, col2 = st.columns(2)

    with col1:

        produtos_vendidos_marca = df_filtrado.groupby('Marca').sum()['Quantidade'].sort_values(ascending=True).reset_index()

        figura_marca_quantidade = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', orientation = 'h',
                                         title = 'Total de produtos vendidos por marca',
                                         color_discrete_sequence = ['#3e4095'],
                                         height = 400, width = 380, text='Quantidade')

        figura_marca_quantidade.update_layout(title_x=0.5)

        st.plotly_chart(figura_marca_quantidade, use_container_width=True)


    # Adicionando gráfico de rosca
    with col2:

        lucro_categoria = df_filtrado.groupby('Categoria').sum()['Lucro'].reset_index()

        figura_lucro_categoria = px.pie(lucro_categoria, values = 'Lucro', names = 'Categoria', hole = 0.6,
                                        title = 'Lucro por Categoria',
                                        color_discrete_sequence = ['#3e4095', "#EC610C"],
                                        height = 400, width = 380)

        figura_lucro_categoria.update_layout(title_x = 0.5)

        st.plotly_chart(figura_lucro_categoria, use_container_width=True)


    lucro_mes_ano_categoria = df_filtrado.groupby(['mes_ano', 'Categoria']).sum()['Lucro'].reset_index()

    figura_lucro_mes_ano_categoria = px.line(lucro_mes_ano_categoria, x='mes_ano', y='Lucro',
                                             title='Lucro x Mês por Ano x Lucro',
                                             color = 'Categoria', markers = True, width = 1200)
    st.plotly_chart(figura_lucro_mes_ano_categoria)

    st.markdown(
        """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 18px;
            color: rgba(0,0,0,0,)
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    style_metric_cards(border_left_color='#3e4095')






if __name__ == '__main__':
    main()

