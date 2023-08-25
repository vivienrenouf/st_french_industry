import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json

st.set_page_config(layout="wide")

lille = pd.read_csv('lille_all_data.csv')
communes = lille.sort_values(by='TP6020', ascending=False)[['LIBGEO']]
geo_data_lille = json.load(open('lille_folium.geojson'))



st.title("""Taux de pauvreté de l'aire d'attraction de Lille""")
#st.image('pauvrete.jpeg')
#st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.""")



with st.sidebar:
    st.sidebar.title("Instructions")
    select_commune = st.selectbox("Sélectionnez une commune de l'agglomération", (communes))

    #Pour fonctionner correctement en fonction du dropdown menu, et même si les indicateurs ne sont pas dans le sidebar, ces variables doivent être stockées directement après le select_commune et en amont des jauges.
    tx_pauvrete_commune = lille.loc[lille['LIBGEO'] == select_commune, 'TP6020'].values[0]
    tx_pauvrete_france = 14.6
    delta_moyenne = tx_pauvrete_commune - tx_pauvrete_france

    tx_chomage_commune = lille.loc[lille['LIBGEO'] == select_commune, 'Taux_chomage'].values[0]

    tx_ss_diplome_commune = lille.loc[lille['LIBGEO'] == select_commune, 'taux_sans_diplome'].values[0]

    tx_inactifs_commune = lille.loc[lille['LIBGEO'] == select_commune, 'taux_inactifs'].values[0]

    tx_location_commune = lille.loc[lille['LIBGEO'] == select_commune, 'taux_loc_princ'].values[0]

    st.write("""Le taux de pauvreté représente la part des ménages dont le revenu disponible est inférieur à 60% du niveau de vie médian national. 
    En France, ce taux est de 14,6%. Il s'agit d'un indicateur purement monétaire. \n\n Afin d'aider les agglomérations à lutter contre la pauvreté, 
    cet outil effectue des prédictions du taux de pauvreté monétaire **à partir de données non monétaires**. 
    En effectuant des simulations axées sur l'emploi, la formation et le logement, les collectivités pourront observer l'impact que pourraient avoir leurs futures politiques contre
    les inégalités.\n\n Ajustez les taux ci-dessous et observez la prédiction du taux de pauvreté :""")
    tx_chomage = st.slider('Ajustez le taux de chômage', 0, 100, int(tx_chomage_commune))
    tx_ss_diplome = st.slider('Ajustez le taux de non diplômés', 0, 100, int(tx_ss_diplome_commune))
    tx_inactifs = st.slider("Ajustez le taux d'inactifs", 0, 100, int(tx_inactifs_commune))
    tx_location = st.slider('Ajustez le taux de locataires', 0, 100, int(tx_location_commune))


tab1, tab2 = st.tabs(['Réél', 'Prédiction'])

#Premier onglet
with tab1:

    with st.container():
        st.header(select_commune)
        col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label='Taux de pauvreté monétaire à '+ select_commune, value='{} %'.format(tx_pauvrete_commune), delta='{} %'.format(delta_moyenne), delta_color="inverse")
    with col2:
        st.metric(label='Taux de chômage à '+ select_commune, value='{} %'.format(tx_chomage_commune))
    with col3:
        st.metric(label='Taux de non diplômés à '+ select_commune, value='{} %'.format(tx_ss_diplome_commune))
    with col4:
        st.metric(label="Taux d'inactifs à" + select_commune, value='{} %'.format(tx_inactifs_commune))
    with col5:
        st.metric(label="Taux de locataires (hab. princ.) à" + select_commune, value='{} %'.format(tx_location_commune))

    with st.container():
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

    #Ce bloc permet de highlight le territoire choisi dans le menu dropdown
        for i in geo_data_lille['features']:
            if i['properties']['LIBGEO'] == select_commune:
                commune = i

        folium.GeoJson(commune, name=select_commune).add_to(m)
        folium.LayerControl().add_to(m)
        st_data = st_folium(m, width='100%')

#Deuxième onglet
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

make_map_responsive= """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)