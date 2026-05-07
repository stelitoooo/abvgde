import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Списък с вредни съставки
harmful_ingredients = {
    "E621": "Мононатриев глутамат – може да предизвика главоболие",
    "E250": "Натриев нитрит – използва се в колбаси",
    "E951": "Аспартам – изкуствен подсладител",
    "палмово масло": "Съдържа наситени мазнини",
    "palm oil": "Contains saturated fats",
    "E102": "Тартразин – изкуствен оцветител",
    "E211": "Натриев бензоат – консервант"
}

# Заглавие
st.title("🍔 AI Food Label Scanner")
st.write("Качи снимка на етикет и приложението ще открие вредни съставки.")

# Качване на снимка
uploaded_file = st.file_uploader("Качи изображение", type=["jpg", "jpeg", "png"])

# Снимка от камера
camera_image = st.camera_input("Или направи снимка")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif camera_image is not None:
    image = Image.open(camera_image)

if image is not None:
    st.image(image, caption="Качено изображение", use_column_width=True)

    # OCR
    reader = easyocr.Reader(['bg', 'en'])

    img_array = np.array(image)

    with st.spinner("Разпознаване на текст..."):
        results = reader.readtext(img_array, detail=0)

    extracted_text = " ".join(results)

    st.subheader("📄 Разпознат текст")
    st.write(extracted_text)

    # Проверка за вредни съставки
    found = []

    for ingredient in harmful_ingredients:
        if ingredient.lower() in extracted_text.lower():
            found.append((ingredient, harmful_ingredients[ingredient]))

    st.subheader("⚠️ Открити вредни съставки")

    if found:
        for ingredient, description in found:
            st.error(f"{ingredient} → {description}")
    else:
        st.success("Не са открити вредни съставки.")
