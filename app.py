import streamlit as st
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="Isolatie Calculator",
    page_icon="🏠",
    layout="centered"
)

# PDF functie
def maak_pdf(klantnaam, plaats, projectdatum, isolatie_type, m2, ruimtes, compartimenten,
             basisprijs, extra_kosten, totaal):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    breedte, hoogte = A4

    y = hoogte - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Offerte - Isolatie Calculator")

    y -= 35
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Klantnaam: {klantnaam if klantnaam else '-'}")
    y -= 20
    pdf.drawString(50, y, f"Plaats: {plaats if plaats else '-'}")
    y -= 20
    pdf.drawString(50, y, f"Datum: {projectdatum}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Projectgegevens")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Type isolatie: {isolatie_type}")
    y -= 20
    pdf.drawString(50, y, f"Aantal m²: {m2}")
    y -= 20
    pdf.drawString(50, y, f"Aantal ruimtes: {ruimtes}")
    y -= 20
    pdf.drawString(50, y, f"Aantal compartimenten: {compartimenten}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Kostenoverzicht")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Basisprijs: € {basisprijs:,.2f}")
    y -= 20
    pdf.drawString(50, y, f"Extra kosten: € {extra_kosten:,.2f}")
    y -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Totaalprijs: € {totaal:,.2f}")
    y -= 40

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(50, y, "Let op: dit is een indicatieve offerte. Definitieve prijs kan afwijken na opname op locatie.")

    pdf.save()
    buffer.seek(0)
    return buffer


st.title("🏠 Isolatie Calculator")
st.caption("Professionele prijsindicatie voor isolatiewerkzaamheden")

st.sidebar.title("Instellingen")
st.sidebar.info("Vul alle projectgegevens in voor een duidelijke prijsindicatie en PDF-offerte.")

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

# Basisprijzen
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
st.subheader("📄 Offerte overzicht")

col5, col6 = st.columns(2)

with col5:
    st.write("**Klant:**", klantnaam if klantnaam else "-")
    st.write("**Plaats:**", plaats if plaats else "-")
    st.write("**Datum:**", projectdatum)

with col6:
    st.write("**Type isolatie:**", isolatie_type)
    st.write("**m²:**", m2)
    st.write("**Ruimtes:**", ruimtes)

st.markdown("---")
st.write("### 💰 Kosten")
st.write(f"Prijs per m²: € {prijs_per_m2}")
st.write(f"Basisprijs: € {basisprijs:,.2f}")
st.write(f"Extra kosten: € {extra_kosten:,.2f}")
st.success(f"**Totaalprijs: € {totaal:,.2f}**")

pdf_bestand = maak_pdf(
    klantnaam,
    plaats,
    projectdatum,
    isolatie_type,
    m2,
    ruimtes,
    compartimenten,
    basisprijs,
    extra_kosten,
    totaal
)

st.download_button(
    label="📥 Download offerte als PDF",
    data=pdf_bestand,
    file_name="offerte_isolatie.pdf",
    mime="application/pdf"
)

st.markdown("---")
st.caption("Let op: dit is een indicatie. Definitieve prijs kan afwijken op basis van opname en situatie op locatie.")
