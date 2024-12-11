import streamlit as st
import requests
import pandas as pd
import requests
import json



st.set_page_config(
    page_title="Projet 10 IA",
    page_icon="🧊"
    
)


source_article = 'https://projet10.blob.core.windows.net/model-artifacts/articles_metadata.csv?sp=racw&st=2024-12-07T16:50:36Z&se=2025-01-11T00:50:36Z&spr=https&sv=2022-11-02&sr=b&sig=WS6H3JpjV2A7PUJI1tprl%2F6jKIA%2BVvDXrNqXUcTwJYc%3D'
source_user = 'https://projet10.blob.core.windows.net/model-artifacts/df_clicks.pkl?sp=r&st=2024-12-10T20:01:09Z&se=2024-12-11T04:01:09Z&spr=https&sv=2022-11-02&sr=b&sig=35X5vRBsoNF%2BBsyIMYMNqmsX2es2FTXRk8YbjupaADY%3D'

article_col=['article_id', 'category_id', 'created_at_ts', 'publisher_id',
       'words_count']

user_col = ['user_id']
@st.cache_data(persist=True)

def load_file(blob_path, col_names):
    source = blob_path
    try:
        # Essayez d'abord de lire le fichier sans spécifier les noms de colonnes
        data = pd.read_csv(source, encoding='latin1')
        # Si col_names est fourni, sélectionnez uniquement ces colonnes
        if col_names:
            data = data[col_names]
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        data = pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur
    
    return data.head(100)


df_article = load_file(source_article,article_col).sample(50)

st.markdown("<h1 style='color: #7350EA;'>Tableau de bord Projet 10 :\n Application de recommandation </h1>", unsafe_allow_html=True)

st.write('### Aperçu des données')       
st.dataframe(df_article,use_container_width= True)




# Fonction pour analyse
st.write('### Test du modèle')

user_input = st.text_input("Veuillez saisir un id utilisateur:")
def analyze_sentiment(text):

    # Url Azure function
    azure_url = "https://httptriggp10.azurewebsites.net/api/http_trigger?"
    
    if user_input:
        response = requests.post(azure_url , params={"user_id": text})
        result  = json.loads(response.content.decode())
            
           
    
    
    st.write( f"## Recommandations pour l'utilisateur {text}")
    # st.write(f"User ID: {result['user']}")

    df_recommendations = pd.DataFrame(result['recommendations'])
    st.dataframe(df_recommendations, use_container_width=True)

    # st.session_state.recommendations_dict= result    
    # st.write(f"**Résultat de l'analyse :** {st.session_state.recommendations_dict}")     

# Bouton pour analyser
if st.button("Obtenir"):
    analyze_sentiment(user_input)




    # Affiche l'interpretation

st.write("")

st.markdown(
    """
    <div style="background-color: #E6F4FA; padding: 10px; border-radius: 5px;">
        <h3 style="color: #262730;">Interprétation</h3>
        <p style="color: #262730;">Les 3 premières recommendations proviennent du modèle collaboratif<br>et les 2 dernières du modèle basé sur le contenu </p>
    </div>
    """,
    unsafe_allow_html=True
)
