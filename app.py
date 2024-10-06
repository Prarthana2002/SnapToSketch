import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# Streamlit Interface
st.title("SketchMaster: Instant Art Converter")

# Sketch Effect Section
st.header("Convert Image to Sketch")

# File uploader for image input
uploaded_image = st.file_uploader("Upload an image to convert to sketch:", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Button to convert image to sketch
    if st.button("Convert to Sketch"):
        img = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        inv_gray = 255 - gray
        blurred = cv2.GaussianBlur(inv_gray, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)

        sketch_pil = Image.fromarray(sketch)
        st.image(sketch_pil, caption='Sketch Image', use_column_width=True)

        # Download option for the sketch image
        img_byte_arr = BytesIO()
        sketch_pil.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        st.download_button(
            label="Download Sketch",
            data=img_byte_arr,
            file_name="sketch_image.png",
            mime="image/png"
        )
