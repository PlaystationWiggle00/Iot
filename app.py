import streamlit as st
import pandas as pd

st.title("Calculadora de Producción para Tilapia, Trucha, Lechuga y Espinaca en Perú")
st.write("Calcula costos, ingresos y ganancias de manera realista para productos agrícolas y acuícolas.")

# Formato de números
def formatear_numero(valor):
    return f"S/ {valor:,.2f}"

def redondear_cantidad(valor):
    return int(valor) if isinstance(valor, int) or valor.is_integer() else round(valor, 2)

# Cálculos de peces
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    parametros = {
        "Tilapia": {
            "peso_promedio": 0.52,
            "tasa_mortalidad": 0.073,
            "fca": 1.23,
            "costo_alimento_por_kg": 6.30,
            "tiempo_produccion": 6,
            "consumo_mensual": [0.2, 0.4, 0.6, 0.8, 1.0, 1.2],  # kg/alimento por pez
        },
        "Trucha": {
            "peso_promedio": 0.6,
            "tasa_mortalidad": 0.15,
            "fca": 1.4,
            "costo_alimento_por_kg": 4.00,
            "tiempo_produccion": 8,
            "consumo_mensual": [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7],  # kg/alimento por pez
        },
    }

    if especie not in parametros:
        st.error("Especie no reconocida.")
        return

    datos = parametros[especie]
    peces_vendibles = cantidad_alevines * (1 - datos["tasa_mortalidad"])
    peso_total_vendible = peces_vendibles * datos["peso_promedio"]
    consumo_total_mensual = [cantidad_alevines * consumo for consumo in datos["consumo_mensual"]]
    consumo_total = sum(consumo_total_mensual)
    costo_alimento = consumo_total * datos["costo_alimento_por_kg"]
    costo_total_alevines = cantidad_alevines * costo_alevin
    otros_costos = 0.2 * (costo_alimento + costo_total_alevines)
    costo_total_produccion = costo_alimento + costo_total_alevines + otros_costos
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Peces Vendibles": redondear_cantidad(peces_vendibles),
        "Peso Total Vendible (kg)": redondear_cantidad(peso_total_vendible),
        "Consumo Total de Alimento (kg)": redondear_cantidad(consumo_total),
        "Costo de Alimentación": formatear_numero(costo_alimento),
        "Costo Total de Alevines": formatear_numero(costo_total_alevines),
        "Otros Costos": formatear_numero(otros_costos),
        "Costo Total de Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    tabla_consumo = pd.DataFrame({
        "Mes": list(range(1, datos["tiempo_produccion"] + 1)),
        "Consumo Alimento (kg)": consumo_total_mensual,
        "Costo Mensual (S/)": [c * datos["costo_alimento_por_kg"] for c in consumo_total_mensual],
    })

    return resultados, tabla_consumo

# Cálculos de vegetales
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    parametros = {
        "Lechuga": {
            "tiempo_produccion": 2,
            "tasa_perdida": 0.05,
            "costo_nutrientes": 0.2,
            "consumo_agua_mes": 0.7,
        },
        "Espinaca": {
            "tiempo_produccion": 1.5,
            "tasa_perdida": 0.07,
            "costo_nutrientes": 0.15,
            "consumo_agua_mes": 0.6,
        },
    }

    if especie not in parametros:
        st.error("Especie no reconocida.")
        return

    datos = parametros[especie]
    plantas_vendibles = cantidad_plantas * (1 - datos["tasa_perdida"])
    costo_total_semillas = cantidad_plantas * costo_semilla
    costo_total_nutrientes = cantidad_plantas * datos["costo_nutrientes"]
    consumo_total_agua = cantidad_plantas * datos["consumo_agua_mes"] * datos["tiempo_produccion"]
    costo_total_produccion = costo_total_semillas + costo_total_nutrientes
    ingreso_estimado = plantas_vendibles * precio_venta
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Plantas Vendibles": redondear_cantidad(plantas_vendibles),
        "Consumo Total de Agua (litros)": redondear_cantidad(consumo_total_agua),
        "Costo Total de Semillas": formatear_numero(costo_total_semillas),
        "Costo Total de Nutrientes": formatear_numero(costo_total_nutrientes),
        "Costo Total de Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    return resultados

# Selección de producto
producto = st.selectbox("Selecciona el producto", ["Tilapia", "Trucha", "Lechuga", "Espinaca"])

if producto in ["Tilapia", "Trucha"]:
    st.subheader(f"Producción de {producto}")
    cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=1, step=1, value=1000)
    costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.1, step=0.1, value=0.5)
    precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", min_value=1.0, step=0.1, value=30.0)
    if st.button(f"Calcular Producción de {producto}"):
        resultados, tabla_consumo = calcular_produccion_peces(producto, cantidad_alevines, costo_alevin, precio_venta_kilo)
        if resultados:
            st.write("### Resultados Generales")
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
            st.write("### Consumo de Alimento Mensual")
            st.table(tabla_consumo)

elif producto in ["Lechuga", "Espinaca"]:
    st.subheader(f"Producción de {producto}")
    cantidad_plantas = st.number_input("Cantidad de Plantas", min_value=1, step=1, value=500)
    costo_semilla = st.number_input("Costo por Semilla (S/)", min_value=0.1, step=0.1, value=0.3)
    precio_venta = st.number_input("Precio de Venta por Unidad (S/)", min_value=0.1, step=0.1, value=2.0)
    if st.button(f"Calcular Producción de {producto}"):
        resultados = calcular_produccion_vegetales(producto, cantidad_plantas, costo_semilla, precio_venta)
        if resultados:
            st.write("### Resultados Generales")
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
