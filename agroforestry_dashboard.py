from datetime import datetime, timedelta
from io import BytesIO
import hashlib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pandas import ExcelWriter  


# Config of beginning page
try:
    st.set_page_config(
        page_title="Agrofloratech",
        page_icon="assets/logo-agrofloratech.png",
        layout="wide"
    )
except:
    st.set_page_config(
        page_title="Agrofloratech",
        page_icon="🌳",
        layout="wide"

    )


# Authentication system
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text


# Simulation of a database (I stored here my users)
users_db = {
    "agronomo1": {
        "password": make_hashes("Uniso123"),
        "name": "Leonardo Peres",
        "access": "full"
    },
    "tecnico1": {
        "password": make_hashes("plantio456"),
        "name": "Técnico Oliveira",
        "access": "limited"
    }
}


# Invented and randomized soil data
def generate_soil_data():
    now = datetime.now()
    dates = [now - timedelta(days=i) for i in range(30)]

    data = {
        "Data": dates,
        "pH": np.random.normal(6.2, 0.3, 30),
        "Nitrogênio (ppm)": np.random.normal(25, 5, 30),
        "Fósforo (ppm)": np.random.normal(15, 3, 30),
        "Potássio (ppm)": np.random.normal(120, 20, 30),
        "Cálcio (cmolc/dm³)": np.random.normal(3.5, 0.5, 30),
        "Magnésio (cmolc/dm³)": np.random.normal(1.2, 0.2, 30),
        "Matéria Orgânica (%)": np.random.normal(3.8, 0.4, 30),
        "Umidade (%)": np.random.normal(65, 8, 30),
        "Temperatura (°C)": np.random.normal(22, 2, 30)
    }

    df = pd.DataFrame(data)
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    return df


# Recomendações de árvores baseadas em parâmetros do solo
def get_tree_recommendations(soil_params):
    trees_db = {
        "Eucalipto Grandis": {
            "pH_min": 5.5, "pH_max": 7.0,
            "nitrogen_min": 20, "nitrogen_max": 40,
            "phosphorus_min": 10, "phosphorus_max": 30,
            "potassium_min": 80, "potassium_max": 150,
            "productivity": "Alta",
            "cycle": "Curto (5-7 anos)",
            "uses": "Celulose, Madeira, Óleos Essenciais"
        },
        "Pinus Taeda": {
            "pH_min": 5.0, "pH_max": 6.5,
            "nitrogen_min": 15, "nitrogen_max": 35,
            "phosphorus_min": 8, "phosphorus_max": 25,
            "potassium_min": 70, "potassium_max": 130,
            "productivity": "Média-Alta",
            "cycle": "Médio (10-15 anos)",
            "uses": "Madeira, Resina"
        },
        "Teca": {
            "pH_min": 6.0, "pH_max": 7.5,
            "nitrogen_min": 25, "nitrogen_max": 45,
            "phosphorus_min": 15, "phosphorus_max": 35,
            "potassium_min": 100, "potassium_max": 180,
            "productivity": "Alta",
            "cycle": "Longo (20-25 anos)",
            "uses": "Madeira Nobre"
        },
        "Mogno Africano": {
            "pH_min": 5.8, "pH_max": 7.2,
            "nitrogen_min": 30, "nitrogen_max": 50,
            "phosphorus_min": 20, "phosphorus_max": 40,
            "potassium_min": 120, "potassium_max": 200,
            "productivity": "Média",
            "cycle": "Longo (15-20 anos)",
            "uses": "Madeira de Luxo"
        }
    }

    recommendations = []
    for tree, params in trees_db.items():
        match = True
        if not (params["pH_min"] <= soil_params["pH"] <= params["pH_max"]):
            match = False
        if not (params["nitrogen_min"] <= soil_params["Nitrogênio (ppm)"] <= params["nitrogen_max"]):
            match = False
        if not (params["phosphorus_min"] <= soil_params["Fósforo (ppm)"] <= params["phosphorus_max"]):
            match = False
        if not (params["potassium_min"] <= soil_params["Potássio (ppm)"] <= params["potassium_max"]):
            match = False

        if match:
            recommendations.append({
                "Espécie": tree,
                "Produtividade": params["productivity"],
                "Ciclo": params["cycle"],
                "Usos": params["uses"]
            })

    return pd.DataFrame(recommendations)


# Pest monitoring
def get_pest_monitoring():
    pests = {
        "Cupins": {
            "severity": "Média",
            "affected_area": "Setor B",
            "last_detection": "3 dias atrás",
            "suggestion": "Aplicação de Fipronil 0.3%"
        },
        "Broca-do-eucalipto": {
            "severity": "Alta",
            "affected_area": "Setor A",
            "last_detection": "1 dia atrás",
            "suggestion": "Controle biológico com Beauveria bassiana"
        },
        "Formigas cortadeiras": {
            "severity": "Baixa",
            "affected_area": "Setor C",
            "last_detection": "5 dias atrás",
            "suggestion": "Isca formicida a base de sulfluramida"
        }
    }

    return pd.DataFrame.from_dict(pests, orient='index').reset_index().rename(columns={"index": "Praga"})


