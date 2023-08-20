import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd



with st.sidebar:
    st.selectbox('Sélectionnez une commune', ('Rouen', 'Mont-Saint_Aignan', 'Petit-Quevilly'))
    tx_chomage = st.slider('Ajustez le taux de chômage', 0, 100, 20)
    tx_ss_diplome = st.slider('Ajustez le taux de non diplômés', 0, 100, 40)
    tx_inactifs = st.slider("Ajustez le taux d'inactifs", 0, 100, 50)
    tx_location = st.slider('Ajustez le taux de locataires', 0, 100, 80)


st.title("""Indicateur de pauvreté""")
#st.image('pauvrete.jpeg')
#st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.""")

df = pd.read_csv('lille_folium.csv')

# center on Liberty Bell, add marker
m = folium.Map(location=[50.62, 3.05], zoom_start=10, tiles="CartoDB positron")

for _, r in df.iterrows():
    # Without simplifying the representation of each borough,
    # the map might not be displayed
    sim_geo = geopandas.GeoSeries(r["geometry"]).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
    folium.Popup(r["LIBGEO"]).add_to(geo_j)
    geo_j.add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)


