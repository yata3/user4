import streamlit as st 
from PIL import Image
from PIL.ExifTags import TAGS


def modify_exif(image, new_metadata):
    exif_data = image.info["exif"]

    for tag, value in new_metadata.items():
        exif_tag = TAGS.get(tag, tag)
        exif_data[tag] = value

    exif_bytes = b""
    for tag, value in exif_data.items():
        if isinstance(value, str):
            value = bytes(value, "utf-8")
        exif_bytes += piexif.dump({exif_tag: value})

    image.save("mnemosyne.jpg", exif=exif_bytes)


uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="Image originale", use_column_width=True)

    exif_data = image._getexif()

    if exif_data is not None:
        existing_metadata = {}
        for tag, value in exif_data.items():
            exif_tag = TAGS.get(tag, tag)
            existing_metadata[exif_tag] = value

        st.header("Éditer les métadonnées EXIF")
        new_metadata = {}
        for exif_tag, value in existing_metadata.items():
            new_value = st.text_input(exif_tag, value)
            new_metadata[exif_tag] = new_value

        if st.button("Modifier les métadonnées"):
            mnemosyne = image.copy()
            modify_exif(mnemosyne, new_metadata)
            st.success("Les métadonnées EXIF ont été modifiées avec succès.")

            st.image(mnemosyne, caption="Image modifiée", use_column_width=True)
    else:
        st.warning("Cette image ne contient pas de métadonnées EXIF.")
else:
    st.warning("Veuillez télécharger une image.")