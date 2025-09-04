import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("🍓 Customize Your Smoothie! 🥭")

st.write("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Get session and fruits table
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").to_pandas()

# Multi-select (show fruit names)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe["FRUIT_NAME"].tolist()   # ensure values are strings
)

# Custom validation: limit to 5 ingredients
if len(ingredients_list) > 5:
    st.warning("⚠️ You can only select up to 5 ingredients. Please remove one.")
    ingredients_list = ingredients_list[:5]  # enforce the limit

# Convert list into a string for insertion
if ingredients_list:
    ingredients_string = " ".join(str(item) for item in ingredients_list)

    # Create SQL insert statement
    my_insert_stmt = f"""
        insert into smoothies.public.orders (ORDER_NAME, INGREDIENTS)
        values ('{name_on_order}', '{ingredients_string}')
    """

    # Submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("✅ Your Smoothie has been added to the database!")
