import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv('vehicles.csv')

st.header('Anúncios de veículos')

#caixa com todos os anúncios
st.subheader('Visualizador de anúncios')
st.dataframe(car_data, width='stretch')

#filtros com caixa de seleção
st.subheader('Filtros')

col1, col2 = st.columns(2)

with col1:
    câmbio = st.selectbox('Câmbio', ['Todos'] + sorted(car_data['transmission'].dropna().unique().tolist()))
    tipo = st.selectbox('Tipo de veículo',['Todos'] + sorted(car_data['type'].dropna().unique().tolist()))

with col2:
    ano = st.selectbox('Ano do Modelo', ['Todos'] + sorted(car_data['model_year'].dropna().unique().tolist(),reverse=True))
    condição = st.selectbox('Condição',['Todas']+sorted(car_data['condition'].dropna().unique().tolist()))

dados_filtrados = car_data.copy()

if câmbio != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['transmission'] == câmbio]

if tipo != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['type'] == tipo]

if ano != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['model_year'] == ano]

if condição != 'Todas':
    dados_filtrados = dados_filtrados[dados_filtrados['condition'] == condição]

#gráfico 1
st.subheader('Condição do Veículo por Ano do Modelo')

fig1 = px.histogram(dados_filtrados, x='model_year', color='condition', labels={'model_year': 'Ano do modelo', 'count': 'Quantidade de anúncios', 'condition': 'Condição'})

fig1.update_layout(xaxis_title='Ano do modelo',yaxis_title='Quantidade de anúncios',legend_title_text='Condição')

st.plotly_chart(fig1, width='stretch', key='condicao_ano')

#gráfico 2
st.subheader('Preço por Quilometragem')

dados_dispersao = dados_filtrados.dropna(subset=['odometer', 'price', 'transmission'])

fig2 = px.scatter(dados_dispersao, x='odometer', y='price', color='transmission', labels={'odometer': 'Quilometragem (milhas)', 'price': 'Preço (US$)', 'transmission': 'Câmbio'}, opacity=0.6)

fig2.update_layout(xaxis_title='Quilometragem (milhas)', yaxis_title='Preço (US$)', legend_title_text='Câmbio')

st.plotly_chart(fig2, width='stretch', key='preco_quilometragem')

#gráfico 3
st.subheader('Comparação de Preços entre Dois Modelos')
st.write('Selecione dois modelos diferentes para comparar.')

# Selecionar os dois modelos
modelos_disponiveis = sorted(dados_filtrados['model'].dropna().unique().tolist())

col1, col2 = st.columns(2)

with col1:
    modelo1 = st.selectbox('Escolha o primeiro modelo', modelos_disponiveis,key='modelo1',index=0)

with col2:
    modelo2 = st.selectbox('Escolha o segundo modelo', modelos_disponiveis, key='modelo2',index=1)

# Opção para normalizar o histograma
normalizar = st.checkbox('Normalizar histograma')

dados_modelos = dados_filtrados[dados_filtrados['model'].isin([modelo1, modelo2])]

if len(modelos_disponiveis) >= 2:
    fig2 = px.histogram(dados_modelos, x='price', color='model', histnorm='percent' if normalizar else None, barmode='overlay', opacity=0.6, labels={'price': 'Preço (US$)', 'model': 'Modelo', 'percent': 'Percentual de anúncios'})
    fig2.update_layout(xaxis_title='Preço (US$)', yaxis_title=('Percentual de anúncios'
            if normalizar
            else 'Quantidade de anúncios'), legend_title_text='Modelo')
    
    st.plotly_chart(fig2, width='stretch', key='comparacao_precos_modelos')