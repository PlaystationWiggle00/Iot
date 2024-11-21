import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Calculadora de Producción Agrícola y Acuícola para Perú")
st.write("Herramienta para calcular costos, recursos y producción con datos realistas para Perú.")

# Función para formatear números
def formatear_numero(valor):
    if isinstance(valor, int) or valor.is_integer():
        return f"S/ {int(valor):,}"
    else:
        return f"S/ {valor:,.2f}"

def redondear_cantidad(valor):
    if isinstance(valor, int) or valor.is_integer():
        return int(valor)
    else:
        return round(valor, 2)

# Función para producción de peces con datos más detallados
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    # Datos específicos y más realistas para Perú
    if especie == "Tilapia":
        # Datos actualizados según estudios de PRODUCE y FONDEPES
        peso_promedio = 0.6  # kg por pez, considerando sistemas semi-intensivos
        tasa_mortalidad = 0.15  # Considerando sistemas con buena gestión
        fca = 1.5  # Factor de conversión alimenticia
        costo_alimento_por_kg = 3.8  # Precio actualizado 
        tiempo_produccion = 7  # meses
        consumo_alimento_mensual = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4]
        
        # Datos de agua y oxígeno específicos
        consumo_agua_diario = 5  # litros por kg de pez
        necesidad_oxigeno = 5  # mg/L, óptimo para tilapia
        recambio_agua_porcentaje = 10  # porcentaje de recambio diario
        
    elif especie == "Trucha":
        # Datos de producción en sistemas de trucha en Perú
        peso_promedio = 0.7  # kg por pez, en sistemas de altura
        tasa_mortalidad = 0.12  # Considerando sistemas tecnificados
        fca = 1.3  # Factor de conversión alimenticia
        costo_alimento_por_kg = 4.2  # Precio actualizado
        tiempo_produccion = 9  # meses
        consumo_alimento_mensual = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9]
        
        # Datos de agua y oxígeno específicos
        consumo_agua_diario = 7  # litros por kg de pez
        necesidad_oxigeno = 7  # mg/L, óptimo para trucha
        recambio_agua_porcentaje = 15  # porcentaje de recambio diario
    
    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos de producción
    peces_vendibles = cantidad_alevines * (1 - tasa_mortalidad)
    peso_total_vendible = peces_vendibles * peso_promedio
    consumo_total_mensual = [cantidad_alevines * consumo for consumo in consumo_alimento_mensual]
    alimento_total = sum(consumo_total_mensual)
    costo_alimento = alimento_total * costo_alimento_por_kg
    costo_total_alevines = cantidad_alevines * costo_alevin
    
    # Costos adicionales realistas
    costo_energia = 500  # S/ mensual para bombeo y aireación
    costo_mantenimiento = 0.3 * (costo_alimento + costo_total_alevines)
    costo_total_produccion = costo_alimento + costo_total_alevines + costo_energia + costo_mantenimiento
    
    # Cálculos de recursos
    consumo_total_agua = cantidad_alevines * consumo_agua_diario * 30 * tiempo_produccion
    recambio_total_agua = consumo_total_agua * (recambio_agua_porcentaje / 100)
    oxigeno_total_requerido = cantidad_alevines * necesidad_oxigeno * 30 * tiempo_produccion
    
    # Ingresos y ganancias
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Peces Vendibles": redondear_cantidad(peces_vendibles),
        "Peso Total Vendible (kg)": redondear_cantidad(peso_total_vendible),
        "Consumo Total de Alimento (kg)": redondear_cantidad(alimento_total),
        "Costo de Alimentación": formatear_numero(costo_alimento),
        "Costo Total de Alevines": formatear_numero(costo_total_alevines),
        "Costo de Energía y Mantenimiento": formatear_numero(costo_energia + costo_mantenimiento),
        "Costo Total de Producción": formatear_numero(costo_total_produccion),
        "Consumo Total de Agua (litros)": redondear_cantidad(consumo_total_agua),
        "Recambio Total de Agua (litros)": redondear_cantidad(recambio_total_agua),
        "Oxígeno Total Requerido (mg)": redondear_cantidad(oxigeno_total_requerido),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    tablas = {
        "Consumo de Alimento Mensual (kg)": [redondear_cantidad(mes) for mes in consumo_total_mensual],
        "Gasto Mensual en Alimento (S/)": [formatear_numero(mes * costo_alimento_por_kg) for mes in consumo_total_mensual],
    }
    return resultados, tablas

