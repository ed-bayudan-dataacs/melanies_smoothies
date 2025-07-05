# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title('My Parents New Healthy Diner')
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

title = st.text_input("Name on smoothie", "")
#st.write("The current movie title is", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5,
    accept_new_options=True
)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string+= fruit
        ingredients_string+= " "
        st.subheader(fruit + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +   fruit)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    save_smoothie = st.button('Submit smoothie order')

    if save_smoothie:
        #my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER) values ('""" + ingredients_string + """')"""
        my_insert_stmt = (
            f"INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER) "
            f"VALUES ('{ingredients_string}'"
            f", '{title}')"
        )
        
        #st.write("SQL is: ", my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success(f"Your smoothie is ordered, {title}!", icon="✅")
        

