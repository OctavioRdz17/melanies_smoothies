# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title("My Parents New Healthy Dinner🥤")
st.write(
    """Choose the fruits you want on your Smoothie
    """
)
conn = st.connection("snowflake")
session = conn.session()

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be: '+name_on_order)



my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    time_to_insert = st.button('Submit Order')

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(fruityvice_response.json(),
                             use_container_width=True)
    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    

    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!  '+name_on_order+'.',icon="✅")
    
