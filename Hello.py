# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Integrantes
# Kelly Alejandra Darghan
# Daniel
# Jhon Jairo Sánchez

import streamlit as st
import torch
from torchvision.ops import nms
from PIL import Image, ImageDraw

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def save_uploaded_image(uploaded_image):
    # Save the uploaded image to a temporary file and return the file path
    with st.spinner("Saving uploaded image..."):
        image_bytes = uploaded_image.read()
        image_path = f"{uploaded_image.name}"
        
        with open(image_path, "wb") as temp_image:
            temp_image.write(image_bytes)

    return image_path

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
      class_name = ''
      # Cargar el modelo
      try:
            model = torch.hub.load("ultralytics/yolov5:master", "custom", path=model_path)
            st.write("Model loaded successfully.")
            image_path = save_uploaded_image(uploaded_file)
            st.write('path: ',image_path)
            results = model(image_path)
            
            st.write(results)

            conf_threshold = 0.5
            iou_threshold = 0.4

            boxes = results.xyxy[0][:, :4].cpu()
            scores = results.xyxy[0][:, 4].cpu()
            class_indices = results.xyxy[0][:, 5].cpu()
            keep = nms(boxes, scores, iou_threshold)
            st.write('boxes: ', boxes)
            st.write('class_indices: ', class_indices)

            original_image = Image.open(image_path).convert("RGB")

            # Check if there are any detections
            if len(keep) > 0:
                # Draw bounding boxes on the image
                image_with_boxes = original_image.copy()
                draw = ImageDraw.Draw(image_with_boxes)

                # Iterate through the kept indices and draw bounding boxes
                for idx in keep:
                    box = tuple(map(int, boxes[idx]))
                    conf = scores[idx]
                    class_index = int(class_indices[idx])
                    
                    if class_index == 0:
                        class_name = 'Comestible'
                    if class_index == 1:
                        class_name = 'No comestible'
                    if class_index == 2:
                        class_name = 'Venenoso'
                    label = f"{class_name} Confidence: {conf:.2f}"
                    draw.rectangle(box, outline="red", width=3)
                    draw.text((box[0], box[1]), label, fill="white")

                # Display the image with bounding boxes
                st.image(image_with_boxes, caption="Image with Bounding Boxes", use_column_width=True)
            else:
                st.write("No detections found.")

            #prediction_list = getattr(results, 'pred', None)
            #st.write("prediction_list: ", prediction_list)

      except Exception as e:
            st.write("Error loading model:", e)
      if class_name == 'Venenoso':
            st.write("Este hongo es: **VENENOSO** !!! :skull_and_crossbones:")
            st.markdown(
                """
                    Recomendamos dar una mirada en Wildfood [Hongos venenosos](https://www.wildfooduk.com/mushroom-guide/?mushroom_type=poisonous)
                """
            )
      if class_name == 'Comestible':
            st.write("Este hongo es: **COMESTIBLE** !!! 🍕")
            st.markdown(
                """
                    Recomendamos dar una mirada en Wildfood [Hongos Comestibles](https://www.wildfooduk.com/mushroom-guide/?mushroom_type=edible)
                """
            )
      if class_name == 'No comestible':
            st.write("Este hongo es: **NO COMESTIBLE** !!! ❌")
            st.markdown(
                """
                    Recomendamos dar una mirada en Wildfood [Hongos no comestibles](https://www.wildfooduk.com/mushroom-guide/?mushroom_type=inedible)
                """
            )
if __name__ == "__main__":
    run()
