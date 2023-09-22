import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
import pickle
import numpy as np

st.set_page_config(layout="wide")

lille = pd.read_csv('lille_all_data.csv')
communes = lille[lille.TP6020.isna() == False].sort_values(by='LIBGEO', ascending=True)[['LIBGEO']].reset_index(drop=True) #Tri des communes par ordre alphabétique pour la sélection
geo_data_lille = json.load(open('lille_folium.geojson'))

pickle_filename = "pauvrete_model.pkl"
with open(pickle_filename, 'rb') as file:
    model = pickle.load(file)



#st.image('pauvrete.jpeg')
#st.write("""La variable TP6020 est une variable publiée par l’INSEE correspondant au taux de pauvreté en 2020. Ce taux est calculé pour les personnes logées de manière ordinaire en France métropolitaine. Il exclut donc les sans-abris et les populations occupant des habitations mobiles. Les ménages dont la personne de référence est étudiante sont aussi exclus de l’analyse. Ce taux est calculé par l’INSEE à partir de l’enquête Revenus fiscaux et sociaux (ERFS), réalisée annuellement.""")


with st.sidebar:
    st.sidebar.title("Paramètres")


    select_commune = st.selectbox("Sélectionnez une commune de l'aire d'attraction de Lille", (communes),  index=43) #l'index 43 correspond à la commune de Lille. Affichage par défaut.

    #Pour fonctionner correctement en fonction du dropdown menu, et même si les indicateurs ne sont pas dans le sidebar, ces variables doivent être stockées directement après le select_commune et en amont des jauges.
    tx_pauvrete_commune = lille.loc[lille['LIBGEO'] == select_commune, 'TP6020'].values[0]
    tx_pauvrete_france = 14.6
    delta_moyenne = np.round(tx_pauvrete_commune - tx_pauvrete_france,1)

    population_commune = int(lille.loc[lille['LIBGEO'] == select_commune, 'pop_tot'].values[0])

    tx_chomage_commune = lille.loc[lille['LIBGEO'] == select_commune, 'Taux_chomage'].values[0]

    tx_ss_diplome_commune = lille.loc[lille['LIBGEO'] == select_commune, 'taux_sans_diplome'].values[0]

    tx_inactifs_commune = lille.loc[lille['LIBGEO'] == select_commune, 'taux_inactifs'].values[0]

    tx_location_commune = lille.loc[lille['LIBGEO'] == select_commune, 'taux_loc_princ'].values[0]

    with st.container():
        col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Taux de pauvreté monétaire', value='{} %'.format(tx_pauvrete_commune).replace('.',','), delta='{} %'.format(delta_moyenne).replace('.',','), delta_color="inverse")
    with col2:
        st.metric(label='Population', value='{:,}'.format(population_commune).replace(',','.'))

    st.write('Ajustez les jauges et observez la prédiction !')

    tx_chomage = st.slider('Taux de chômage', 0.0, 100.0, tx_chomage_commune, step=0.1, format="%f")
    tx_ss_diplome = st.slider('Taux de non diplômés', 0.0, 100.0, tx_ss_diplome_commune, step=0.1, format="%f")
    tx_inactifs = st.slider("Taux d'inactifs", 0.0, 100.0, tx_inactifs_commune, step=0.1, format="%f")
    tx_location = st.slider('Taux de locataires (hab. princ.)', 0.0, 100.0, tx_location_commune, step=0.1, format="%f")

    inputs = [[tx_chomage, tx_ss_diplome, tx_location, tx_inactifs]]
    prediction = model.predict(inputs)
    rounded_prediction = np.round(prediction[0], 1)
    st.success('Prédiction : {} %'.format(rounded_prediction))
    st.metric(label='Prédiction', value='{} %'.format(rounded_prediction))

    st.divider()
    st.caption(""" \* L'INSEE ne publie qu'une partie des données communales (secret statistique). 
             Cet outil ne tient compte que des communes pour lesquelles les données sont publiées. 
             Les autres communes ne sont pas sélectionnables et sont représentées en blanc sur les cartographies.""")
    
    

st.title("Analyse de la pauvreté à " + select_commune)

tab1, tab2 = st.tabs(['Cartographie', 'Instructions'])

#Premier onglet
with tab1:

    with st.container():
        #st.subheader(select_commune)
        col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label='Taux de chômage', value='{} %'.format(tx_chomage_commune).replace('.',','))
    with col2:
        st.metric(label='Taux de non diplômés', value='{} %'.format(tx_ss_diplome_commune).replace('.',','))
    with col3:
        st.metric(label="Taux d'inactifs", value='{} %'.format(tx_inactifs_commune).replace('.',','))
    with col4:
        st.metric(label="Taux de locataires (hab. princ.)", value='{} %'.format(tx_location_commune).replace('.',','))


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

    choropleth.geojson.add_child(folium.features.GeoJsonPopup(fields=['LIBGEO'], labels=False, localize=True))

    #Ce bloc permet de highlight le territoire choisi dans le menu dropdown
    for i in geo_data_lille['features']:
        if i['properties']['LIBGEO'] == select_commune:
            commune = i

    folium.GeoJson(commune, name=select_commune, style_function=lambda x : {'fillOpacity':.0}).add_to(m)
    folium.LayerControl().add_to(m)
    st_data = st_folium(m, width='100%')


    st.caption(""" Crédits : Frédérique RAOUX - Marie-Hélène IZQUIERDO - Dominique MOLL - Vivien RENOUF \nProjet cursus Data Analyst 2023 - Datascientest""")

#Deuxième onglet
with tab2:
    st.header('Instructions')

    st.write("""Le taux de pauvreté représente la part des ménages dont le revenu disponible est inférieur à 60% du niveau de vie médian national. 
    En France, ce taux est de 14,6%. Il s'agit d'un **indicateur purement monétaire**, que l'INSEE publie également au niveau communal*. \n\n Afin de 
    lutter contre la pauvreté, prédire le taux de pauvreté monétaire **à partir de données non monétaires**, axées sur l'emploi, la formation et 
    le logement, peut aider les agglomérations à cibler les politiques à mener. \n\n En simulant des variations sur les axes proposés, quel 
    pourrait être l'impact sur le taux de pauvreté de la commune sélectionnée ? \n\n Ajustez les jauges et observez la prédiction !
    """)


#Le code CSS ci-dessous centre les st.metric
css_metrics='''
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

st.markdown(f'<style>{css_metrics}</style>',unsafe_allow_html=True)

css_header = '''
[data-testid="StyledLinkIconContainer"] {
    width: fit-content;
    margin: auto;
}

'''

st.markdown(f'<style>{css_header}</style>',unsafe_allow_html=True)

make_map_responsive= """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)


css_slider_text = '''
div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p{
font-size: 18px;
}
'''

st.markdown(f'<style>{css_slider_text}</style>',unsafe_allow_html=True)

css_slider_num = '''
[data-testid="stThumbValue"] {
font-size: 16px;
}
'''

st.markdown(f'<style>{css_slider_num}</style>',unsafe_allow_html=True)

css_metric_title = '''
div[data-testid="metric-container"] > label > div[class="css-1wivap2 e1i5pmia3"] > div[data-testid="stMarkdownContainer"] > p {
font-size: 18px;
}

'''

st.markdown(f'<style>{css_metric_title}</style>',unsafe_allow_html=True)
