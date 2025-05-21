import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fırın Alaşım Hesaplayıcı", layout="centered")
st.title("🔥 Fırın Alaşım Hesaplayıcı (V2) – Gerçek Zamanlı Ölçüm")

# Kullanıcıdan toplam fırın yükünü al
furnace_mass = st.number_input("Toplam Fırın Yükü (kg)", min_value=100.0, step=100.0)

st.markdown("---")
st.subheader("🎯 Hedef Element Bileşimleri (%)")

# Giriş tablosu
@st.cache_data
def get_input_table():
    return pd.DataFrame({
        "Element": ["Al", "Si", "Fe", "Mg", "Mn", "Cu", "Zn", "Ti", "Cr", "Ni"],
        "Min (%)": [88.0, 0.30, 0.15, 0.05, 0.1, 0.05, 0.01, 0.01, 0.01, 0.01],
        "Nominal (%)": [92.0, 0.35, 0.20, 0.08, 0.2, 0.10, 0.02, 0.02, 0.02, 0.02],
        "Max (%)": [99.5, 0.40, 0.25, 0.10, 0.3, 0.15, 0.05, 0.05, 0.05, 0.05]
    })

input_df = st.data_editor(get_input_table(), num_rows="dynamic", use_container_width=True)

st.markdown("---")
st.subheader("📡 Gerçek Zamanlı Ölçüm Değerleri (%)")

# Gerçek zamanlı ölçüm girişleri
measurement_input = {}
for element in input_df["Element"]:
    measurement_input[element] = st.number_input(f"{element} ölçüm (%)", min_value=0.0, format="%.4f")

if st.button("🔍 Hesapla"):
    result_df = input_df.copy()
    result_df["Ölçülen (%)"] = result_df["Element"].map(measurement_input)
    result_df["Hedef (kg)"] = (result_df["Nominal (%)"] / 100) * furnace_mass
    result_df["Min (kg)"] = (result_df["Min (%)"] / 100) * furnace_mass
    result_df["Max (kg)"] = (result_df["Max (%)"] / 100) * furnace_mass
    result_df["Ölçülen (kg)"] = (result_df["Ölçülen (%)"] / 100) * furnace_mass
    result_df["Fark (kg)"] = result_df["Hedef (kg)"] - result_df["Ölçülen (kg)"]
    result_df["Durum"] = result_df.apply(lambda row: "✅" if row["Min (%)"] <= row["Ölçülen (%)"] <= row["Max (%)"] else "⚠️ Dışında", axis=1)

    st.success("Hesaplama tamamlandı!")
    st.dataframe(result_df, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Grafik: Hedef vs Ölçülen (kg)")
    chart_df = result_df.set_index("Element")[["Hedef (kg)", "Ölçülen (kg)"]]
    st.bar_chart(chart_df)

    st.markdown("---")
    st.subheader("📌 Dışında Kalanlar ve Gerekli Eklemeler")
    outside_df = result_df[result_df["Durum"] == "⚠️ Dışında"][["Element", "Fark (kg)"]]
    if not outside_df.empty:
        st.warning("Bazı elementler hedef aralığın dışında:")
        st.dataframe(outside_df)
    else:
        st.info("Tüm elementler hedef aralıkta!")
