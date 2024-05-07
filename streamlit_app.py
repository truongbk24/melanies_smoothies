# Import python packages
import streamlit as st
import requests
import pandas
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        if not search_on:
            search_on = "test"
            st.write('The search value for ', fruit_chosen,' is ', pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'FRUIT_NAME'].iloc[0], '.')
        else
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+ ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    
    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients,name_on_order)
                    values ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered')
        
