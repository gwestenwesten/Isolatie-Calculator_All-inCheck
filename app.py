import streamlit as st
import smtplib
from email.message import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# -------------------------------------------------
# PAGINA INSTELLINGEN
# -------------------------------------------------
st.set_page_config(
    page_title="Isolatie Calculator",
    page_icon="🏠",
    layout="centered"
)


# -------------------------------------------------
# PDF MAKEN
# -------------------------------------------------
def maak_pdf(naam, telefoon, email, adres, beschrijving, isolatie_type, m2, ruimtes, prijs):
    file_name = "offerte.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Offerte Isolatiewerkzaamheden")

    c.setFont("Helvetica", 11)
    c.drawString(50, 720, f"Naam: {naam}")
    c.drawString(50, 700, f"Telefoon: {telefoon}")
    c.drawString(50, 680, f"E-mail: {email}")
    c.drawString(50, 660, f"Adres: {adres}")
    c.drawString(50, 640, f"Soort isolatie: {isolatie_type}")
    c.drawString(50, 620, f"Aantal m²: {m2}")

    if isolatie_type in ["Vloerisolatie", "Plafondisolatie"]:
        c.drawString(50, 600, f"Aantal ruimtes: {ruimtes}")
        y_beschrijving = 560
    else:
        y_beschrijving = 580

    c.drawString(50, y_beschrijving, "Beschrijving:")
    c.drawString(50, y_beschrijving - 20, f"{beschrijving}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_beschrijving - 60, f"Totaalprijs: € {prijs:.2f}")

    c.save()
    return file_name


# -------------------------------------------------
# MAIL NAAR JOU
# -------------------------------------------------
def stuur_mail_naar_jou(
    naam,
    telefoon,
    klant_email,
    adres,
    beschrijving,
    isolatie_type,
    m2,
    ruimtes,
    ventilatie,
    schoonmaken,
    all_in_check,
    pdf_bestand,
    totaal
):
    EMAIL = "g.westenanders@gmail.com"
    WACHTWOORD = "HIER_JOUW_APP_WACHTWOORD"

    msg = EmailMessage()
    msg["Subject"] = f"Nieuwe offerte aanvraag van {naam}"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    msg.set_content(f"""
Nieuwe aanvraag ontvangen:

Naam: {naam}
Telefoon: {telefoon}
E-mail klant: {klant_email}
Adres: {adres}

Aanvraag:
Soort isolatie: {isolatie_type}
Aantal m²: {m2}
Aantal ruimtes: {ruimtes if isolatie_type in ["Vloerisolatie", "Plafondisolatie"] else "n.v.t."}

Extra werkzaamheden:
Ventilatie boren incl rooster en pvc: {"Ja" if ventilatie else "Nee"}
Kruipruimte schoonmaken met afvoer puin: {"Ja" if schoonmaken else "Nee"}
Kruipruimte all in check: {"Ja" if all_in_check else "Nee"}

Beschrijving:
{beschrijving if beschrijving else "Geen beschrijving ingevuld"}

Indicatieprijs: € {totaal:.2f}
""")

    with open(pdf_bestand, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="offerte.pdf"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, WACHTWOORD)
        smtp.send_message(msg)


# -------------------------------------------------
# MAIL NAAR KLANT
# -------------------------------------------------
def stuur_mail_naar_klant(klant_email, naam, pdf_bestand):
    EMAIL = "g.westenanders@gmail.com"
    WACHTWOORD = "HIER_JOUW_APP_WACHTWOORD"

    msg = EmailMessage()
    msg["Subject"] = "Uw offerteaanvraag"
    msg["From"] = EMAIL
    msg["To"] = klant_email

    msg.set_content(f"""
Beste {naam},

Bedankt voor uw aanvraag.

In de bijlage vindt u de PDF met de gegevens van uw aanvraag.
Wij nemen zo snel mogelijk contact met u op.

Met vriendelijke groet,
Isolatie Calculator
""")

    with open(pdf_bestand, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="offerte.pdf"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, WACHTWOORD)
        smtp.send_message(msg)


# -------------------------------------------------
# WEBSITE BOVENKANT
# -------------------------------------------------
st.title("🏠 Isolatie Calculator")
st.write("Bereken snel en eenvoudig een indicatieprijs voor isolatiewerkzaamheden.")

st.markdown("## Onze diensten")

col1, col2 = st.columns(2)

with col1:
    st.info("""
**Vloerisolatie**
- Meer comfort in huis
- Minder kou vanuit de vloer
- Lagere energiekosten
""")

with col2:
    st.info("""
**Kruipruimte werkzaamheden**
- Ventilatie verbeteren
- Kruipruimte inspecteren
- Schoonmaken en puin afvoeren
""")

st.markdown("---")


# -------------------------------------------------
# CALCULATOR
# -------------------------------------------------
st.header("🧮 Calculator")

isolatie_type = st.selectbox(
    "Kies het type isolatie",
    ["Vloerisolatie", "Dakisolatie", "Plafondisolatie", "Spouwisolatie"]
)

m2 = st.number_input("Aantal m²", min_value=0.0, step=1.0)

ruimtes = 0
if isolatie_type in ["Vloerisolatie", "Plafondisolatie"]:
    ruimtes = st.number_input("Aantal ruimtes", min_value=1, step=1)

prijzen_per_m2 = {
    "Vloerisolatie": 28.50,
    "Dakisolatie": 32.50,
    "Plafondisolatie": 27.50,
    "Spouwisolatie": 24.50
}

basis_prijs = prijzen_per_m2[isolatie_type]
totaal = m2 * basis_prijs

if isolatie_type in ["Vloerisolatie", "Plafondisolatie"]:
    totaal += ruimtes * 15.00

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
st.subheader("Totaalprijs")
st.success(f"Totale indicatieprijs: € {totaal:.2f}")

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

st.markdown("---")


# -------------------------------------------------
# OFFERTE FORMULIER
# -------------------------------------------------
st.header("📞 Offerte aanvragen")

naam = st.text_input("Naam")
telefoon = st.text_input("Telefoonnummer")
email = st.text_input("E-mailadres")
adres = st.text_input("Adres")
beschrijving = st.text_area("Beschrijving van de situatie")

st.info("📅 Wij nemen binnen 24 uur contact met je op.")

if st.button("Vraag offerte aan"):
    if naam and telefoon and email and adres:
        try:
            pdf = maak_pdf(
                naam,
                telefoon,
                email,
                adres,
                beschrijving,
                isolatie_type,
                m2,
                ruimtes,
                totaal
            )

            stuur_mail_naar_jou(
                naam,
                telefoon,
                email,
                adres,
                beschrijving,
                isolatie_type,
                m2,
                ruimtes,
                ventilatie,
                schoonmaken,
                all_in_check,
                pdf,
                totaal
            )

            stuur_mail_naar_klant(email, naam, pdf)

            st.success("Offerte verzonden! Jij krijgt een mail en de klant ontvangt automatisch de PDF 📧")
        except Exception as e:
            st.error(f"Er ging iets mis bij het versturen: {e}")
    else:
        st.error("Vul alle velden in.")
