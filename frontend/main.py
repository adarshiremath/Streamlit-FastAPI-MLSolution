import time
import requests
import streamlit as st
from PIL import Image
from io import BytesIO

STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the scream": "the_scream",
    "the wave": "the_wave",
    "udnie": "udnie",
}

st.title("Style Transfer Web App")

image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
style = st.selectbox("Choose the style", list(STYLES.keys()))

if st.button("Style Transfer"):
    if image is not None and style is not None:
        st.write("Processing...")
        files = {"file": image.getvalue()}
        try:
            res = requests.post(f"http://backend:8080/{STYLES[style]}", files=files)
            res.raise_for_status()  # Raise an error for bad HTTP status codes
            img_path = res.json()
            image = Image.open(img_path.get("name"))
            st.image(image, caption=f"Styled with {style}", use_column_width=True)

            displayed_styles = {style}
            displayed = 1
            total = len(STYLES)

            st.write("Generating other styles...")

            for other_style in STYLES:
                if other_style not in displayed_styles:
                    try:
                        res = requests.post(f"http://backend:8080/{STYLES[other_style]}", files=files)
                        res.raise_for_status()
                        img_path = res.json()
                        image = Image.open(img_path.get("name"))
                        st.image(image, caption=f"Styled with {other_style}", use_column_width=True)
                        time.sleep(1)
                        displayed += 1
                        displayed_styles.add(other_style)
                    except requests.RequestException as e:
                        st.error(f"Error with style {other_style}: {e}")
        except requests.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please upload an image and select a style.")
