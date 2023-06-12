import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
from streamlit_javascript import st_javascript
import random as r
import numpy as np
import matplotlib.patches as mpatches
import pyautogui, webbrowser
from time import sleep

st.set_page_config(page_title = "Emotions Tweets", page_icon="assets/TwitterIcon.png")

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


random_numbers = [random.uniform(-1, 1) for _ in range(10)]
contador = 0

def separar_tendencias_en_dominios_porcentajes( lista_promedios ):

    array       = np.array( lista_promedios )
    condiciones = [ (array >= -1) & (array < -0.5),
                    (array >= -0.5) & (array < 0),
                    (array == 0),
                    (array > 0) & (array <= 0.5),
                    (array > 0.5) & (array <= 1)]

    sublistas = [array[condicion] for condicion in condiciones]
    sublistas_python = [list(sublista) for sublista in sublistas]

    return sublistas_python



def separar_diccionario_con_listas( lista_sublistas ):
    return {
        "muy_enojado"   : lista_sublistas[0],
        "enojado"       : lista_sublistas[1],
        "neutral"       : lista_sublistas[2],
        "alegre"        : lista_sublistas[3],
        "muy_alegre"    : lista_sublistas[4]
    }


def get_from_local_storage(k):
    global contador
    v = st_javascript(f"JSON.parse(localStorage.getItem('{k}'));", key=f"""{ contador}""")
    contador = contador + 1

    sub_listas_porcentajes  = separar_tendencias_en_dominios_porcentajes( v ) 
    diccionario             = separar_diccionario_con_listas( sub_listas_porcentajes ) 
    return diccionario or {}