# Login screen
def login_page():
    st.title("Agrofloratech - Acesso Restrito")
    st.markdown("** Agronomia Florestal Inteligente**")

    login_form = st.form(key='login_form')
    username = login_form.text_input("Usuário")
    password = login_form.text_input("Senha", type="password")
    submit_button = login_form.form_submit_button("Login")


    if submit_button:
        if username in users_db:
            if check_hashes(password, users_db[username]["password"]):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["user_name"] = users_db[username]["name"]
                st.session_state["access_level"] = users_db[username]["access"]
                st.rerun()
            else:
                st.error("Senha incorreta")
        else:
            st.error("Usuário não encontrado")


# Dashboard
def main_dashboard():
    st.sidebar.title(f"Bem-vindo, {st.session_state['user_name']}")
    st.sidebar.markdown(f"**Nível de acesso:** {st.session_state['access_level']}")

    if st.sidebar.button("🚪 Sair"):
        st.session_state["logged_in"] = False
        st.rerun()

    # soil data
    soil_df = generate_soil_data()
    latest_soil_data = soil_df.iloc[-1].to_dict()

    st.title(" Agrofloratech - Dashboard")
    st.markdown(
        f"**Monitoramento do Solo - Cidade Universitária Uniso, SP** | Última atualização: {soil_df['Data'].iloc[-1].strftime('%d/%m/%Y')}")

    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("pH do Solo", f"{latest_soil_data['pH']:.1f}",
                "0.1" if latest_soil_data['pH'] > soil_df.iloc[-2]['pH'] else "-0.1")
    col2.metric("Matéria Orgânica", f"{latest_soil_data['Matéria Orgânica (%)']:.1f}%",
                "0.2%" if latest_soil_data['Matéria Orgânica (%)'] > soil_df.iloc[-2][
                    'Matéria Orgânica (%)'] else "-0.1%")
    col3.metric("Umidade", f"{latest_soil_data['Umidade (%)']:.1f}%",
                "1.2%" if latest_soil_data['Umidade (%)'] > soil_df.iloc[-2]['Umidade (%)'] else "-0.8%")
    col4.metric("Temperatura", f"{latest_soil_data['Temperatura (°C)']:.1f}°C",
                "0.5°C" if latest_soil_data['Temperatura (°C)'] > soil_df.iloc[-2]['Temperatura (°C)'] else "-0.3°C")

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Análise do Solo", "🌲 Recomendações", "🐜 Monitoramento de Pragas", "📅 Histórico"]) # you can put the name waht you want

    with tab1:
        st.header("Análise de Nutrientes do Solo")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Macronutrientes")
            fig = px.bar(
                x=["Nitrogênio", "Fósforo", "Potássio", "Cálcio", "Magnésio"],
                y=[
                    latest_soil_data["Nitrogênio (ppm)"],
                    latest_soil_data["Fósforo (ppm)"],
                    latest_soil_data["Potássio (ppm)"],
                    latest_soil_data["Cálcio (cmolc/dm³)"],
                    latest_soil_data["Magnésio (cmolc/dm³)"]
                ],
                labels={"x": "Nutriente", "y": "Valor"},
                color=["Nitrogênio", "Fósforo", "Potássio", "Cálcio", "Magnésio"],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Indicadores Físicos")
            fig = px.pie(
                names=["Matéria Orgânica", "Umidade", "Outros Componentes"],
                values=[
                    latest_soil_data["Matéria Orgânica (%)"],
                    latest_soil_data["Umidade (%)"],
                    100 - latest_soil_data["Matéria Orgânica (%)"] - latest_soil_data["Umidade (%)"]
                ],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Tendências dos Últimos 30 Dias")
        selected_metric = st.selectbox(
            "Selecione o parâmetro para visualizar",
            ["pH", "Nitrogênio (ppm)", "Fósforo (ppm)", "Potássio (ppm)",
             "Cálcio (cmolc/dm³)", "Magnésio (cmolc/dm³)", "Matéria Orgânica (%)",
             "Umidade (%)", "Temperatura (°C)"]
        )

        fig = px.line(
            soil_df,
            x="Data",
            y=selected_metric,
            title=f"Variação de {selected_metric} nos últimos 30 dias",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Recomendações de Cultivo")

        if st.button("Gerar Recomendações com Base no Solo Atual"):
            recommendations = get_tree_recommendations(latest_soil_data)

            if not recommendations.empty:
                st.success("Encontramos estas espécies adequadas para seu solo:")

                for idx, row in recommendations.iterrows():
                    with st.expander(f"🌲 {row['Espécie']}"):
                        st.markdown(f"""
                        **Produtividade:** {row['Produtividade']}  
                        **Ciclo de Cultivo:** {row['Ciclo']}  
                        **Principais Usos:** {row['Usos']}
                        """)

                        if st.button(f"Ver detalhes de cultivo para {row['Espécie']}", key=f"details_{idx}"):
                            st.session_state["selected_tree"] = row['Espécie']

                if "selected_tree" in st.session_state:
                    st.subheader(f"Detalhes de Cultivo: {st.session_state['selected_tree']}")

                    if st.session_state["selected_tree"] == "Eucalipto Grandis":
                        st.markdown("""
                        **Densidade de Plantio:** 1.100 a 1.600 plantas/hectare  
                        **Espaçamento:** 3x2m ou 3x3m  
                        **Adubação Recomendada:**  
                        - Plantio: 300g de NPK 06-30-06 + 50g de FTE BR-12  
                        - 6 meses: 200g de NPK 20-05-20  
                        **Cuidados Especiais:** Monitoramento constante de brocas e cupins
                        """)
                    elif st.session_state["selected_tree"] == "Pinus Taeda":
                        st.markdown("""
                        **Densidade de Plantio:** 1.600 a 2.500 plantas/hectare  
                        **Espaçamento:** 2.5x2.5m  
                        **Adubação Recomendada:**  
                        - Plantio: 200g de NPK 10-30-10 + 50g de FTE BR-12  
                        - 12 meses: 300g de NPK 20-10-10  
                        **Cuidados Especiais:** Controle de formigas cortadeiras
                        """)
            else:
                st.warning(
                    "Não encontramos espécies ideais para as condições atuais do solo. Considere corrigir os parâmetros do solo.")

        st.subheader("Simulador de Produtividade")
        st.markdown("Ajuste os parâmetros para simular o impacto nas recomendações:")

        with st.form("soil_simulator"):
            sim_pH = st.slider("pH", 4.0, 8.0, latest_soil_data["pH"], 0.1)
            sim_nitrogen = st.slider("Nitrogênio (ppm)", 5, 50, int(latest_soil_data["Nitrogênio (ppm)"]), 1)
            sim_phosphorus = st.slider("Fósforo (ppm)", 5, 40, int(latest_soil_data["Fósforo (ppm)"]), 1)
            sim_potassium = st.slider("Potássio (ppm)", 50, 250, int(latest_soil_data["Potássio (ppm)"]), 5)

            if st.form_submit_button("Simular Recomendações"):
                simulated_soil = {
                    "pH": sim_pH,
                    "Nitrogênio (ppm)": sim_nitrogen,
                    "Fósforo (ppm)": sim_phosphorus,
                    "Potássio (ppm)": sim_potassium
                }

                sim_recommendations = get_tree_recommendations(simulated_soil)
                st.session_state["sim_recommendations"] = sim_recommendations

        if "sim_recommendations" in st.session_state and not st.session_state["sim_recommendations"].empty:
            st.subheader("Resultados da Simulação")
            st.dataframe(st.session_state["sim_recommendations"])

    with tab3:
        st.header("Monitoramento de Pragas e Doenças")

        pests_df = get_pest_monitoring()
        st.dataframe(pests_df, use_container_width=True, hide_index=True)

        st.subheader("Mapa de Infestação")

        # Mapa fictício
        infestation_data = {
            "Setor": ["A", "B", "C", "D", "E"],
            "Nível de Infestação": ["Alta", "Média", "Baixa", "Nenhuma", "Nenhuma"],
            "Latitude": [-23.50044, -23.50144, -23.49944, -23.50244, -23.49844],
            "Longitude": [-47.39791, -47.39691, -47.39891, -47.39591, -47.39991]
        }

        fig = px.scatter_mapbox(
            pd.DataFrame(infestation_data),
            lat="Latitude",
            lon="Longitude",
            color="Nível de Infestação",
            size=[10, 8, 6, 4, 4],
            hover_name="Setor",
            zoom=14,
            mapbox_style="open-street-map",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recomendações de Controle")
        selected_pest = st.selectbox("Selecione a praga para ver recomendações", pests_df["Praga"].tolist())

        if selected_pest:
            pest_info = pests_df[pests_df["Praga"] == selected_pest].iloc[0]

            st.markdown(f"""
            **Praga:** {pest_info['Praga']}  
            **Severidade:** {pest_info['severity']}  
            **Área Afetada:** {pest_info['affected_area']}  
            **Última Detecção:** {pest_info['last_detection']}  
            **Recomendação:** {pest_info['suggestion']}
            """)

            if st.button("Registrar Aplicação de Defensivo"):
                st.success(
                    f"Aplicação de {pest_info['suggestion']} registrada para {selected_pest} no {pest_info['affected_area']}")

    with tab4:
        st.header("Histórico Completo de Dados")
        st.markdown("Dados dos últimos 30 dias coletados pelos sensores")
        st.dataframe(soil_df, use_container_width=True)

        output = BytesIO()

        with pd.ExcelWriter(output, engine = 'openpyxl') as writer:
            soil_df.to_excel(writer, sheet_name = "Dados_solo", index = False)

        st.download_button(
            label="📥 Baixar Dados Completos",
            data=output.getvalue(),
            file_name="Solo_export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



# Controle de fluxo da aplicação
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_dashboard()
else:
    login_page()
