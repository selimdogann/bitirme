import streamlit as st

st.set_page_config(page_title="Türkçe İlaç Asistanı", page_icon="💊")

st.title("Türkçe İlaç Asistanı")
st.caption(
    "Cevaplar resmî kullanma talimatlarından alınır. "
    "Tıbbi tavsiye değildir; doktorunuza veya eczacınıza danışın."
)

soru = st.text_input("İlacınızla ilgili sorunuzu yazın:")
if soru:
    st.write("Sorunuz:", soru)
