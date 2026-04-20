import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Isolatie Calculator",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Isolatie Calculator")
st.caption("Professionele prijsindicatie voor isolatiewerkzaamheden")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    klantnaam = st.text_input("Klantnaam")
    projectdatum = st.date_input("Datum", value=date.today())

with col2:
    plaats = st.text_input("Plaats")
    compartimenten = st.number_input("Aantal compartimenten", min_value=1, step=1)

st.subheader("Werkgegevens")

isolatie_type = st.selectbox(
    "Type isolatie",
    [
        "Vloerisolatie",
        "Bodemisolatie",
        "Spouwmuurisolatie",
        "Dakisolatie"
    ]
)

m2 = st.number_input("Aantal m²", min_value=0.0, step=1.0)
ruimtes = st.number_input("Aantal ruimtes", min_value=1, step=1)

st.subheader("Extra werkzaamheden")

col3, col4 = st.columns(2)

with col3:
    kruipruimte = st.checkbox("Kruipruimte isoleren")
    ventilatie = st.checkbox("Ventilatie boren")
    schoonmaken = st.checkbox("Kruipruimte schoonmaken")

with col4:
    plafondisolatie = st.checkbox("Plafondisolatie")
    spouwisolatie = st.checkbox("Spouwisolatie")
    all_in_check = st.checkbox("Kruipruimte all-in check")

if isolatie_type == "Vloerisolatie":
    prijs_per_m2 = 25
elif isolatie_type == "Bodemisolatie":
    prijs_per_m2 = 18
elif isolatie_type == "Spouwmuurisolatie":
    prijs_per_m2 = 20
else:
    prijs_per_m2 = 30

basisprijs = m2 * prijs_per_m2
extra_kosten = 0

if kruipruimte:
    extra_kosten += 500
if ventilatie:
    extra_kosten += 150
if schoonmaken:
    extra_kosten += 200
if plafondisolatie:
    extra_kosten += 300
if spouwisolatie:
    extra_kosten += 350
if all_in_check:
    extra_kosten += 125

extra_kosten += compartimenten * 50

totaal = basisprijs + extra_kosten

st.markdown("---")
st.subheader("Kostenoverzicht")

st.write(f"**Klantnaam:** {klantnaam if klantnaam else '-'}")
st.write(f"**Plaats:** {plaats if plaats else '-'}")
st.write(f"**Datum:** {projectdatum}")
st.write(f"**Type isolatie:** {isolatie_type}")
st.write(f"**Aantal m²:** {m2}")
st.write(f"**Aantal ruimtes:** {ruimtes}")
st.write(f"**Aantal compartimenten:** {compartimenten}")

st.info(f"Basisprijs: EUR {basisprijs:,.2f}")
st.info(f"Extra werkzaamheden: EUR {extra_kosten:,.2f}")
st.success(f"Totaalprijs: EUR {totaal:,.2f}")

st.markdown("---")
st.caption("Let op: dit is een prijsindicatie. Definitieve prijs kan afwijken op basis van opname en situatie op locatie.")