# Función para producción de vegetales con datos más precisos
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    # Datos específicos para producción en Perú, considerando sistemas hidropónicos
    if especie == "Lechuga":
        tiempo_produccion = 45  # días
        tasa_perdida = 0.08
        costo_nutrientes = 0.25
        consumo_agua_diario = 0.5  # litros por planta
        temperatura_optima = (18, 22)  # rango en grados Celsius
        ph_optimo = (5.5, 6.5)
        conductividad_electrica = (1.2, 1.8)  # mS/cm

    elif especie == "Espinaca":
        tiempo_produccion = 40  # días
        tasa_perdida = 0.1
        costo_nutrientes = 0.20
        consumo_agua_diario = 0.4  # litros por planta
        temperatura_optima = (15, 20)  # rango en grados Celsius
        ph_optimo = (6.0, 7.0)
        conductividad_electrica = (1.5, 2.0)  # mS/cm

    else:
        st.error("Especie no reconocida.")
        return

    plantas_vendibles = cantidad_plantas * (1 - tasa_perdida)
    costo_total_semillas = cantidad_plantas * costo_semilla
    costo_total_nutrientes = cantidad_plantas * costo_nutrientes * (tiempo_produccion / 30)
    
    # Costos adicionales
    costo_energia_hidroponia = 300  # S/ por ciclo de producción
    costo_sistema_riego = 200  # S/ por ciclo
    
    consumo_total_agua = cantidad_plantas * consumo_agua_diario * tiempo_produccion
    costo_total_produccion = costo_total_semillas + costo_total_nutrientes + costo_energia_hidroponia + costo_sistema_riego
    ingreso_estimado = plantas_vendibles * precio_venta
    ganancia = ingreso_estimado - costo_total_produccion

    resultados = {
        "Plantas Vendibles (unidades)": redondear_cantidad(plantas_vendibles),
        "Consumo Total de Agua (litros)": redondear_cantidad(consumo_total_agua),
        "Temperatura Óptima (°C)": f"{temperatura_optima[0]} - {temperatura_optima[1]}",
        "Rango de pH Óptimo": f"{ph_optimo[0]} - {ph_optimo[1]}",
        "Conductividad Eléctrica (mS/cm)": f"{conductividad_electrica[0]} - {conductividad_electrica[1]}",
        "Costo Total de Semillas": formatear_numero(costo_total_semillas),
        "Costo Total de Nutrientes": formatear_numero(costo_total_nutrientes),
        "Costo de Energía e Infraestructura": formatear_numero(costo_energia_hidroponia + costo_sistema_riego),
        "Costo Total de Producción": formatear_numero(costo_total_produccion),
        "Ingreso Estimado": formatear_numero(ingreso_estimado),
        "Ganancia Estimada": formatear_numero(ganancia),
    }

    tablas = {
        "Gasto Mensual en Nutrientes (S/)": [formatear_numero(costo_total_nutrientes)],
    }
    return resultados, tablas

# Interfaz de Streamlit
producto = st.selectbox("Selecciona el producto", ["Tilapia", "Trucha", "Lechuga", "Espinaca"])

if producto in ["Tilapia", "Trucha"]:
    st.subheader(f"Producción Realista de {producto}")
    cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=1, step=1)
    costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.1, step=0.1)
    precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", min_value=1.0, step=0.1)
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
    costo_semilla = st.number_input("Costo por Semilla (S/)", min_value=0.1, step=0.1)
    precio_venta = st.number_input("Precio de Venta por Unidad (S/)", min_value=0.1, step=0.1)
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
