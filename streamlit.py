import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas
import json

st.set_page_config(layout="wide")

lille = pd.read_csv('lille_folium.csv')
communes = lille['LIBGEO'].sort_values()

with st.sidebar:
    st.sidebar.title("Paramètres")
    st.selectbox("Sélectionnez une commune de l'agglomération", (communes))
    tx_chomage = st.slider('Ajustez le taux de chômage', 0, 100, 20)
    tx_ss_diplome = st.slider('Ajustez le taux de non diplômés', 0, 100, 40)
    tx_inactifs = st.slider("Ajustez le taux d'inactifs", 0, 100, 50)
    tx_location = st.slider('Ajustez le taux de locataires', 0, 100, 80)


st.title("""Prédiction d'un taux de pauvreté monétaire à partir de données non monétaires""")
#st.image('pauvrete.jpeg')
#st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.""")

geo_data_lille = json.load(open('lille_folium.geojson'))


m = folium.Map(location=[50.62, 3.05], zoom_start=10, tiles="CartoDB positron")


choropleth = folium.Choropleth(
    geo_data=geo_data_lille ,
    name="choropleth",
    data=lille,
    columns=["LIBGEO", "TP6020"],
    key_on="feature.properties.LIBGEO",
    fill_color="OrRd",
    nan_fill_color="white",
    fill_opacity=1,
    line_opacity=.5,
    line_color="#5BA69E",
    legend_name="Taux de pauvreté (%)",
    popup=folium.GeoJsonPopup(fields=['LIBGEO'])
).add_to(m)

choropleth.geojson.add_child(folium.features.GeoJsonPopup(fields=['LIBGEO', 'TP6020'], labels=False, localize=True))

st_data = st_folium(m, width=1400)


