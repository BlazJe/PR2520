import streamlit as st
import plotly.express as px
from funkcije import load_data, stack_data, get_monthly_stacked, get_weekday_stacked, get_holiday_stacked
import calendar
import import_ipynb
import predictions  

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
    "OpisKraja": "Opis kraja",
    "StanjePrometa": "Stanje prometa",
    "StanjeVozisca": "Stanje vozišča",
    "TipNesrece": "Tip nesreče",
    "UporabaVarnostnegaPasu": "Uporaba varnostnega pasu",
    "UpravnaEnotaStoritve": "Upravna enota",
    "VNaselju": "V naselju",
    "VremenskeOkoliscine": "Vremenske okoliščine",
    "VrstaCesteNaselja": "Vrsta ceste",
    "VrstaUdelezenca": "Vrsta udeleženca",
    "VrstaVozisca": "Vrsta vozišča",
    "VzrokNesrece": "Vzrok nesreče"
}

st.write("## Prikaz števila nesreč po klasifikaciji")

selected_label = st.selectbox("Izberi kategorijo za prikaz:", list(group_options.values()))
group_col = [k for k, v in group_options.items() if v == selected_label][0]
top_n = st.slider("Število kategorij za prikaz:", 5, 30, 5)

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

st.write("## Prikaz razmerij med kalsfikacijami nesreč")

selected_ratio_label = st.selectbox(
    "Izberi kategorijo za prikaz razmerij:",
    list(group_options.values()),
    key="ratio_select"
)
ratio_group_col = [k for k, v in group_options.items() if v == selected_ratio_label][0]
top_n_ratio = st.slider("Število kategorij za prikaz:", 5, 30, 5, key="ratio_slider")

unique_accidents = combined_data.groupby('ZaporednaStevilkaPN').first()

filtered_ratio = unique_accidents[unique_accidents[ratio_group_col].notnull()]
injury_counts_ratio = filtered_ratio.pivot_table(
    index=ratio_group_col,
    columns='KlasifikacijaNesrece',
    aggfunc='size',
    fill_value=0
)

injury_ratios_ratio = injury_counts_ratio.div(injury_counts_ratio.sum(axis=1), axis=0).reset_index()

sort_cols = [
    'S SMRTNIM IZIDOM',
    'S HUDO TELESNO POŠKODBO',
    'Z LAŽJO TELESNO POŠKODBO'
]
for col in sort_cols:
    if col not in injury_ratios_ratio.columns:
        injury_ratios_ratio[col] = 0

injury_ratios_ratio = injury_ratios_ratio.sort_values(
    by=sort_cols,
    ascending=[False, False, False]
).head(top_n_ratio)

injury_long_ratio = injury_ratios_ratio.melt(
    id_vars=ratio_group_col,
    var_name='Klasifikacija',
    value_name='Razmerje'
)

order_klas = [
    'S SMRTNIM IZIDOM',
    'S HUDO TELESNO POŠKODBO',
    'Z LAŽJO TELESNO POŠKODBO',
    'Z MATERIALNO ŠKODO'
]

fig_ratio = px.bar(
    injury_long_ratio,
    x='Razmerje',
    y=ratio_group_col,
    color='Klasifikacija',
    orientation='h',
    color_discrete_map=classification_colors,
    title=f'Razmerje med poškodbami po kategoriji: {selected_ratio_label}',
    barmode='stack',
    category_orders={'Klasifikacija': order_klas}
)
fig_ratio.update_layout(xaxis_tickformat='.0%', legend_title_text='Klasifikacija nesreč')

st.plotly_chart(fig_ratio, use_container_width=True)

st.write("## Časovna analiza nesreč")

tab1, tab2, tab3 = st.tabs(["Po mesecih", "Po dnevih v tednu", "Prazniki"])

with tab1:
    stacked_month = get_monthly_stacked(combined_data)
    stacked_month.index = [
        calendar.month_abbr[i] for i in range(1, 13)
    ]  
    stacked_month_long = stacked_month.reset_index().melt(
        id_vars='index',
        var_name='Klasifikacija',
        value_name='Povprečno na dan'
    ).rename(columns={'index': 'Mesec'})
    fig_month = px.bar(
        stacked_month_long,
        x='Mesec',
        y='Povprečno na dan',
        color='Klasifikacija',
        barmode='stack',
        color_discrete_map=classification_colors,
        category_orders={'Mesec': [calendar.month_abbr[i] for i in range(1, 13)]}
    )
    fig_month.update_layout(title='Nesreče povprečno po mesecih', xaxis_title='Mesec', yaxis_title='Povprečno število nesreč na dan')
    st.plotly_chart(fig_month, use_container_width=True)

