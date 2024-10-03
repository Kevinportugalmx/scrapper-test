import json
import csv
import requests

url = "https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    raise SystemExit(f"Error al obtener los datos: {e}")

data = response.json()
all_variants = data.get("allVariants", [])

if not all_variants:
    raise ValueError("No se encontraron variantes en los datos obtenidos.")

attributes_raw = all_variants[0].get("attributesRaw", [])
custom_attributes = next(
    (attr for attr in attributes_raw if attr.get("name") == "custom_attributes"),
    None,
)

if not custom_attributes:
    raise ValueError("No se encontraron atributos personalizados.")

values = json.loads(custom_attributes["value"]["es-CR"])


def extract_value(key):
    """Función auxiliar para extraer valores del diccionario con manejo seguro."""
    return values.get(key, {}).get("value", "")


def format_boolean(value):
    """Función auxiliar para convertir valores booleanos o cadenas a mayúsculas."""
    if isinstance(value, bool):
        return str(value).upper()
    elif isinstance(value, str):
        return value.upper()
    return ""


def safe_float(value):
    """Función para convertir una cadena a float de manera segura."""
    try:
        return round(float(value), 1)
    except (ValueError, TypeError):
        raise ValueError(f"No se pudo convertir el valor '{value}' a float.")


allergens = [item["name"] for item in values.get("allergens", {}).get("value", [])]

data_output = {
    "allergens": ", ".join(allergens),
    "sku": extract_value("sku"),
    "vegan": format_boolean(extract_value("vegan")),
    "kosher": format_boolean(extract_value("kosher")),
    "organic": format_boolean(extract_value("organic")),
    "vegetarian": format_boolean(extract_value("vegetarian")),
    "gluten_free": format_boolean(extract_value("gluten_free")),
    "lactose_free": format_boolean(extract_value("lactose_free")),
    "package_quantity": extract_value("package_quantity"),
    "unit_size": safe_float(extract_value("unit_size")),
    "net_weight": safe_float(extract_value("net_weight")),
}

csv_file = "output-product.csv"
try:
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data_output.keys())
        writer.writeheader()
        writer.writerow(data_output)
    print(f"Datos exportados exitosamente en: {csv_file}")
except IOError as e:
    raise SystemExit(f"Error al escribir en el archivo CSV: {e}")
