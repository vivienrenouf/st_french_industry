import streamlit as st

st.title("""Indicateur de pauvreté""")
st.image('pauvrete.jpeg')
st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.
""")


chomage = st.slider('Ajustez le taux de chômage', 0, 100, 50)
st.write('Le taux de chômage est de', chomage)