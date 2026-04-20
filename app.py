import streamlit as st

st.set_page_config(page_title="Isolatie Calculator", page_icon="🏠", layout="centered")

st.title("🏠 Isolatie Calculator")
st.write("Bereken snel en eenvoudig een indicatieprijs voor de werkzaamheden.")

# Keuze soort isolatie
isolatie_type = st.selectbox(
    "Kies het type isolatie",
    ["Vloerisolatie", "Dakisolatie", "Plafondisolatie", "Spouwisolatie"]
)

# Algemene invoer
m2 = st.number_input("Aantal m²", min_value=0.0, step=1.0)

ruimtes = 0

# Logica per type
if isolatie_type == "Vloerisolatie":
    ruimtes = st.number_input("Aantal ruimtes", min_value=1, step=1)

elif isolatie_type == "Plafondisolatie":
    ruimtes = st.number_input("Aantal ruimtes", min_value=1, step=1)

# Basisprijzen per m² (pas deze aan naar jouw echte prijzen!)
prijzen_per_m2 = {
    "Vloerisolatie": 28.50,
    "Dakisolatie": 32.50,
    "Plafondisolatie": 27.50,
    "Spouwisolatie": 24.50
}

basis_prijs_per_m2 = prijzen_per_m2[isolatie_type]
totaal = m2 * basis_prijs_per_m2

# Toeslag per ruimte (alleen waar nodig)
if isolatie_type in ["Vloerisolatie", "Plafondisolatie"]:
    totaal += ruimtes * 15.00

st.markdown("---")
st.subheader("Extra werkzaamheden")

ventilatie = st.checkbox("Ventilatie boren incl rooster en pvc (+ €59,95)")
schoonmaken = st.checkbox("Kruipruimte schoonmaken met afvoer puin mogelijk (+ €199,95)")
all_in_check = st.checkbox("Kruipruimte all in check (+ €159,95)")

if ventilatie:
    totaal += 59.95

if schoonmaken:
    totaal += 199.95

if all_in_check:
    totaal += 159.95

st.markdown("---")
st.subheader("Prijsopbouw")

st.write(f"**Soort isolatie:** {isolatie_type}")
st.write(f"**Aantal m²:** {m2}")
st.write(f"**Prijs per m²:** € {basis_prijs_per_m2:.2f}")

if isolatie_type in ["Vloerisolatie", "Plafondisolatie"]:
    st.write(f"**Aantal ruimtes:** {ruimtes}")
    st.write(f"**Toeslag ruimtes:** € {ruimtes * 15.00:.2f}")

extras_totaal = 0
if ventilatie:
    extras_totaal += 59.95
if schoonmaken:
    extras_totaal += 199.95
if all_in_check:
    extras_totaal += 159.95

st.write(f"**Totaal extra werkzaamheden:** € {extras_totaal:.2f}")

st.markdown("---")
st.subheader("Totaalprijs")
st.success(f"Totale richtprijs: € {totaal:.2f}")

with st.expander("Uitleg: kruipruimte all in check"):
    st.write("""
Hierbij controleren we onder andere:

- de vochtigheid
- lekkages
- leidingen
- beugels
- staat van het beton
- staat van de bekabeling
- ventilatiegaten

Als iets niet meer in goede staat is, repareren we dat altijd in overleg.
""")
