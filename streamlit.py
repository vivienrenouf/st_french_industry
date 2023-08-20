import streamlit as st



with st.sidebar:
    chomage = st.slider('Ajustez le taux de chômage', 0, 100, 20)
    ss_diplome = st.slider('Ajustez le taux de non diplômés', 0, 100, 40)
    tx_INACTIFS = st.slider("Ajustez le taux d'inactifs", 0, 100, 50)
    tx_location = st.slider('Ajustez le taux de locataires', 0, 100, 80)


st.title("""Indicateur de pauvreté""")
st.image('pauvrete.jpeg')
st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.
    """)


