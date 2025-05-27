from dearpygui.dearpygui import *

# Fixed list of elements and target percentages (example values)
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

def calculate_callback(sender, app_data, user_data):
    furnace_mass = get_value("furnace_mass")
    result = ""
    for elem in elements:
        name = elem["name"]
        measured = get_value(f"{name}_measured")
        target_kg = furnace_mass * elem["nom"] / 100
        measured_kg = furnace_mass * measured / 100
        diff = target_kg - measured_kg
        status = "[OK]"
        if measured < elem["min"] or measured > elem["max"]:
            status = "[OUT OF RANGE]"
        result += f"{name}: Measured={measured:.2f}%, Target={elem['nom']}% -> Diff={diff:.2f} kg {status}\n"
    set_value("result_box", result)

create_context()

with font_registry():
    default_font = add_font("C:/Windows/Fonts/arial.ttf", 18)

with window(label="Furnace Alloy Calculator GUI", width=600, height=800):
    bind_font(default_font)
    add_input_float(tag="furnace_mass", label="Total Furnace Mass (kg)", default_value=5000.0, min_value=0.0, step=100.0)
    add_spacing()
    add_text("Real-Time Measured Composition (%)")

    for elem in elements:
        add_input_float(tag=f"{elem['name']}_measured", label=f"{elem['name']} (%)", default_value=elem["nom"], min_value=0.0, max_value=100.0, step=0.01)

    add_spacing(count=2)
    add_button(label="Calculate", callback=calculate_callback)
    add_spacing()
    add_input_text(tag="result_box", default_value="", multiline=True, readonly=True, width=500, height=300)

create_viewport(title="Furnace Alloy Calculator", width=700, height=800)
setup_dearpygui()
show_viewport()

while is_dearpygui_running():
    render_dearpygui_frame()

destroy_context()
