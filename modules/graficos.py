from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
PLOTLY_CONFIG = {
    # Remove a marca do Plotly da barra de ferramentas e mantém a interface mais institucional.
    "displaylogo": False,
    # Permite zoom com o scroll do mouse, útil em dashboards com muitos registros.
    "scrollZoom": True,
    # Remove ferramentas menos necessárias para o usuário final, reduzindo ruído visual.
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}


def _tema_plotly(tema_escuro: bool = False) -> str:
    """Retorna o template visual do Plotly conforme o tema selecionado no dashboard."""
    return "plotly_dark" if tema_escuro else "plotly_white"


def grafico_restricoes_por_ug(
    df_resumo_ug: pd.DataFrame,
    tema_escuro: bool = False,
) -> go.Figure | None:
    """
    Gera gráfico interativo de quantidade de restrições por Unidade Gestora.

    Alterações de estilo aplicadas:
    - conversão para Plotly, permitindo hover, zoom e pan no dashboard web;
    - uso de template claro/escuro profissional: plotly_white ou plotly_dark;
    - aplicação da paleta Viridis, adequada para acessibilidade e leitura progressiva;
    - adoção de barras horizontais para melhorar a leitura de nomes longos de UGs;
    - remoção de bordas desnecessárias e manutenção de grade discreta no eixo quantitativo;
    - aumento da fonte, título explicativo, rótulos claros e hover com informações adicionais.
    """
    if df_resumo_ug is None or df_resumo_ug.empty:
        return None

    colunas_obrigatorias = {"ug", "nome_ug", "quantidade", "restricoes"}
    if not colunas_obrigatorias.issubset(df_resumo_ug.columns):
        return None

    df_plot = df_resumo_ug.copy()
    df_plot["ug"] = df_plot["ug"].astype(str).str.zfill(6)
    df_plot["nome_ug"] = df_plot["nome_ug"].fillna("UG não identificada").astype(str)
    df_plot["restricoes"] = df_plot["restricoes"].fillna("Não informado").astype(str)
    df_plot["quantidade"] = pd.to_numeric(df_plot["quantidade"], errors="coerce").fillna(0).astype(int)

    # Ordenação crescente para que as maiores barras fiquem visualmente destacadas ao final.
    df_plot = df_plot.sort_values("quantidade", ascending=True)

    # Rótulo composto para reduzir ambiguidade entre código e denominação da UG.
    df_plot["ug_label"] = df_plot["ug"] + " - " + df_plot["nome_ug"]

    fig = px.bar(
        df_plot,
        x="quantidade",
        y="ug_label",
        orientation="h",
        color="quantidade",
        color_continuous_scale="Viridis",
        text="quantidade",
        custom_data=["ug", "nome_ug", "restricoes"],
        labels={
            "quantidade": "Quantidade de restrições",
            "ug_label": "Unidade Gestora",
            "color": "Quantidade",
        },
        template=_tema_plotly(tema_escuro),
    )

    # Hover enriquecido: acrescenta dados úteis sem poluir o gráfico principal.
    fig.update_traces(
        hovertemplate=(
            "<b>UG:</b> %{customdata[0]}<br>"
            "<b>Nome da UG:</b> %{customdata[1]}<br>"
            "<b>Quantidade:</b> %{x}<br>"
            "<b>Restrições:</b> %{customdata[2]}"
            "<extra></extra>"
        ),
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        title={
            "text": "Quantidade de Restrições Contábeis por Unidade Gestora",
            "x": 0.01,
            "xanchor": "left",
            "font": {"size": 22},
        },
        xaxis_title="Quantidade de restrições",
        yaxis_title="Unidade Gestora",
        font={"size": 14},
        height=max(460, 34 * len(df_plot)),
        margin={"l": 20, "r": 30, "t": 80, "b": 45},
        coloraxis_colorbar={"title": "Quantidade"},
        showlegend=True,
        hoverlabel={"font_size": 13},
    )

    # Limpeza visual: sem bordas; grade apenas onde ajuda a leitura quantitativa.
    fig.update_xaxes(showline=False, showgrid=True, zeroline=False)
    fig.update_yaxes(showline=False, showgrid=False, automargin=True)
    return fig


