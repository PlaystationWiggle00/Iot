import streamlit as st
import pandas as pd

# Título
st.title("Calculadora de Producción para Tilapia y Trucha en Perú")
st.write("Esta herramienta calcula costos, ingresos y ganancias para la producción de peces.")

# Formato de números (sin decimales)
def formatear_numero(valor):
    return f"S/ {int(round(valor)):,}".replace(",", ".")

def redondear_cantidad(valor):
    return int(round(valor))  # Redondeo a enteros para resultados numéricos

# Producción de peces
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    parametros = {
        "Tilapia": {
            "peso_promedio": 0.52,  # kg por pez al final del ciclo
            "tasa_mortalidad": 0.073,
            "fca": 1.23,  # Factor de conversión alimenticia
            "costo_alimento_por_kg": 6.30,  # S/
            "meses_produccion": 6,
            "consumo_mensual": [0.2, 0.4, 0.6, 0.8, 1.0, 1.2],  # Consumo mensual de alimento (kg por pez)
        },
        "Trucha": {
            "peso_promedio": 0.6,  # kg por pez al final del ciclo
            "tasa_mortalidad": 0.15,
            "fca": 1.4,
            "costo_alimento_por_kg": 4.00,  # S/
            "meses_produccion": 8,
            "consumo_mensual": [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7],
        },
    }

    # Validar especie
    if especie not in parametros:
        st.error("Especie no reconocida.")
        return

    datos = parametros[especie]

    # Peces sobrevivientes
    peces_vendibles = cantidad_alevines * (1 - datos["tasa_mortalidad"])
    peso_total_vendible = peces_vendibles * datos["peso_promedio"]

    # Consumo total de alimento
    consumo_total_mensual = [peces_vendibles * consumo for consumo in datos["consumo_mensual"]]
    costo_mensual_alimento = [consumo * datos["costo_alimento_por_kg"] for consumo in consumo_total_mensual]

    # Ajustar consumo total basado en peso final (usando FCA correctamente)
    consumo_total = peso_total_vendible * datos["fca"]
    costo_total_alimento = consumo_total * datos["costo_alimento_por_kg"]

    # Costos totales
    costo_total_alevines = cantidad_alevines * costo_alevin
    otros_costos = 0.1 * (costo_total_alimento + costo_total_alevines)  # 10% para electricidad, mano de obra, etc.
    costo_total_produccion = costo_total_alimento + costo_total_alevines + otros_costos

    # Ingresos y ganancias
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_total_produccion

    # Resultados generales
    resultados = {
        "Peces Vendibles": redondear_cantidad(peces_vendibles),  # Entero porque son peces
        "Peso Total Vendible (kg)": redondear_cantidad(peso_total_vendible),
        "Consumo Total de Alimento (kg)": redondear_cantidad(consumo_total),
        "Costo Total Alimentación": formatear_numero(costo_total_alimento),
        "Costo Total Alevines": formatear_numero(costo_total_alevines),
        "Otros Costos (10%)": formatear_numero(otros_costos),
        "Costo Total Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    # Tabla detallada
    tabla_consumo = pd.DataFrame({
        "Mes": list(range(1, datos["meses_produccion"] + 1)),
        "Consumo Alimento (kg)": [redondear_cantidad(val) for val in consumo_total_mensual],
        "Costo Mensual Alimento (S/)": [formatear_numero(val) for val in costo_mensual_alimento],
    })

    return resultados, tabla_consumo

# Selección de producto
producto = st.selectbox("Selecciona el producto", ["Tilapia", "Trucha"])

if producto:
    st.subheader(f"Producción de {producto}")
    cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=1, step=1, value=1000)
    costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.1, step=0.1, value=0.5)
    precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", min_value=1.0, step=0.1, value=20.0)

    if st.button(f"Calcular Producción de {producto}"):
        resultados, tabla_consumo = calcular_produccion_peces(producto, cantidad_alevines, costo_alevin, precio_venta_kilo)

        if resultados:
            st.write("### Resultados Generales")
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
            st.write("### Detalle de Consumo de Alimento por Mes")
            st.table(tabla_consumo)
