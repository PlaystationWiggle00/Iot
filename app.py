import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Calculadora de Producción para Tilapia, Trucha, Lechuga y Espinaca en Perú")
st.write("Esta aplicación estima los costos y ganancias para la producción de tilapia, trucha, lechuga y espinaca en el contexto peruano.")

# Función para formatear números
def formatear_numero(valor):
    if isinstance(valor, int):
        return f"S/ {valor:,}"
    else:
        return f"S/ {valor:,.2f}"

# Función para calcular producción de peces (por kilo)
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    if especie == "Tilapia":
        peso_promedio = 0.5  # kg por pez
        tasa_mortalidad = 0.10  # 10%
        fca = 1.6  # Factor de Conversión Alimenticia
        costo_alimento_por_kg = 3.5  # S/ por kg de alimento
        tiempo_produccion = 6  # meses
        consumo_alimento_mensual = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]  # Consumo en kg por pez por mes
    elif especie == "Trucha":
        peso_promedio = 0.6  # kg por pez
        tasa_mortalidad = 0.15  # 15%
        fca = 1.4  # Factor de Conversión Alimenticia
        costo_alimento_por_kg = 4.0  # S/ por kg de alimento
        tiempo_produccion = 8  # meses
        consumo_alimento_mensual = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7]  # Consumo en kg por pez por mes
    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos
    peces_vendibles = cantidad_alevines * (1 - tasa_mortalidad)
    peso_total_vendible = peces_vendibles * peso_promedio
    consumo_total_mensual = [cantidad_alevines * consumo for consumo in consumo_alimento_mensual]
    alimento_total = sum(consumo_total_mensual)
    costo_alimento = alimento_total * costo_alimento_por_kg
    costo_total_alevines = cantidad_alevines * costo_alevin
    gasto_mensual = [mes * costo_alimento_por_kg for mes in consumo_total_mensual]
    costo_produccion = costo_total_alevines + costo_alimento
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_produccion

    resultados = {
        "Cantidad de Peces Vendibles": int(peces_vendibles),
        "Peso Total Vendible (kg)": peso_total_vendible,
        "Consumo Total de Alimento (kg)": alimento_total,
        "Costo de Alimento": formatear_numero(costo_alimento),
        "Costo Total de Alevines": formatear_numero(costo_total_alevines),
        "Costo Total de Producción": formatear_numero(costo_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    tablas = {
        "Consumo de Alimento Mensual (kg)": consumo_total_mensual,
        "Gasto Mensual en Alimento (S/)": gasto_mensual,
    }
    return resultados, tablas

# Función para calcular producción de vegetales
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    if especie == "Lechuga":
        tiempo_produccion = 2  # meses
        tasa_perdida = 0.05  # 5%
        consumo_agua_por_mes = 0.7  # litros por planta por mes
        costo_nutrientes_por_planta = 0.2  # S/ por planta
    elif especie == "Espinaca":
        tiempo_produccion = 1.5  # meses
        tasa_perdida = 0.07  # 7%
        consumo_agua_por_mes = 0.6  # litros por planta por mes
        costo_nutrientes_por_planta = 0.15  # S/ por planta
    else:
        st.error("Especie no reconocida.")
        return

    plantas_vendibles = cantidad_plantas * (1 - tasa_perdida)
    gasto_mensual = [costo_nutrientes_por_planta * cantidad_plantas for _ in range(int(tiempo_produccion))]
    consumo_agua_total = cantidad_plantas * consumo_agua_por_mes * tiempo_produccion
    costo_nutrientes = cantidad_plantas * costo_nutrientes_por_planta
    costo_total_semillas = cantidad_plantas * costo_semilla
    costo_produccion = costo_total_semillas + costo_nutrientes
    ingreso_estimado = plantas_vendibles * precio_venta
    ganancia = ingreso_estimado - costo_produccion

    resultados = {
        "Cantidad Vendible (unidades)": int(plantas_vendibles),
        "Consumo Total de Agua (L)": consumo_agua_total,
        "Costo de Nutrientes": formatear_numero(costo_nutrientes),
        "Costo Total de Semillas": formatear_numero(costo_total_semillas),
        "Costo Total de Producción": formatear_numero(costo_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    tablas = {
        "Gasto Mensual en Nutrientes (S/)": gasto_mensual,
    }
    return resultados, tablas

# Selección de producto
producto = st.selectbox("Selecciona el producto", ["Tilapia", "Trucha", "Lechuga", "Espinaca"])

if producto in ["Tilapia", "Trucha"]:
    st.subheader(f"Producción Realista de {producto}")
    cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=1, step=1)
    costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.0, step=0.1)
    precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", min_value=0.0, step=0.1)
    if st.button(f"Calcular Producción de {producto}"):
        resultados, tablas = calcular_produccion_peces(producto, cantidad_alevines, costo_alevin, precio_venta_kilo)
        if resultados:
            st.subheader("Resultados Generales")
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
            st.subheader("Tablas Detalladas")
            for key, value in tablas.items():
                st.write(key)
                df = pd.DataFrame({f"Mes {i+1}": [v] for i, v in enumerate(value)})
                st.table(df)

elif producto in ["Lechuga", "Espinaca"]:
    st.subheader(f"Producción Realista de {producto}")
    cantidad_plantas = st.number_input("Cantidad de Plantas", min_value=1, step=1)
    costo_semilla = st.number_input("Costo por Semilla (S/)", min_value=0.0, step=0.1)
    precio_venta = st.number_input("Precio de Venta por Unidad (S/)", min_value=0.0, step=0.1)
    if st.button(f"Calcular Producción de {producto}"):
        resultados, tablas = calcular_produccion_vegetales(producto, cantidad_plantas, costo_semilla, precio_venta)
        if resultados:
            st.subheader("Resultados Generales")
            for key, value in resultados.items():
                st.write(f"{key}: {value}")
            st.subheader("Tablas Detalladas")
            for key, value in tablas.items():
                st.write(key)
                df = pd.DataFrame({f"Mes {i+1}": [v] for i, v in enumerate(value)})
                st.table(df)
