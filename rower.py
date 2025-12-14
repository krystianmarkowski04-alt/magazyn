import streamlit as st
import csv
import pandas as pd
import plotly.express as px
import hashlib

# Funkcja do ładowania danych z pliku CSV
def load_inventory():
    try:
        with open("inventory.csv", mode="r") as file:
            reader = csv.DictReader(file)
            st.session_state.inventory = [dict(row) for row in reader]
    except FileNotFoundError:
        st.session_state.inventory = []

# Funkcja do zapisywania danych do pliku CSV
def save_inventory():
    with open("inventory.csv", mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["item", "quantity", "description"])
        writer.writeheader()
        for entry in st.session_state.inventory:
            writer.writerow(entry)

# Funkcja do dodawania towaru
def add_item():
    item = st.text_input("Nazwa towaru", "")
    quantity = st.number_input("Ilość", min_value=1, step=1)
    description = st.text_area("Opis towaru")
    if st.button("Dodaj towar"):
        if item != "":
            # Sprawdzenie, czy towar już istnieje
            if any(existing_item['item'] == item for existing_item in st.session_state.inventory):
                st.warning(f"Towar {item} już istnieje w magazynie!")
            else:
                st.session_state.inventory.append({"item": item, "quantity": quantity, "description": description})
                st.success(f"Towar {item} dodany!")
        else:
            st.error("Proszę podać nazwę towaru!")

# Funkcja do edytowania towaru
def edit_item():
    item_to_edit = st.selectbox("Wybierz towar do edycji", [x['item'] for x in st.session_state.inventory])
    if item_to_edit:
        new_quantity = st.number_input("Nowa ilość", min_value=1, step=1)
        new_description = st.text_area("Nowy opis", value="")
        if st.button("Zaktualizuj ilość i opis"):
            for entry in st.session_state.inventory:
                if entry['item'] == item_to_edit:
                    entry['quantity'] = new_quantity
                    entry['description'] = new_description
                    st.success(f"Ilość i opis towaru {item_to_edit} zaktualizowane!")
                    break

# Funkcja do usuwania towaru
def remove_item():
    item_to_remove = st.selectbox("Wybierz towar do usunięcia", [x['item'] for x in st.session_state.inventory])
    if st.button("Usuń towar"):
        st.session_state.inventory = [x for x in st.session_state.inventory if x['item'] != item_to_remove]
        st.success(f"Towar {item_to_remove} usunięty!")

# Funkcja do sortowania towarów
def sort_inventory():
    sort_option = st.radio("Sortuj po:", ("Nazwie", "Ilości"))
    if sort_option == "Nazwie":
        st.session_state.inventory.sort(key=lambda x: x['item'])
    elif sort_option == "Ilości":
        st.session_state.inventory.sort(key=lambda x: x['quantity'], reverse=True)

# Funkcja do filtrowania towarów
def filter_inventory():
    search_term = st.text_input("Szukaj towaru:")
    if search_term:
        filtered_inventory = [item for item in st.session_state.inventory if search_term.lower() in item['item'].lower()]
        if filtered_inventory:
            for entry in filtered_inventory:
                st.write(f"{entry['item']} - Ilość: {entry['quantity']}")
        else:
            st.write("Brak towarów spełniających kryteria wyszukiwania.")
    else:
        for entry in st.session_state.inventory:
            st.write(f"{entry['item']} - Ilość: {entry['quantity']}")

# Funkcja do wyświetlania wykresu stanu magazynowego
def plot_inventory():
    inventory_data = [{"item": entry['item'], "quantity": entry['quantity']} for entry in st.session_state.inventory]
    df = pd.DataFrame(inventory_data)
    fig = px.bar(df, x="item", y="quantity", title="Stan magazynowy")
    st.plotly_chart(fig)

# Funkcja do wyświetlania produktów o niskim stanie
def check_low_stock():
    threshold = 5
    low_stock_items = [entry for entry in st.session_state.inventory if entry['quantity'] < threshold]
    if low_stock_items:
        st.warning("Towary o niskim stanie:")
        for item in low_stock_items:
            st.write(f"{item['item']} - Ilość: {item['quantity']}")

# Funkcja do autentykacji użytkownika
def authenticate_user():
    password = st.text_input("Hasło:", type="password")
    if password and hashlib.md5(password.encode()).hexdigest() == 'd2d2d2d2d2d2d2d2d2d2':  # Wstaw odpowiednią wartość hasła
        st.session_state.authenticated = True
        st.success("Zalogowano pomyślnie!")
    elif password:
        st.error("Niepoprawne hasło!")

# Inicjalizacja
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Interfejs użytkownika
st.title("Prosty magazyn")

# Sekcja logowania
if not st.session_state.authenticated:
    authenticate_user()

# Po zalogowaniu pokazujemy resztę funkcji
if st.session_state.authenticated:
    load_inventory()

    # Opcje aplikacji
    option = st.sidebar.selectbox("Wybierz akcję", ["Dodaj towar", "Edytuj towar", "Usuń towar", "Sortuj towary", "Filtrowanie", "Stan magazynowy", "Zapisz stan", "Wykres"])

    if option == "Dodaj towar":
        add_item()
    elif option == "Edytuj towar":
        edit_item()
    elif option == "Usuń towar":
        remove_item()
    elif option == "Sortuj towary":
        sort_inventory()
    elif option == "Filtrowanie":
        filter_inventory()
    elif option == "Stan magazynowy":
        for entry in st.session_state.inventory:
            st.write(f"{entry['item']} - Ilość: {entry['quantity']} - Opis: {entry.get('description', 'Brak opisu')}")
        check_low_stock()
    elif option == "Wykres":
        plot_inventory()

    # Zapisz stan magazynu
    if st.button("Zapisz stan magazynu"):
        save_inventory()
        st.success("Stan magazynu zapisany do pliku!")
