import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Calculadora de Producción para Tilapia, Trucha, Lechuga y Espinaca")
st.write("Esta aplicación estima los costos y ganancias para la producción de tilapia, trucha, lechuga y espinaca en Perú.")

# Función para formatear números
def formatear_numero(valor):
    return f"S/ {valor:,.2f}"

# Función para calcular producción de peces (por kilo)
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    # Datos específicos por especie
    if especie == "Tilapia":
        consumo_alimento_mensual = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]  # kg por pez por mes
        tiempo_cria = 6  # meses
        tasa_mortalidad = 0.10  # 10%
        peso_promedio = 0.3  # Peso en kg al momento de la venta
    elif especie == "Trucha":
        consumo_alimento_mensual = [0.6, 1.2, 1.8, 2.4, 3.0, 3.5, 4.0, 4.5]  # kg por pez por mes
        tiempo_cria = 8  # meses
        tasa_mortalidad = 0.15  # 15%
        peso_promedio = 1.0  # Peso en kg al momento de la venta
    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos
    costo_total_alevines = cantidad_alevines * costo_alevin
    consumo_alimento_total = [cantidad_alevines * consumo for consumo in consumo_alimento_mensual[:tiempo_cria]]
    consumo_alimento_total_sum = sum(consumo_alimento_total)
    agua_necesaria = cantidad_alevines * 0.2 * tiempo_cria  # m³ totales
    oxigeno_necesario = cantidad_alevines * 0.1 * tiempo_cria  # L totales
    costo_alimento = consumo_alimento_total_sum * 3.5  # S/ por kg de alimento
    costo_produccion = costo_total_alevines + costo_alimento
    cantidad_vendible = cantidad_alevines * (1 - tasa_mortalidad)
    peso_total_vendible = cantidad_vendible * peso_promedio  # Total en kg para venta
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_produccion

    # Resultados
    resultados = {
        "Costo Total de Alevines": formatear_numero(costo_total_alevines),
        "Consumo de Alimento por Mes (kg)": [f"{consumo:.2f} kg" for consumo in consumo_alimento_total],
        "Consumo Total de Alimento (kg)": f"{consumo_alimento_total_sum:.2f} kg",
        "Agua Necesaria (m³)": f"{agua_necesaria:.2f}",
        "Oxígeno Necesario (L)": f"{oxigeno_necesario:.2f}",
        "Costo de Alimento": formatear_numero(costo_alimento),
        "Costo Total de Producción": formatear_numero(costo_produccion),
        "Peso Total Vendible (kg)": f"{peso_total_vendible:.2f} kg",
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia)
    }
    return resultados

# Función para calcular producción de vegetales
def calcular_produccion_vegetales(especie, cantidad_semillas, costo_semilla, precio_venta):
    # Datos específicos por especie
    if especie == "Lechuga":
        consumo_nutrientes_mensual = [0.05, 0.07]  # kg por planta por mes
        tasa_perdida = 0.05  # 5%
    elif especie == "Espinaca":
        consumo_nutrientes_mensual = [0.04, 0.06]  # kg por planta por mes
        tasa_perdida = 0.07  # 7%
    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos
    costo_total_semillas = cantidad_semillas * costo_semilla
    consumo_nutrientes_total = [cantidad_semillas * consumo for consumo in consumo_nutrientes_mensual]
    consumo_nutrientes_total_sum = sum(consumo_nutrientes_total)
    agua_necesaria = cantidad_semillas * 0.1  # m³
    costo_nutrientes = consumo_nutrientes_total_sum * 2.0  # S/ por kg de nutrientes
    costo_produccion = costo_total_semillas + costo_nutrientes
    cantidad_vendible = cantidad_semillas * (1 - tasa_perdida)
    ingreso_estimado = cantidad_vendible * precio_venta
    ganancia = ingreso_estimado - costo_produccion

    # Resultados
    resultados = {
        "Costo Total de Semillas": formatear_numero(costo_total_semillas),
        "Consumo de Nutrientes por Mes (kg)": [f"{consumo:.2f} kg" for consumo in consumo_nutrientes_total],
        "Consumo Total de Nutrientes (kg)": f"{consumo_nutrientes_total_sum:.2f} kg",
        "Agua Necesaria (m³)": f"{agua_necesaria:.2f}",
        "Costo de Nutrientes": formatear_numero(costo_nutrientes),
        "Costo Total de Producción": formatear_numero(costo_produccion),
        "Cantidad Vendible (unidades)": f"{cantidad_vendible:.0f} unidades",
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia)
    }
    return resultados

# Selección de producto
producto = st.selectbox("Selecciona el producto", ["Tilapia", "Trucha", "Lechuga", "Espinaca"])

# Entrada de datos según el producto
if producto in ["Tilapia", "Trucha"]:
    st.subheader(f"Producción de {producto}")
    cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=1, step=1)
    costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.0, step=0.1)
    precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", min_value=0.0, step=0.1)
    if st.button(f"Calcular Producción de {producto}"):
        resultados = calcular_produccion_peces(producto, cantidad_alevines, costo_alevin, precio_venta_kilo)
        if resultados:
            st.subheader("Resultados")
            for key, value in resultados.items():
                if isinstance(value, list):
                    st.write(f"{key}:")
                    df = pd.DataFrame({f"Mes {i+1}": [v] for i, v in enumerate(value)})
                    st.table(df.style.format("{:,.2f}"))
                else:
                    st.write(f"{key}: {value}")

elif producto in ["Lechuga", "Espinaca"]:
    st.subheader(f"Producción de {producto}")
    cantidad_semillas = st.number_input("Cantidad de Semillas", min_value=1, step=1)
    costo_semilla = st.number_input("Costo por Semilla (S/)", min_value=0.0, step=0.1)
    precio_venta = st.number_input("Precio de Venta por Unidad (S/)", min_value=0.0, step=0.1)
    if st.button(f"Calcular Producción de {producto}"):
        resultados = calcular_produccion_vegetales(producto, cantidad_semillas, costo_semilla, precio_venta)
        if resultados:
            st.subheader("Resultados")
            for key, value in resultados.items():
                if isinstance(value, list):
                    st.write(f"{key}:")
                    df = pd.DataFrame({f"Mes {i+1}": [v] for i, v in enumerate(value)})
                    st.table(df.style.format("{:,.2f}"))
                else:
                    st.write(f"{key}: {value}")
