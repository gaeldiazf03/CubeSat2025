import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

styles: dict = {
    "title": "Delphinus Cubesat v1.1",
    "themename": "united",
    "size": (1620, 800),
    "resizable": ("false", "false")
}

logo_png = os.path.join(BASE_DIR, "img", "iconoCansat_nb.png")

icon_png = os.path.join(BASE_DIR, "img", "Delfin16.png")

main_sub_color: str = "primary"

variables_monitorear: list = [
    "Temperatura",
    "Latitud",
    "Longitud",
    "Presión",
    "Humedad",
    "Altura",
    "AX",
    "AY",
    "AZ",
    "GX",
    "GY",
    "GZ",
    "MX",
    "MY",
    "MZ",
    "CO2",
    "Velocidad",
    "Batería"
]
