import streamlit as st
import webbrowser
import tweepy
from textblob import TextBlob

st.set_page_config(page_title = "Emotions Tweets", page_icon="assets/TwitterIcon.png")

API_KEY             = 'PmZro1geo9ZIiJ1hN31BCydIv'
API_SECRET_KEY      = 'MOLOO4Yr5PN2LzQu1DIP5NFt0uqcXMTAxKYiZFowiE540HFYFl'
BEARER_TOKEN        = 'AAAAAAAAAAAAAAAAAAAAADf6ngEAAAAADRUfdlWUAPFL2yPz85Bemfxso7Y%3Dkj8a5yDSTPMa3aiRmeAUTke2sOMThzPehrsolBp28PS4qiJCrT'
ACCESS_TOKEN        = '965774104157741059-t0J8mATP0Sc9UhuvruW6keX0o8JvC1i'
ACCESS_TOKEN_SECRET = 'v7IOJXhJfFTIoUJedltl6BinzhJ1ehHQ7rNrzLtJznZ9b'


def traducir_texto(texto, idioma_origen, idioma_destino):
    # Crear un objeto TextBlob con el texto en el idioma de origen
    blob = TextBlob(texto)
    
    # Realizar la traducción al idioma destino
    texto_traducido = blob.translate(from_lang=idioma_origen, to=idioma_destino)
    
    return str(texto_traducido)


st.markdown("""
<style>
h1, h2, h3, h4, h5, h6 {
    font-size: 30px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


class ConexionTwitter:
    def __init__(self):
        self.auth       = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api        = tweepy.API( self.auth )
    

    def getApi(self):
        return self.api


class ObtenerTendencias:

    def __init__(self):
        self.conexion = ConexionTwitter()
        self.api = self.conexion.getApi()
        

    def obtenerTendenciasCol( self ):
        woeid = 368149
        trends = self.api.get_place_trends( woeid )

        nombresTrends = []
        for trend in trends[0]["trends"]:
            nombresTrends.append( trend["name"])

        return nombresTrends

#Lista quemada donde deveria de ser las tendencis que traiga la api
tendencias = ObtenerTendencias()
lista = tendencias.obtenerTendenciasCol()

def guardar_seleccion(palabra, num):
    js_code = f"""<script>localStorage.setItem("tendencia", JSON.stringify( {[ palabra, num]} ));</script>"""
    st.components.v1.html(js_code)

def trending_topics():
    st.title("Trending Topics:")
    st.write('Seleccione el número de tweets:')
    st.write(traducir_texto('Seleccione el número de tweets:', 'es', 'en'))
    
    int_val = st.slider('', 20, 80, 20)
    html_code = """
    <div>
        <h4>Trending Topics in Colombia: </h4>
    </div>"""
    
    # Mostrar el código HTML en la página
    st.markdown( html_code , unsafe_allow_html=True )
    st.write('Seleccione una tendencia:')
    st.write(traducir_texto('Seleccione una tendencia:', 'es', 'en'))
    
    for i in range(len(lista)):
        col1, col2 = st.columns([0.1, 3])
        with col1:
            st.write(f"{i+1}.")
        with col2:
            if st.button(lista[i], key=f"{i}"):
                st.markdown("<h6>Por favor diríjase al apartado de tweets para visualizarlos!</h6>", unsafe_allow_html=True)
                guardar_seleccion(lista[i], int_val)
    
    
trending_topics()