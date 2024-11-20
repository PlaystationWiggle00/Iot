import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Calculadora de Producción para Tilapia, Trucha, Lechuga y Espinaca en Perú")
st.write("Esta herramienta permite calcular costos, ingresos y ganancias de manera realista para productos agrícolas y acuícolas.")

# Función para formatear números
def formatear_numero(valor):
    if isinstance(valor, int):
        return f"S/ {valor:,}"
    else:
        return f"S/ {valor:,.2f}"

# Función para producción de peces
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    if especie == "Tilapia":
        peso_promedio = 0.5
        tasa_mortalidad = 0.10
        fca = 1.6
        costo_alimento_por_kg = 3.5
        tiempo_produccion = 6
    elif especie == "Trucha":
        peso_promedio = 0.6
        tasa_mortalidad = 0.15
        fca = 1.4
        costo_alimento_por_kg = 4.0
        tiempo_produccion = 8
    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos
    peces_vendibles = cantidad_alevines * (1 - tasa_mortalidad)
    peso_total_vendible = peces_vendibles * peso_promedio
    alimento_total = peso_total_vendible * fca
    costo_alimento = alimento_total * costo_alimento_por_kg
    costo_total_alevines = cantidad_alevines * costo_alevin
    otros_costos = 0.2 * (costo_total_alevines + costo_alimento)  # Otros costos adicionales (electricidad, mantenimiento)
    costo_total_produccion = costo_total_alevines + costo_alimento + otros_costos
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Peces Vendibles": int(peces_vendibles),
        "Peso Total Vendible (kg)": peso_total_vendible,
        "Consumo Total de Alimento (kg)": alimento_total,
        "Costo de Alimentación": formatear_numero(costo_alimento),
        "Costo Total de Alevines": formatear_numero(costo_total_alevines),
        "Otros Costos (Electricidad, Mantenimiento)": formatear_numero(otros_costos),
        "Costo Total de Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }
    return resultados

# Función para producción de vegetales
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    if especie == "Lechuga":
        tiempo_produccion = 2
        tasa_perdida = 0.05
        costo_nutrientes = 0.2
    elif especie == "Espinaca":
        tiempo_produccion = 1.5
        tasa_perdida = 0.07
        costo_nutrientes = 0.15
    else:
        st.error("Especie no reconocida.")
        return

    plantas_vendibles = cantidad_plantas * (1 - tasa_perdida)
    costo_total_semillas = cantidad_plantas * costo_semilla
    costo_total_nutrientes = cantidad_plantas * costo_nutrientes
    costo_total_produccion = costo_total_semillas + costo_total_nutrientes
    ingreso_estimado = plantas_vendibles * precio_venta
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Plantas Vendibles (unidades)": int(plantas_vendibles),
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
    st.subheader(f"Producción Realista de {producto}")
    cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=1, step=1)
    costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.1, step=0.1)
    precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", min_value=1.0, step=0.1)
    if st.button(f"Calcular Producción de {producto}"):
        resultados = calcular_produccion_peces(producto, cantidad_alevines, costo_alevin, precio_venta_kilo)
        if resultados:
            for key, value in resultados.items():
                st.write(f"{key}: {value}")

elif producto in ["Lechuga", "Espinaca"]:
    st.subheader(f"Producción Realista de {producto}")
    cantidad_plantas = st.number_input("Cantidad de Plantas", min_value=1, step=1)
    costo_semilla = st.number_input("Costo por Semilla (S/)", min_value=0.1, step=0.1)
    precio_venta = st.number_input("Precio de Venta por Unidad (S/)", min_value=0.1, step=0.1)
    if st.button(f"Calcular Producción de {producto}"):
        resultados = calcular_produccion_vegetales(producto, cantidad_plantas, costo_semilla, precio_venta)
        if resultados:
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
