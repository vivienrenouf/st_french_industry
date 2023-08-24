import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json

st.set_page_config(layout="wide")

lille = pd.read_csv('lille_folium.csv')
communes = lille.sort_values(by='TP6020', ascending=False)[['LIBGEO']]
geo_data_lille = json.load(open('lille_folium.geojson'))

with st.sidebar:
    st.sidebar.title("Paramètres")
    select_commune = st.selectbox("Sélectionnez une commune de l'agglomération", (communes))
    
    tx_pauvrete_commune = lille.loc[lille['LIBGEO'] == select_commune, 'TP6020'].values[0]
    delta_moyenne = tx_pauvrete_commune - 14.6
    st.metric(label='Taux de pauvreté de '+ select_commune, value='{} %'.format(tx_pauvrete_commune), delta='{} %'.format(delta_moyenne), delta_color="inverse") #value='{} %'.format(tx_pauvrete_commune))
    st.write("""Le taux de pauvreté représente la part des ménages dont le revenu disponible est inférieur à 60% du niveau de vie médian national. 
    En France, ce taux est de 14,6%. Il s'agit d'un indicateur purement monétaire. \n\n Afin d'aider les agglomérations à lutter contre la pauvreté, 
    cet outil effectue des prédictions du taux de pauvreté à partir de données non monétaires afin de pouvoir aider les collectivités à trouver les leviers nécessaires
     à leurs politiques contre les inégalités""")
    tx_chomage = st.slider('Ajustez le taux de chômage', 0, 100, 20)
    tx_ss_diplome = st.slider('Ajustez le taux de non diplômés', 0, 100, 40)
    tx_inactifs = st.slider("Ajustez le taux d'inactifs", 0, 100, 50)
    tx_location = st.slider('Ajustez le taux de locataires', 0, 100, 80)


st.title("""Taux de pauvreté de l'aire d'attraction de Lille""")
#st.image('pauvrete.jpeg')
#st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.""")

tab1, tab2 = st.tabs(['Réél', 'Prédiction'])

with tab1:
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

    for i in geo_data_lille['features']:
        if i['properties']['LIBGEO'] == select_commune:
            commune = i

    folium.GeoJson(commune, name=select_commune).add_to(m)
    folium.LayerControl().add_to(m)

    st_data = st_folium(m, width=1400)

with tab2:
    st.header('')

#Le code CSS ci-dessous centre les st.metric
css='''
[data-testid="metric-container"] {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] > div {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] label {
    width: fit-content;
    margin: auto;
}
'''

st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)