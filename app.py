import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fırın Alaşım Hesaplayıcı", layout="centered")
st.title("🔥 Fırın Alaşım Hesaplayıcı (V1)")

# Kullanıcıdan toplam fırın yükünü al
furnace_mass = st.number_input("Toplam Fırın Yükü (kg)", min_value=100.0, step=100.0)

st.markdown("---")
st.subheader("🎯 Hedef Element Bileşimleri (%)")

# Giriş tablosu için boş DataFrame
def get_input_table():
    return pd.DataFrame({
        "Element": ["Al", "Si", "Fe", "Mg", "Mn", "Cu", "Zn", "Ti", "Cr", "Ni"],
        "Min (%)": [88.0, 0.30, 0.15, 0.05, 0.1, 0.05, 0.01, 0.01, 0.01, 0.01],
        "Nominal (%)": [92.0, 0.35, 0.20, 0.08, 0.2, 0.10, 0.02, 0.02, 0.02, 0.02],
        "Max (%)": [99.5, 0.40, 0.25, 0.10, 0.3, 0.15, 0.05, 0.05, 0.05, 0.05]
    })

input_df = st.data_editor(get_input_table(), num_rows="dynamic", use_container_width=True)

if st.button("🔍 Hesapla"):
    result_df = input_df.copy()
    result_df["Hedef (kg)"] = (result_df["Nominal (%)"] / 100) * furnace_mass
    result_df["Min (kg)"] = (result_df["Min (%)"] / 100) * furnace_mass
    result_df["Max (kg)"] = (result_df["Max (%)"] / 100) * furnace_mass

    st.success("Hesaplama tamamlandı!")
    st.dataframe(result_df, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Grafik Gösterimi (Nominal Değerler)")
    st.bar_chart(result_df.set_index("Element")["Hedef (kg)"])
