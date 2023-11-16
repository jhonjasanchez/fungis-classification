# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Integrantes
# Kelly Alejandra Darghan
# Daniel
# Jhon Jairo Sánchez

import streamlit as st
from streamlit.logger import get_logger
import base64

LOGGER = get_logger(__name__)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def run():
    st.set_page_config(
        page_title="Hongos App",
        page_icon=":mushroom:",
    )

    set_png_as_page_bg('/workspaces/fungis-classification/background.jpg')

    st.write("# Clasificación de Hongos! :mushroom:")

    st.markdown(
        """
        El objetivo de nuestra aplicación Web será el de clasificar los hongos en tres
        tipos de clases:.
        - **Edible**: Comestibles.
        - **Inedible**: No comestibles, aunque no son venenosos, pueden generar alergias o por su sabor no se recomienda su consumo.
        - **Poisonous**: Venenosos, por lo tanto representan un peligro vital si se consumen. 

        ### Nuestro dataset
        - Kaggle [Mushrooms images classification](https://www.kaggle.com/datasets/daniilonishchenko/mushrooms-images-classification-215)
        - Wildfood [Mushroom Guide](https://www.wildfooduk.com)
        - iNaturalist [Taxonomía](https://www.inaturalist.org/taxa/47170-Fungi)
    """
    )

    # Upload la imagen del hongo
    uploaded_file = st.file_uploader("Seleccione una imagen/foto de un hongo: ", type=("jpg", "png"))

    if uploaded_file is not None:
        # Display la imagen del hongo
        st.image(uploaded_file, caption="Imagen del hongo seleccionado.", use_column_width=True)

    if st.button("Clasificar !!!"):
      st.write("Este hongo es: **VENENOSO** !!! :skull_and_crossbones:")
      st.markdown(
          """
            Recomendamos dar una mirada en Wildfood [Hongos venenosos](https://www.wildfooduk.com/mushroom-guide/?mushroom_type=poisonous)
          """
      )
if __name__ == "__main__":
    run()
