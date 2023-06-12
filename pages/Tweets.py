import streamlit as st
import tweepy
import re
from textblob import TextBlob
from streamlit_javascript import st_javascript

st.set_page_config(page_title = "Emotions Tweets", page_icon="assets/TwitterIcon.png")

API_KEY             = 'PmZro1geo9ZIiJ1hN31BCydIv'
API_SECRET_KEY      = 'MOLOO4Yr5PN2LzQu1DIP5NFt0uqcXMTAxKYiZFowiE540HFYFl'
BEARER_TOKEN        = 'AAAAAAAAAAAAAAAAAAAAADf6ngEAAAAADRUfdlWUAPFL2yPz85Bemfxso7Y%3Dkj8a5yDSTPMa3aiRmeAUTke2sOMThzPehrsolBp28PS4qiJCrT'
ACCESS_TOKEN        = '965774104157741059-t0J8mATP0Sc9UhuvruW6keX0o8JvC1i'
ACCESS_TOKEN_SECRET = 'v7IOJXhJfFTIoUJedltl6BinzhJ1ehHQ7rNrzLtJznZ9b'

#Bootstrap
st.markdown('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">', unsafe_allow_html=True)

st.markdown("""
<style>
h1, h2, h3, h4, h5, h6 {
    font-size: 30px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


def traducir_texto(texto, idioma_origen, idioma_destino):
    # Crear un objeto TextBlob con el texto en el idioma de origen
    blob = TextBlob(texto)
    
    # Realizar la traducción al idioma destino
    texto_traducido = blob.translate(from_lang=idioma_origen, to=idioma_destino)
    
    return str(texto_traducido)


class ConexionTwitter:
    def __init__(self):
        self.auth       = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api        = tweepy.API( self.auth )
    

    def getApi(self):
        return self.api

    def limpiar_texto_twits( self, lista_twits ):
        twits_sin_emojis = [ self.deEmojify( twit) for twit in lista_twits ]
        return twits_sin_emojis


    def traducir_twits( self, lista_twits ):

        # try:
        twits_ingles = [ TextBlob( twit).translate( from_lang="es", to="en") for twit in lista_twits ]
        return twits_ingles
        # except Exception as ex:
        #   print( "Error twits_ingles")
        #   print( ex , "   \n\n\n")

        return []

    def deEmojify( self, text):
        regrex_pattern = re.compile(pattern = "["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002500-\U00002BEF"  # chinese char
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                           "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    def buscarTwitsTendencias( self, tendencia, n_tweets ):
        # Obtener 1000 tweets de las 3 tendencias actuales

        lista_twits =  self.api.search_tweets( q=tendencia, lang ="es", count=n_tweets ) 

        # La siguiente lista contiene los twits con los emojis y espacios innecesarios
        lista_twits_texto_sucia = [ twit._json["text"].strip() for twit in lista_twits]
        
        # Lista de los twits sin emojis en español
        twits_limpios = self.limpiar_texto_twits( lista_twits_texto_sucia )
        lista_twits_tendencia = twits_limpios
        twits_ingles = self.traducir_twits( twits_limpios )
        
        for i in range( len (twits_ingles )):
            st.write( f"""{i+1}. { lista_twits_tendencia[i]}""" )
            
        print( len( twits_limpios ))
        return twits_ingles

class Obtener_porcentaje():
    
    def obtener_lista_porcentajes( self, lista_twits ):
        return [ self.obtener_porcentaje( twit ) for twit in lista_twits ]
          

    def obtener_porcentaje( self, text ):
        return text.sentiment.polarity


def get_from_local_storage(k):
    v = st_javascript(f"JSON.parse(localStorage.getItem('{k}'));", key="unique" )
    return v or {}


def redireccion():
    st.write(f'''
        <a target="_self" href="http://localhost:8501/Gráficas">
            <button class="btn btn-primary">
                Gráficas
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )

lista_twits_tendencia = []

def tweets():
    st.title("Tweets:")
    data = get_from_local_storage("tendencia")

    try:
        info = f"""La tendencia es {data[0]} y la cantidad de tweets es {data[1]}"""
        info_english = traducir_texto( info, "es", "en")
        st.write( info )
        st.write( info_english )
    except KeyError as e:
        # Manejar la excepción KeyError aquí
        st.write( "Por favor ve a la sección de trending topics y selecciona la tendencia!" )
        info_english_dos = traducir_texto( "Por favor ve a la sección de trending topics y selecciona la tendencia!", "es", "en")
        st.write( info_english_dos )
        st.components.v1.html('<img src="https://media.tenor.com/uCMXQo80r0kAAAAC/guino-ozuna.gif" alt="GIF">', width=600, height=300)
    
    conex       = ConexionTwitter   ()
    porcentajes = Obtener_porcentaje()

    try:
        twits_ingles = conex.buscarTwitsTendencias( data[0], data[1] )
    except Exception as e:
        print("Error al buscar los tweets, muchas peticiones")
        twits_ingles = []
        
    lista_porcentajes = porcentajes.obtener_lista_porcentajes( twits_ingles )
        
    js_code = f"""
    <script>
        localStorage.setItem("porcentajes", JSON.stringify( {lista_porcentajes} ));
    </script>
    """
    st.components.v1.html(js_code)


tweets()