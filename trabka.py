%%writefile streamlit_app.py
import streamlit as st

# Initialize inventory as a global list, not in session state, as requested.
# For a persistent app, consider st.session_state or a database.
inventory = []

# Application Title
st.title('Inventory Management System')

# Display current inventory
st.header('Current Inventory')
if inventory:
    for item in inventory:
        st.write(f"- {item}")
else:
    st.write("Inventory is empty.")

# Add new item section
st.header('Add New Item')
new_item = st.text_input('Item Name', key='add_item_input')
if st.button('Add Item'):
    if new_item:
        inventory.append(new_item)
        st.success(f"'{new_item}' added to inventory!")
        # Clearing the input field after adding (requires session state for persistence across rerun)
        # For this example without session state for inventory, the input field state will reset.
    else:
        st.error("Please enter an item name to add.")

# Remove item section
st.header('Remove Item')
if inventory:
    item_to_remove = st.selectbox('Select item to remove', inventory, key='remove_item_select')
    if st.button('Remove Selected Item'):
        if item_to_remove:
            if item_to_remove in inventory:
                inventory.remove(item_to_remove)
                st.success(f"'{item_to_remove}' removed from inventory!")
                # Rerunning the app to update display (Streamlit handles this on state change normally)
                # st.experimental_rerun() is often used, but here, the app naturally reruns on interaction.
            else:
                st.error(f"'{item_to_remove}' is not in the inventory.")
        else:
            st.error("Please select an item to remove.")
else:
    st.write("Inventory is empty, no items to remove.")
