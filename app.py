import streamlit as st
import pandas as pd

# Título
st.title("Calculadora de Producción para Tilapia, Trucha, Lechuga y Espinaca en Perú")
st.write("Esta herramienta calcula costos, ingresos y ganancias para la producción de peces y vegetales.")

# Formato de números (sin decimales)
def formatear_numero(valor):
    return f"S/ {int(valor):,}".replace(",", ".")

def redondear_cantidad(valor):
    return int(valor)  # Redondeo a enteros para resultados numéricos sin decimales

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

    if especie not in parametros:
        st.error("Especie no reconocida.")
        return

    datos = parametros[especie]

    peces_vendibles = cantidad_alevines * (1 - datos["tasa_mortalidad"])
    peso_total_vendible = peces_vendibles * datos["peso_promedio"]
    consumo_total = peso_total_vendible * datos["fca"]
    costo_total_alimento = consumo_total * datos["costo_alimento_por_kg"]
    costo_total_alevines = cantidad_alevines * costo_alevin
    otros_costos = 0.1 * (costo_total_alimento + costo_total_alevines)
    costo_total_produccion = costo_total_alimento + costo_total_alevines + otros_costos
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Peces Vendibles": redondear_cantidad(peces_vendibles),
        "Peso Total Vendible (kg)": redondear_cantidad(peso_total_vendible),
        "Consumo Total de Alimento (kg)": redondear_cantidad(consumo_total),
        "Costo Total Alimentación": formatear_numero(costo_total_alimento),
        "Costo Total Alevines": formatear_numero(costo_total_alevines),
        "Otros Costos (10%)": formatear_numero(otros_costos),
        "Costo Total Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    tabla_consumo = pd.DataFrame({
        "Mes": list(range(1, datos["meses_produccion"] + 1)),
        "Consumo Alimento (kg)": [redondear_cantidad(peces_vendibles * val) for val in datos["consumo_mensual"]],
        "Costo Mensual Alimento (S/)": [formatear_numero(peces_vendibles * val * datos["costo_alimento_por_kg"]) for val in datos["consumo_mensual"]],
    })

    return resultados, tabla_consumo

# Producción de vegetales (Lechuga, Espinaca) - Ambas con ciclo de 2 meses
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    parametros = {
        "Lechuga": {
            "meses_produccion": 2,
            "tasa_perdida": 0.05,
            "consumo_agua_mensual": 0.7,  # Litros por planta
            "costo_nutrientes": 0.2,
        },
        "Espinaca": {
            "meses_produccion": 2,  # Ahora Espinaca también tiene un ciclo de 2 meses
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
    
    # Para ambos ciclos (Lechuga y Espinaca), el costo de nutrientes se distribuye entre los 2 meses
    consumo_nutrientes_mes_1 = cantidad_plantas * datos["costo_nutrientes"]
    consumo_nutrientes_mes_2 = cantidad_plantas * datos["costo_nutrientes"]

    costo_total_nutrientes = consumo_nutrientes_mes_1 + consumo_nutrientes_mes_2
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
    meses = int(datos["meses_produccion"])  # Número de meses de producción (2 meses)
    
    # Ajustamos para mostrar dos filas, distribuyendo el consumo de agua y nutrientes
    consumo_agua_mes = consumo_total_agua / meses
    tabla_consumo = pd.DataFrame({
        "Mes": [1, 2],
        "Consumo Agua (litros)": [redondear_cantidad(consumo_agua_mes), redondear_cantidad(consumo_agua_mes)],
        "Costo Nutrientes (S/)": [formatear_numero(consumo_nutrientes_mes_1), formatear_numero(consumo_nutrientes_mes_2)],
    })

    return resultados, tabla_consumo

# Selección de producto
producto = st.selectbox("Selecciona el producto", ["Tilapia", "Trucha", "Lechuga", "Espinaca"])

if producto in ["Tilapia", "Trucha"]:
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

elif producto in ["Lechuga", "Espinaca"]:
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