with tab2:
    stacked_weekday = get_weekday_stacked(combined_data)
    order_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    order_si = ['Ponedeljek', 'Torek', 'Sreda', 'Četrtek', 'Petek', 'Sobota', 'Nedelja']
    if list(stacked_weekday.index) == order_en:
        stacked_weekday.index = order_si
    else:
        stacked_weekday = stacked_weekday.reindex(order_si)
    stacked_weekday_long = stacked_weekday.reset_index().melt(
        id_vars='index',
        var_name='Klasifikacija',
        value_name='Povprečno na dan'
    ).rename(columns={'index': 'Dan'})
    fig_weekday = px.bar(
        stacked_weekday_long,
        x='Dan',
        y='Povprečno na dan',
        color='Klasifikacija',
        barmode='stack',
        color_discrete_map=classification_colors,
        category_orders={'Dan': order_si}
    )
    fig_weekday.update_layout(title='Nesreče povprečno na dan v tednu', xaxis_title='Dan v tednu', yaxis_title='Povprečno število nesreč na dan')
    st.plotly_chart(fig_weekday, use_container_width=True)

with tab3:
    stacked_holiday = get_holiday_stacked(combined_data)
    num_holidays = len(stacked_holiday)
    top_n_holidays = st.slider(
        "Število prikazanih praznikov:", 
        min_value=5, 
        max_value=num_holidays, 
        value=num_holidays
    )
    stacked_holiday = stacked_holiday.head(top_n_holidays)
    stacked_holiday_long = stacked_holiday.reset_index().melt(
        id_vars='Holiday',
        var_name='Klasifikacija',
        value_name='Povprečno na dan'
    )
    holiday_order = stacked_holiday.index.tolist()
    fig_holiday = px.bar(
        stacked_holiday_long,
        y='Holiday',
        x='Povprečno na dan',
        color='Klasifikacija',
        orientation='h',
        barmode='stack',
        color_discrete_map=classification_colors,
        category_orders={'Holiday': holiday_order}
    )
    fig_holiday.update_layout(
        title='Nesreče povprečno na praznik na dan',
        xaxis_title='Povprečno število nesreč na dan',
        yaxis_title='Praznik'
    )
    st.plotly_chart(fig_holiday, use_container_width=True)

st.write("## Napovedovalni model")

allowedColumns = [
    'KlasifikacijaNesrece', 'UpravnaEnotaStoritve', 'UraPN', 'VNaselju',
    'Lokacija', 'VrstaCesteNaselja', 'SifraCesteNaselja',
    'TekstCesteNaselja', 'SifraOdsekaUlice', 'TekstOdsekaUlice',
    'StacionazaDogodka', 'OpisKraja', 'VzrokNesrece', 'TipNesrece',
    'VremenskeOkoliscine', 'StanjePrometa', 'StanjeVozisca', 'VrstaVozisca',
    'GeoKoordinataX', 'GeoKoordinataY', 'Povzrocitelj', 'Starost', 'Spol',
    'UEStalnegaPrebivalisca', 'Drzavljanstvo', 'PoskodbaUdelezenca',
    'VrstaUdelezenca', 'UporabaVarnostnegaPasu', 'VozniskiStazVLetih',
    'VrednostAlkotesta', 'VrednostStrokovnegaPregleda'
]
computeHeavyModels = [
    'SifraCesteNaselja', 'TekstCesteNaselja', 'SifraOdsekaUlice', 'TekstOdsekaUlice', 'StacionazaDogodka'
]

model_options = [col for col in allowedColumns if col not in computeHeavyModels]
modelName = st.selectbox("Kaj želiš napovedovati?", model_options)

st.write("Vnesi vrednosti za ostale atribute (če ne veš, pusti -1):")

selectbox_fields = [
    'KlasifikacijaNesrece',
    'UpravnaEnotaStoritve',
    'VNaselju',
    'VrstaCesteNaselja',
    'TekstCesteNaselja',
    'VzrokNesrece',
    'TipNesrece',
    'VremenskeOkoliscine',
    'StanjePrometa',
    'StanjeVozisca',
    'VrstaVozisca',
    'Povzrocitelj',
    'Spol',
    'UEStalnegaPrebivalisca',
    'Drzavljanstvo',
    'PoskodbaUdelezenca',
    'VrstaUdelezenca',
    'UporabaVarnostnegaPasu',
    'OpisKraja',
    'Lokacija'
]

def get_unique_values(col, data):
    vals = data[col].dropna().unique()
    vals = [str(v) for v in vals if str(v).strip() != "" and str(v).strip() != "-1"]
    return sorted(list(set(vals)))

with st.form("prediction_form"):
    predictionData = {}
    for col in allowedColumns:
        if col == modelName:
            continue
        if col in selectbox_fields and col in combined_data.columns:
            options = get_unique_values(col, combined_data)
            options = ["-1"] + options
            predictionData[col] = st.selectbox(col, options, index=0)
        else:
            predictionData[col] = st.text_input(col, value="-1")
    submit = st.form_submit_button("Napovej")

if submit:
    try:
        result = predictions.predictValue(modelName, predictionData, "models_naiveBayas/")
        st.success(f"Napovedana vrednost za **{modelName}**: {result}")
    except Exception as e:
        st.error(f"Napaka pri napovedi: {e}")