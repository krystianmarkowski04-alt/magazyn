import streamlit as st

# Inicjalizacja listy magazynowej
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# Funkcja do dodawania towaru
def add_item():
    item = st.text_input("Nazwa towaru", "")
    quantity = st.number_input("Ilość", min_value=1, step=1)
    if st.button("Dodaj towar"):
        if item != "":
            st.session_state.inventory.append({"item": item, "quantity": quantity})
            st.success(f"Towar {item} dodany!")
        else:
            st.error("Proszę podać nazwę towaru!")

# Funkcja do usuwania towaru
def remove_item():
    item_to_remove = st.selectbox("Wybierz towar do usunięcia", [x['item'] for x in st.session_state.inventory])
    if st.button("Usuń towar"):
        st.session_state.inventory = [x for x in st.session_state.inventory if x['item'] != item_to_remove]
        st.success(f"Towar {item_to_remove} usunięty!")

# Wyświetlanie obecnego stanu magazynu
def show_inventory():
    if st.session_state.inventory:
        st.write("Aktualny stan magazynowy:")
        for idx, entry in enumerate(st.session_state.inventory):
            st.write(f"{entry['item']} - Ilość: {entry['quantity']}")
    else:
        st.write("Magazyn jest pusty.")

# Interfejs użytkownika
st.title("Prosty magazyn")

add_item()
remove_item()
show_inventory()
