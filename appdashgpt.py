import dash
from dash import html
from components import kpi_card, form_card, tasks_card, dropdown_card, insights_card

app = dash.Dash(__name__, assets_folder='assets')

app.layout = html.Div(
    style={"padding": "2rem"},
    children=[
        html.H1("Dashboard Minimalista Vizu", style={"textAlign": "center"}),

        # KPIs
        html.Div(
            style={"display": "flex", "gap": "1rem", "flexWrap": "wrap"},
            children=[
                kpi_card.kpi_card("Usuários", "124"),
                kpi_card.kpi_card("Taxa de Conversão", "57%"),
                kpi_card.kpi_card("Sessões", "843"),
            ]
        ),

        # Insights
        insights_card.insights_card("As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias.As conversões aumentaram 20% nos últimos 7 dias."),

        # Checklist
        tasks_card.tasks_card(["Revisar dados", "Ajustar layout", "Publicar resultado"]),

        # Dropdown
        dropdown_card.dropdown_card(["Opção A", "Opção B", "Opção C"]),

        # Formulário
        form_card.form_card(),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
