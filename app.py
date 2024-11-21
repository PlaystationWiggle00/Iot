import streamlit as st
import pandas as pd

# Título
st.title("Calculadora de Producción para Tilapia, Trucha, Lechuga y Espinaca en Perú")
st.write("Esta herramienta calcula costos, ingresos y ganancias para la producción de peces y vegetales.")

# Formato de números (sin decimales)
def formatear_numero(valor):
    return f"S/ {int(round(valor)):,}".replace(",", ".")

def redondear_cantidad(valor):
    return int(round(valor))  # Redondeo a enteros para resultados numéricos

# Producción de vegetales (Lechuga, Espinaca)
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    parametros = {
        "Lechuga": {
            "meses_produccion": 2,
            "tasa_perdida": 0.05,
            "consumo_agua_mensual": 0.7,  # Litros por planta
            "costo_nutrientes": 0.2,
        },
        "Espinaca": {
            "meses_produccion": 1.5,
            "tasa_perdida": 0.07,
            "consumo_agua_mensual": 0.6,  # Litros por planta
            "costo_nutrientes": 0.15,
        },
    }

    if especie not in parametros:
        st.error("Especie no reconocida.")
        return

    datos = parametros[especie]

    plantas_vendibles = cantidad_plantas * (1 - datos["tasa_perdida"])
    consumo_total_agua = cantidad_plantas * datos["consumo_agua_mensual"] * datos["meses_produccion"]
    costo_total_nutrientes = cantidad_plantas * datos["costo_nutrientes"]
    costo_total_semillas = cantidad_plantas * costo_semilla
    costo_total_produccion = costo_total_nutrientes + costo_total_semillas
    ingreso_estimado = plantas_vendibles * precio_venta
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Plantas Vendibles": redondear_cantidad(plantas_vendibles),
        "Consumo Total de Agua (litros)": redondear_cantidad(consumo_total_agua),
        "Costo Total Nutrientes": formatear_numero(costo_total_nutrientes),
        "Costo Total Semillas": formatear_numero(costo_total_semillas),
        "Costo Total Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    # Ahora creamos una tabla detallada para Consumo de Agua y Costo de Nutrientes
    meses = int(datos["meses_produccion"])  # Número de meses de producción (1.5 para espinaca)
    
    # Ajustamos para mostrar dos filas, distribuyendo el consumo de agua y nutrientes
    consumo_agua_mes = consumo_total_agua / meses
    costo_nutrientes_mes = costo_total_nutrientes / meses

    tabla_consumo = pd.DataFrame({
        "Mes": [1, 2] if especie == "Lechuga" else [1, 2],
        "Consumo Agua (litros)": [consumo_agua_mes, consumo_agua_mes],
        "Costo Nutrientes (S/)": [formatear_numero(costo_nutrientes_mes), formatear_numero(costo_nutrientes_mes)],
    })

    return resultados, tabla_consumo

# Selección de producto
producto = st.selectbox("Selecciona el producto", ["Lechuga", "Espinaca"])

if producto in ["Lechuga", "Espinaca"]:
    st.subheader(f"Producción de {producto}")
    cantidad_plantas = st.number_input("Cantidad de Plantas", min_value=1, step=1, value=500)
    costo_semilla = st.number_input("Costo por Semilla (S/)", min_value=0.1, step=0.1, value=0.3)
    precio_venta = st.number_input("Precio de Venta por Unidad (S/)", min_value=0.1, step=0.1, value=2.0)

    if st.button(f"Calcular Producción de {producto}"):
        resultados, tabla_consumo = calcular_produccion_vegetales(producto, cantidad_plantas, costo_semilla, precio_venta)
        if resultados:
            st.write("### Resultados Generales")
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
            st.write("### Detalle de Consumo de Agua y Nutrientes")
            st.table(tabla_consumo)
