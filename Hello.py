# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Integrantes
# Kelly Alejandra Darghan
# Daniel
# Jhon Jairo Sánchez

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hongos App",
        page_icon=":mushroom:",
    )

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
        st.image(uploaded_file, caption="Imagen del hongo.", use_column_width=True)


if __name__ == "__main__":
    run()
