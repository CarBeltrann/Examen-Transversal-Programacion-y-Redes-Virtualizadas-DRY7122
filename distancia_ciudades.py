import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjZjZDI3NjZhMjI0ZDRiMDlhNjRlN2RhYjY5YjMzMDQyIiwiaCI6Im11cm11cjY0In0="

def obtener_coordenadas(ciudad, pais):
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        'api_key': API_KEY,
        'text': ciudad,
        'boundary.country': pais
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'features' in data and len(data['features']) > 0:
        coords = data['features'][0]['geometry']['coordinates']
        return coords
    else:
        print(f"❌ No se encontró la ciudad '{ciudad}'. Verifica el nombre.")
        return None

def traducir_transporte(opcion):
    tipos = {
        "auto": "driving-car",
        "bicicleta": "cycling-regular",
        "caminar": "foot-walking"
    }
    return tipos.get(opcion.lower(), None)

def calcular_ruta(origen_coords, destino_coords, transporte):
    url = f"https://api.openrouteservice.org/v2/directions/{transporte}/geojson"
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        'coordinates': [origen_coords, destino_coords]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

while True:
    print("\n===== Calcular distancia entre ciudades (Chile - Argentina) =====")
    origen = input("Ingrese ciudad de origen (o 's' para salir): ").strip()
    if origen.lower() == "s":
        print("✅ Programa finalizado.")
        break

    destino = input("Ingrese ciudad de destino: ").strip()

    print("\nOpciones de transporte: auto / bicicleta / caminar")
    transporte_opcion = input("Ingrese tipo de transporte: ").strip()
    transporte = traducir_transporte(transporte_opcion)

    if not transporte:
        print("❌ Transporte no válido. Intente con: auto, bicicleta o caminar.")
        continue

    origen_coords = obtener_coordenadas(origen, "CL")
    destino_coords = obtener_coordenadas(destino, "AR")

    if origen_coords and destino_coords:
        ruta = calcular_ruta(origen_coords, destino_coords, transporte)

        try:
            segmento = ruta['features'][0]['properties']['segments'][0]
            distancia_km = segmento['distance'] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion_horas = segmento['duration'] / 3600

            print(f"\n📍 Distancia: {distancia_km:.2f} km | {distancia_millas:.2f} millas")
            print(f"🕒 Duración estimada: {duracion_horas:.2f} horas")

            print("\n📢 Primeros pasos del viaje:")
            for idx, paso in enumerate(segmento['steps'][:3], 1):
                print(f"{idx}. {paso['instruction']}")
        except Exception as e:
            print("❌ Error al calcular la ruta:", e)
    else:
        print("⚠️ No se pudo obtener las coordenadas correctamente.")

