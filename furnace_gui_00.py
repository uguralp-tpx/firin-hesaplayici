from dearpygui.dearpygui import *

# Sabit element listesi ve hedef oranlar (örnek değerlerle)
elements = [
    {"name": "Al", "min": 88.0, "nom": 92.0, "max": 99.5},
    {"name": "Si", "min": 0.30, "nom": 0.35, "max": 0.40},
    {"name": "Fe", "min": 0.15, "nom": 0.20, "max": 0.25},
    {"name": "Mg", "min": 0.05, "nom": 0.08, "max": 0.10},
    {"name": "Mn", "min": 0.10, "nom": 0.20, "max": 0.30},
    {"name": "Cu", "min": 0.05, "nom": 0.10, "max": 0.15},
    {"name": "Zn", "min": 0.01, "nom": 0.02, "max": 0.05},
    {"name": "Ti", "min": 0.01, "nom": 0.02, "max": 0.05},
    {"name": "Cr", "min": 0.01, "nom": 0.02, "max": 0.05},
    {"name": "Ni", "min": 0.01, "nom": 0.02, "max": 0.05},
]

def hesapla_callback(sender, app_data, user_data):
    firin_yuku = get_value("firin_yuku")
    sonuc = ""
    for elem in elements:
        ad = elem["name"]
        olculen = get_value(f"{ad}_ölcum")
        hedef_kg = firin_yuku * elem["nom"] / 100
        olculen_kg = firin_yuku * olculen / 100
        fark = hedef_kg - olculen_kg
        durum = "✅"
        if olculen < elem["min"] or olculen > elem["max"]:
            durum = "⚠️ Dışında"
        sonuc += f"{ad}: Ölçülen={olculen:.2f}%, Hedef={elem['nom']}% → Fark={fark:.2f} kg {durum}\n"
    set_value("Sonuç", sonuc)

create_context()
with window(label="🧪 Fırın Alaşım Hesaplayıcı GUI", width=600, height=800):
    add_input_float(tag="firin_yuku", label="Toplam Fırın Yükü (kg)", default_value=5000.0, min_value=0.0, step=100.0)
    add_spacing()
    add_text("📡 Gerçek Zamanlı Ölçüm Değerleri (%)")

    for elem in elements:
        add_input_float(tag=f"{elem['name']}_ölcum", label=f"{elem['name']} (%)", default_value=elem["nom"], min_value=0.0, max_value=100.0, step=0.01)

    add_spacing(count=2)
    add_button(label="🔍 Hesapla", callback=hesapla_callback)
    add_spacing()
    add_input_text(tag="Sonuç", default_value="", multiline=True, readonly=True, width=500, height=300)

create_viewport(title="🧪 Fırın Alaşım Hesaplayıcı", width=700, height=800)
setup_dearpygui()
show_viewport()

while is_dearpygui_running():
    render_dearpygui_frame()

destroy_context()
