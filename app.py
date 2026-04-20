import streamlit as st

st.title("Isolatie Calculator")

m2 = st.number_input("Aantal m²", 0)
kamers = st.number_input("Aantal ruimtes", 1)

kruipruimte = st.checkbox("Kruipruimte isoleren")
ventilatie = st.checkbox("Ventilatie boren")
schoonmaken = st.checkbox("Kruipruimte schoonmaken")

prijs_per_m2 = 25
totaal = m2 * prijs_per_m2

if kruipruimte:
    totaal += 500
if ventilatie:
    totaal += 150
if schoonmaken:
    totaal += 200

st.subheader("Totale prijs:")
st.write(f"€ {totaal}")
