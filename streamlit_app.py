# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)
pd_df = my_dataframe.to_pandas()

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients (IN ORDER)",
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# Checkbox for Order Filled
order_filled = st.checkbox("Mark order as FILLED")

# If ingredients are selected
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # comma-separated in order

    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f"The search value for {fruit_chosen} is {search_on}.")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    st.write("Ingredients string:", ingredients_string)

    # Build insert SQL
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
        VALUES ('{ingredients_string}', '{name_on_order}', {str(order_filled).upper()})
    """

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")


    if time_to_insert:
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
