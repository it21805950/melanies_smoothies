# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# App title
st.title("🥤 Customize your smoothie 🥤")
st.write("Choose the fruits you want in your Smoothie!")

# Get user input
name_on_order = st.text_input("Name on smoothie:")
st.write("Name on your smoothie will be:", name_on_order)

# Get session and fruit options
cnx = st.connection("snowflake")
session = cnx_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Extract fruit names as a list for multiselect
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect with ingredient choices
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list
)

# Check for selection limit
if len(ingredients_list) > 5:
    st.warning("⚠️ You can only select up to 5 options. Please remove one.")
    st.stop()

# If valid selections made
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
 # SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Show button and handle click
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

