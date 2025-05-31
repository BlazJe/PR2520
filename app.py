import streamlit as st
import plotly.express as px
from funkcije import load_data, stack_data

@st.cache_data
def load_combined_data():
    return load_data()

@st.cache_data
def get_stacked_data(df, group_col, n):
    return stack_data(df, group_col).head(n)

st.write("# Analiza prometnih nesreč")
combined_data = load_combined_data()
filtered_2023 = combined_data[combined_data['DatumPN'].str.endswith('.2023')]

st.write("## Podatki o prometnih nesrečah")
st.write("Uporabljeni podatki pri tej analizi izgledajo takole:")

query_str = st.text_input(
    "Vpiši pogoj za filtriranje (npr. UpravnaEnotaStoritve == 'LITIJA' and Starost > 30):"
)

if query_str:
    try:
        filtered = filtered_2023.query(query_str)
        st.dataframe(filtered)
        st.success(f"Prikazanih {len(filtered)} vrstic.")
    except Exception as e:
        st.error(f"Napaka v poizvedbi: {e}")
else:
    filtered_2023 = combined_data[combined_data['DatumPN'].str.endswith('.2023')]
    st.dataframe(filtered_2023)
    st.info(f"Privzeto prikazujem samo podatke za leto 2023 ({len(filtered_2023)} vrstic).")

classification_colors = {
    'Z MATERIALNO ŠKODO': '#377eb8',  
    'Z LAŽJO TELESNO POŠKODBO': '#4daf4a', 
    'S HUDO TELESNO POŠKODBO': '#ff7f00',  
    'S SMRTNIM IZIDOM': '#e41a1c'  
}

group_options = {
    "UpravnaEnotaStoritve": "Upravna enota",
    "VzrokNesrece": "Vzrok nesreče",
    "VrstaUdelezenca": "Vrsta udeleženca",
    "VNaselju": "V naselju",
    "VrstaCesteNaselja": "Vrsta ceste",
    "OpisKraja": "Opis kraja",
    "TipNesrece": "Tip nesreče",
    "VremenskeOkoliscine": "Vremenske okoliščine",
    "StanjePrometa": "Stanje prometa",
    "StanjeVozisca": "Stanje vozišča",
    "VrstaVozisca": "Vrsta vozišča"
}

st.write("## Prikaz števila nesreč po klasifikaciji")

selected_label = st.selectbox("Izberi kategorijo za prikaz:", list(group_options.values()))
group_col = [k for k, v in group_options.items() if v == selected_label][0]
top_n = st.slider("Število kategorij za prikaz:", 5, 50, 10)

stacked_data = get_stacked_data(combined_data, group_col, top_n)
stacked_long = stacked_data.reset_index().melt(
    id_vars=group_col,
    var_name="Klasifikacija",
    value_name="Število nesreč"
)

fig = px.bar(
    stacked_long,
    x="Število nesreč",
    y=group_col,
    color="Klasifikacija",
    orientation="h",
    color_discrete_map=classification_colors,
    title=f"Število nesreč po kategoriji: {selected_label}"
)

st.plotly_chart(fig, use_container_width=True)