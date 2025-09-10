# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Text input to get the smoothie name from user
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the current Snowflake session
session = get_active_session()

# Load only the fruit names from the database
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Add a multiselect dropdown for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Continue only if ingredients are selected
if ingredients_list:
    # Convert list of ingredients to a single string separated by spaces
    ingredients_string = ' '.join(ingredients_list)

    # Escape single quotes in strings for basic SQL injection safety
    safe_name = name_on_order.replace("'", "''")
    safe_ingredients = ingredients_string.replace("'", "''")

    # Create SQL insert statement with both columns specified
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(name_on_order, ingredients)
        VALUES ('{safe_name}', '{safe_ingredients}')
    """

    # Create the submit button
    time_to_insert = st.button('Submit Order')

    # When button clicked, execute the insert statement and show success
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