def grafico_frequencia_restricoes(
    df_resumo_restricao: pd.DataFrame,
    tema_escuro: bool = False,
) -> go.Figure | None:
    """
    Gera gráfico interativo de frequência por código de restrição.

    Alterações de estilo aplicadas:
    - conversão para Plotly com renderização via st.plotly_chart;
    - uso da paleta Cividis, acessível e adequada para escala de intensidade;
    - hover com descrição do código de restrição, quando existente na tabela interna;
    - título e eixos explícitos, fonte ampliada e remoção de bordas desnecessárias.
    """
    if df_resumo_restricao is None or df_resumo_restricao.empty:
        return None

    colunas_obrigatorias = {"restricao", "quantidade"}
    if not colunas_obrigatorias.issubset(df_resumo_restricao.columns):
        return None

    df_plot = df_resumo_restricao.copy()
    df_plot["restricao"] = df_plot["restricao"].astype(str).str.zfill(3)
    df_plot["quantidade"] = pd.to_numeric(df_plot["quantidade"], errors="coerce").fillna(0).astype(int)

    if "descricao" not in df_plot.columns:
        df_plot["descricao"] = "Descrição não informada"
    df_plot["descricao"] = df_plot["descricao"].fillna("Descrição não informada").astype(str)
    df_plot = df_plot.sort_values("quantidade", ascending=False)

    fig = px.bar(
        df_plot,
        x="restricao",
        y="quantidade",
        color="quantidade",
        color_continuous_scale="Cividis",
        text="quantidade",
        custom_data=["descricao"],
        labels={
            "restricao": "Código da restrição",
            "quantidade": "Quantidade de ocorrências",
            "color": "Quantidade",
        },
        template=_tema_plotly(tema_escuro),
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Restrição:</b> %{x}<br>"
            "<b>Quantidade:</b> %{y}<br>"
            "<b>Descrição:</b> %{customdata[0]}"
            "<extra></extra>"
        ),
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        title={
            "text": "Frequência por Código de Restrição Contábil",
            "x": 0.01,
            "xanchor": "left",
            "font": {"size": 22},
        },
        xaxis_title="Código da restrição",
        yaxis_title="Quantidade de ocorrências",
        font={"size": 14},
        height=480,
        margin={"l": 20, "r": 30, "t": 80, "b": 45},
        coloraxis_colorbar={"title": "Quantidade"},
        showlegend=True,
        hoverlabel={"font_size": 13},
    )

    fig.update_xaxes(showline=False, showgrid=False, type="category")
    fig.update_yaxes(showline=False, showgrid=True, zeroline=False)
    return fig


def exibir_grafico_plotly_streamlit(fig: go.Figure | None, mensagem_sem_dados: str) -> None:
    """
    Envolve a figura Plotly em uma estrutura Streamlit para dashboard web.

    A função centraliza o uso de st.plotly_chart, garantindo comportamento visual
    padronizado, largura responsiva, zoom com scroll e barra de ferramentas limpa.
    O import do Streamlit é local para manter as funções geradoras de figuras
    reutilizáveis e testáveis fora do ambiente do dashboard.
    """
    import streamlit as st

    if fig is None:
        st.info(mensagem_sem_dados)
        return

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


def exibir_graficos_resumo_streamlit(
    df_resumo_ug: pd.DataFrame,
    df_resumo_restricao: pd.DataFrame,
    tema_escuro: bool = False,
) -> None:
    """
    Renderiza, no dashboard Streamlit, os gráficos interativos da aba Resumo.

    Esta camada separa a construção dos gráficos da exibição na interface,
    facilitando manutenção, testes e reaproveitamento em outras páginas do app.
    """
    fig_ug = grafico_restricoes_por_ug(df_resumo_ug, tema_escuro=tema_escuro)
    fig_restr = grafico_frequencia_restricoes(df_resumo_restricao, tema_escuro=tema_escuro)

    exibir_grafico_plotly_streamlit(
        fig_ug,
        "Não há dados suficientes para gerar o gráfico de restrições por UG.",
    )
    exibir_grafico_plotly_streamlit(
        fig_restr,
        "Não há dados suficientes para gerar o gráfico de frequência por código de restrição.",
    )
