# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Integrantes
# Kelly Alejandra Darghan
# Daniel
# Jhon Jairo Sánchez

import streamlit as st
import torch
from PIL import Image, ImageDraw
from torchvision.transforms import functional as F
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.plots import plot_one_box

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

# Function to perform YOLOv5 inference on an image
def inference(image, model):
    img_tensor = F.to_tensor(image).unsqueeze(0)
    
    # Perform inference
    with torch.no_grad():
        results = model(img_tensor)

    # Process the YOLOv5 model output
    results = non_max_suppression(results[0], conf_thres=0.5, iou_thres=0.4)
    
    return results[0] if results else None

# Function to draw bounding boxes on the image
def draw_boxes(image, boxes):
    draw = ImageDraw.Draw(image)

    for box in boxes:
        label = int(box[5])
        plot_one_box(box, draw, label=label, color='red')

    return image

def run():
    st.set_page_config(
        page_title="Hongos App",
        page_icon=":mushroom:",
    )

    image_url = "background.jpg"
    st.image(image_url, caption="", use_column_width=True)

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
      # Ruta al modelo entrenado
      model_path = "best.pt"

      # Cargar el modelo
      try:
            model = torch.hub.load("ultralytics/yolov5:master", "custom", path=model_path)
            st.write("Model loaded successfully.")
            image = Image.open(uploaded_file).convert("RGB")
            results = inference(image)

             # Display the original image
            st.image(image, caption="Original Image", use_column_width=True)

            if results:
                # Draw bounding boxes on the image
                image_with_boxes = draw_boxes(image.copy(), results[:, :5])
                st.image(image_with_boxes, caption="Image with Bounding Boxes", use_column_width=True)


      except Exception as e:
            st.write("Error loading model:", e)

      st.write("Este hongo es: **VENENOSO** !!! :skull_and_crossbones:")
      st.markdown(
          """
            Recomendamos dar una mirada en Wildfood [Hongos venenosos](https://www.wildfooduk.com/mushroom-guide/?mushroom_type=poisonous)
          """
      )
if __name__ == "__main__":
    run()