def grafics():
    st.title("Gráficas:")
    st.write(f"""Estas son las gráficas para la tendencia seleccionada:""")
    
    diagrama_dispersion()
    diagrama_barras()
    diagrama_pastel()
    diagrama_desviacion()
    
    st.write(f'''
        <a target="_self" href="http://localhost:8501/Conclusiones">
            <button class="btn btn-primary">
                Ir a Conclusiones
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )
        

def diagrama_barras():
    # Datos para el gráfico
    diccionario = get_from_local_storage("porcentajes")

    lista_nombres       = ["Muy enojado", "Enojado", "Neutral", "Alegre", "Muy alegre"]
    lista_frecuencias  = [ len( dato ) for dato in diccionario.values() ]

    # Gráfico de barras
    fig, ax = plt.subplots()
    fig.suptitle("Diagrama de barras")
    ax.bar(x = lista_nombres, height = lista_frecuencias, color=['black', 'red', 'green', 'blue', 'cyan'] )
    plt.show() 
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

def diagrama_dispersion():
    # Datos para el gráfico
    diccionario = get_from_local_storage("porcentajes")

    matriz_frecuencias = list(diccionario.values())
    lista_frecuencias       = np.concatenate( matriz_frecuencias ).tolist()
    datos_x                 = np.array( lista_frecuencias )
    conditions              = [    (datos_x >= -1) & (datos_x < -0.5),    (datos_x >= -0.5) & (datos_x < 0),    (datos_x == 0),    (datos_x > 0) & (datos_x <= 0.5),    (datos_x > 0.5) & (datos_x <= 1)]
    frecuencias_redondeadas = [ round( dato * 10, 0 ) for dato in lista_frecuencias ]
    
    num_twit                = [ i for i in range( len( frecuencias_redondeadas ))]

    colors_opt  = ['black', 'red', 'green', 'blue', 'cyan']
    color       = np.select( conditions, colors_opt, default="yellow")

    fig, ax = plt.subplots()
    ax.scatter( num_twit, frecuencias_redondeadas, c = color)
    fig.suptitle("Diagrama de disperción")
    rojo    = mpatches.Patch(color = "black"  , label = "Muy enojado")
    azul    = mpatches.Patch(color = "red" , label = "Enojado")
    cafe    = mpatches.Patch(color = "green", label = "Neutral")
    rosado  = mpatches.Patch(color = "blue" , label = "Alegre")
    verde   = mpatches.Patch(color = "cyan", label = "Muy alegre")

    plt.legend(handles = [rojo, azul, cafe, rosado, verde ])
    plt.xlabel('Numero de tweet')
    plt.ylabel('Cantidad de emocion ( entre mas grande el numero mas feliz y viceversa )')
    plt.show()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    

def mensaje_whatsapp(numero, muy_enojados, enojados, neutral, alegre, muy_alegre, desviacion_general):
    
    mensaje = """Hola, gracias por usar los servicios de Emotions_Tweet!
        Muy Enojados: {:.16f}
        Enojados: {:.16f}
        Neutral: {:.1f}
        Alegres: {:.16f}
        Muy alegres: {:.16f}
        Desviación en general: {:.16f}
        """.format(muy_enojados, enojados, neutral, alegre, muy_alegre, desviacion_general)
    
    webbrowser.open('https://web.whatsapp.com/send?phone=' + str(numero) + "&text=" + mensaje)
    sleep(8)
    pyautogui.click(1230, 964)
    sleep(1)
    pyautogui.press('enter')


def diagrama_desviacion():
    # Datos para el gráfico
    diccionario = get_from_local_storage("porcentajes")

    des_muy_enojado    = np.std( diccionario["muy_enojado"] )
    des_enojado        = np.std( diccionario["enojado"] )
    des_neutral        = np.std( diccionario["neutral"] )
    des_alegre         = np.std( diccionario["alegre"] )
    des_muy_alegre     = np.std( diccionario["muy_alegre"] )

    st.write("Desviaciones estandar: ")

    #Validaciones
    if( len( diccionario["muy_enojado"] ) != 0 ):
        st.write(f"""Muy enojados: {des_muy_enojado}""")
        
    if( len( diccionario["enojado"] ) != 0 ):
        st.write(f"""Enojados: {des_enojado}""")

    if( len( diccionario["neutral"] ) != 0 ):
        st.write(f"""Neutral: {des_neutral}""")
    
    if( len( diccionario["alegre"] ) != 0 ):
        st.write(f"""Alegres: {des_alegre}""")
    
    if( len( diccionario["muy_alegre"] ) != 0 ):
        st.write(f"""Muy alegres: {des_muy_alegre}""")

    matriz_frecuencias      = np.array(  list( diccionario.values() ) , dtype=object )
    lista_frecuencias       = np.concatenate( matriz_frecuencias ).tolist()

    st.write(f"""Desviacion en general: { np.std( lista_frecuencias )}""")
    
    mensaje = st.number_input('Ingresa tu numero de telefono para hacerte llegar los resultados:')
    numero = int(mensaje)
    
    if numero < 0:
        st.markdown('<p style="color:red;">Por favor ingresa un número válido</p>', unsafe_allow_html=True)
    elif len(str(numero)) < 10:
        st.markdown('<p style="color:red;">El número de teléfono debe tener al menos 10 dígitos</p>', unsafe_allow_html=True)
    else:
        mensaje_whatsapp(numero, des_muy_enojado, des_enojado, des_neutral, des_alegre, des_muy_alegre, np.std( lista_frecuencias ))
    


def diagrama_pastel():
    # Datos para el gráfico
    diccionario = get_from_local_storage("porcentajes")
    lista_nombres           = ["Muy enojado", "Enojado", "Neutral", "Alegre", "Muy alegre"]
    matriz_frecuencias = list(diccionario.values())
    lista_frecuencias = [len(sublista) for sublista in matriz_frecuencias]
    colors_opt  = ['black', 'red', 'green', 'blue', 'cyan']
    fig, ax = plt.subplots()
    plt.pie( lista_frecuencias, labels=lista_nombres, colors=colors_opt, autopct="%0.1f %%" )
    plt.axis("equal")
    plt.title("Diagrama circular")
    plt.show()
    # Mostrar el gráfico en Streamlit
    st.pyplot( fig )

grafics()