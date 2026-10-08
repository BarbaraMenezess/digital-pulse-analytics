import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Configuração da Página & Estilo Clássico (Off-White)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Digital Pulse Analytics",
    page_icon="📈",
    layout="wide"
)

# Estilização CSS personalizada com fundo Off-White sofisticado
st.markdown("""
    <style>
    /* Fundo geral da aplicação em Off-White */
    .stApp {
        background-color: #FDFBF7;
    }
    /* Estilo refinado para a barra lateral */
    [data-testid="stSidebar"] {
        background-color: #F4F1EA;
    }
    /* Cartões de KPI limpos e destacados */
    .stMetric {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.04);
    }
    h1 {
        color: #0F172A;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    h2, h3 {
        color: #1E293B;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Processamento da Base de Dados
# ---------------------------------------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    datas = pd.date_range(start='2023-01-01', periods=24, freq='MS')
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA']
    
    data = []
    for estado in estados:
        base_pib = np.random.uniform(-1.8, 2.8, len(datas))
        base_influencers = np.random.uniform(60, 320, len(datas)) + np.linspace(10, 60, len(datas))
        
        for dt, pib, inf in zip(datas, base_pib, base_influencers):
            data.append({
                'Data': dt,
                'Ano': dt.year,
                'Mês': dt.strftime('%b'),
                'Estado': estado,
                'Variacao_PIB_%': round(pib, 2),
                'Faturamento_Influencers_Mi': round(inf, 2)
            })
            
    df = pd.DataFrame(data)
    df['Status_PIB'] = np.where(df['Variacao_PIB_%'] >= 0, '🟢 Melhora', '🔴 Piora')
    df['Resiliente'] = np.where((df['Variacao_PIB_%'] < 0) & (df['Faturamento_Influencers_Mi'] > 160), 'Sim', 'Não')
    
    return df

df = load_data()

# ---------------------------------------------------------
# 3. Cabeçalho Principal
# ---------------------------------------------------------
st.title("Digital Pulse Analytics")
st.markdown("##### *O Impacto da Economia dos Influenciadores na Resiliência do PIB Regional*")
st.markdown("---")

# ---------------------------------------------------------
# 4. Barra Lateral de Filtros (Filtros Executivos)
# ---------------------------------------------------------
st.sidebar.markdown("### 🔍 Filtros de Análise")

anos_disponiveis = sorted(df['Ano'].unique().tolist())
ano_selecionado = st.sidebar.multiselect("Ano:", anos_disponiveis, default=anos_disponiveis)

estados_disponiveis = sorted(df['Estado'].unique().tolist())
estado_selecionado = st.sidebar.multiselect("Estado / Região:", estados_disponiveis, default=estados_disponiveis)

df_filtrado = df[(df['Ano'].isin(ano_selecionado)) & (df['Estado'].isin(estado_selecionado))]

# ---------------------------------------------------------
# 5. Painel de KPIs (Cartões de Visão Geral)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

pib_medio = df_filtrado['Variacao_PIB_%'].mean() if not df_filtrado.empty else 0
fat_total = df_filtrado['Faturamento_Influencers_Mi'].sum() if not df_filtrado.empty else 0
casos_resiliencia = (df_filtrado['Resiliente'] == 'Sim').sum() if not df_filtrado.empty else 0
status_dominante = "🟢 Melhora" if pib_medio >= 0 else "🔴 Piora"

col1.metric("Variação Média do PIB", f"{pib_medio:.2f}%", delta=status_dominante)
col2.metric("Faturamento Digital Total", f"R$ {fat_total:,.2f} Mi")
col3.metric("Meses de Resiliência Digital", f"{casos_resiliencia} Mês(es)")
col4.metric("Tendência Econômica Geral", status_dominante)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. Gráficos Principais (Fundo Transparente para casar com o Off-White)
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📈 Tendência Temporal", "🎯 Mapeamento de Quadrantes"])

with tab1:
    st.markdown("### Evolução Temporal: PIB vs. Mercado de Influenciadores")
    
    df_temp = df_filtrado.groupby('Data').agg({
        'Variacao_PIB_%': 'mean',
        'Faturamento_Influencers_Mi': 'sum'
    }).reset_index()

    fig_linha = go.Figure()

    fig_linha.add_trace(go.Scatter(
        x=df_temp['Data'], y=df_temp['Variacao_PIB_%'],
        name="Variação PIB (%)",
        line=dict(color='#1E3A8A', width=3)
    ))

    fig_linha.add_trace(go.Scatter(
        x=df_temp['Data'], y=df_temp['Faturamento_Influencers_Mi'],
        name="Faturamento Influencers (R$ Mi)",
        yaxis="y2",
        line=dict(color='#0284C7', width=2, dash='dot')
    ))

    fig_linha.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Período"),
        yaxis=dict(
            title=dict(text="Variação PIB (%)", font=dict(color="#1E3A8A"))
        ),
        yaxis2=dict(
            title=dict(text="Faturamento Influencers (R$ Mi)", font=dict(color="#0284C7")),
            overlaying="y",
            side="right"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_linha, use_container_width=True)

with tab2:
    st.markdown("### Relação entre Faturamento Digital e Desempenho do PIB")
    
    fig_disp = px.scatter(
        df_filtrado,
        x="Faturamento_Influencers_Mi",
        y="Variacao_PIB_%",
        color="Status_PIB",
        symbol="Estado",
        hover_data=["Mês", "Ano"],
        color_discrete_map={"🟢 Melhora": "#059669", "🔴 Piora": "#DC2626"}
    )

    fig_disp.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Faturamento Digital (R$ Milhões)",
        yaxis_title="Variação do PIB (%)"
    )

    st.plotly_chart(fig_disp, use_container_width=True)

# ---------------------------------------------------------
# 7. Tabela de Suporte
# ---------------------------------------------------------
with st.expander("📋 Exibir Tabela de Dados Detalhada"):
    st.dataframe(df_filtrado.sort_values('Data', ascending=False), use_container_width=True)