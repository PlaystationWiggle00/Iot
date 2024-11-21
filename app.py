import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Calculadora de Producción Agrícola y Acuícola para Perú")
st.write("Herramienta con datos reales del mercado peruano para calcular costos y rendimientos")

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

# Función para producción de peces con datos reales de Perú
def calcular_produccion_peces(especie, cantidad_alevines, costo_alevin, precio_venta_kilo):
    if especie == "Tilapia":
        # Datos reales según fuentes peruanas
        peso_promedio = 0.520  # kg por pez en 6 meses (dato de Proyectos Peruanos)
        tasa_mortalidad = 0.073  # 9,270 de 10,000 sobreviven (dato de Proyectos Peruanos)
        fca = 1.23  # Factor de conversión alimenticia real
        costo_alimento_por_kg = 6.30  # S/ por kg (dato calculado de Proyectos Peruanos)
        tiempo_produccion = 6  # meses
        # Consumo mensual basado en la curva de crecimiento
        consumo_alimento_mensual = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65]
        
        # Datos de agua y oxígeno 
        consumo_agua_diario = 4  # litros por kg de biomasa
        necesidad_oxigeno = 4.5  # mg/L mínimo requerido
        recambio_agua_porcentaje = 8  # porcentaje diario
        
    elif especie == "Trucha":
        # Datos reales para trucha en Perú
        peso_promedio = 0.275  # kg por pez (promedio comercial)
        tasa_mortalidad = 0.10  # Estimado en sistemas bien manejados
        fca = 1.3  # Factor de conversión alimenticia para trucha
        costo_alimento_por_kg = 7.20  # Aproximado basado en alimentos de alta proteína
        tiempo_produccion = 9  # meses
        consumo_alimento_mensual = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        
        consumo_agua_diario = 6  # litros por kg de biomasa
        necesidad_oxigeno = 6.5  # mg/L mínimo requerido
        recambio_agua_porcentaje = 12  # porcentaje diario
    
    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos de producción
    peces_vendibles = cantidad_alevines * (1 - tasa_mortalidad)
    peso_total_vendible = peces_vendibles * peso_promedio
    
    # Cálculo de alimento total y costos
    consumo_total_mensual = []
    biomasa_actual = cantidad_alevines * 0.001  # peso inicial aproximado
    for tasa in consumo_alimento_mensual:
        consumo_mes = biomasa_actual * tasa * 30  # consumo diario * 30 días
        consumo_total_mensual.append(consumo_mes)
        biomasa_actual = biomasa_actual * 1.2  # incremento aproximado mensual
    
    alimento_total = sum(consumo_total_mensual)
    costo_alimento = alimento_total * costo_alimento_por_kg
    costo_total_alevines = cantidad_alevines * costo_alevin
    
    # Costos operativos reales
    costo_mano_obra = 1200 * tiempo_produccion  # Sueldo mensual * meses
    costo_energia = 300 * tiempo_produccion  # Costo mensual aproximado
    costos_varios = 0.15 * (costo_alimento + costo_total_alevines)  # 15% de costos principales
    
    costo_total_produccion = (costo_alimento + costo_total_alevines + 
                             costo_mano_obra + costo_energia + costos_varios)
    
    # Cálculos de recursos
    consumo_total_agua = peso_total_vendible * consumo_agua_diario * 30 * tiempo_produccion
    recambio_total_agua = consumo_total_agua * (recambio_agua_porcentaje / 100)
    oxigeno_requerido_diario = peso_total_vendible * necesidad_oxigeno * 24  # mg/día
    
    # Ingresos y rentabilidad
    ingreso_estimado = peso_total_vendible * precio_venta_kilo
    ganancia = ingreso_estimado - costo_total_produccion
    rentabilidad = (ganancia / costo_total_produccion) * 100 if costo_total_produccion > 0 else 0

    # Costo por kg producido
    costo_por_kg = costo_total_produccion / peso_total_vendible if peso_total_vendible > 0 else 0

    resultados = {
        "Producción":
        {
            "Peces Vendibles": redondear_cantidad(peces_vendibles),
            "Peso Total Vendible (kg)": redondear_cantidad(peso_total_vendible),
            "Tiempo de Producción (meses)": tiempo_produccion
        },
        "Costos":
        {
            "Costo Total de Alevines": formatear_numero(costo_total_alevines),
            "Costo de Alimentación": formatear_numero(costo_alimento),
            "Costo de Mano de Obra": formatear_numero(costo_mano_obra),
            "Costo de Energía": formatear_numero(costo_energia),
            "Costos Varios": formatear_numero(costos_varios),
            "Costo Total de Producción": formatear_numero(costo_total_produccion),
            "Costo por Kg Producido": formatear_numero(costo_por_kg)
        },
        "Recursos":
        {
            "Consumo Total de Alimento (kg)": redondear_cantidad(alimento_total),
            "Consumo Total de Agua (litros)": redondear_cantidad(consumo_total_agua),
            "Recambio Total de Agua (litros/día)": redondear_cantidad(recambio_total_agua),
            "Oxígeno Requerido (mg/día)": redondear_cantidad(oxigeno_requerido_diario)
        },
        "Rentabilidad":
        {
            "Ingreso Estimado": formatear_numero(ingreso_estimado),
            "Ganancia Estimada": formatear_numero(ganancia),
            "Rentabilidad (%)": f"{rentabilidad:.2f}%"
        }
    }

    tablas = {
        "Consumo de Alimento Mensual (kg)": [redondear_cantidad(mes) for mes in consumo_total_mensual],
        "Gasto Mensual en Alimento (S/)": [formatear_numero(mes * costo_alimento_por_kg) for mes in consumo_total_mensual],
    }
    return resultados, tablas

# Función para producción de vegetales con datos reales
def calcular_produccion_vegetales(especie, cantidad_plantas, costo_semilla, precio_venta):
    if especie == "Lechuga":
        tiempo_produccion = 65  # días promedio en Perú
        tasa_perdida = 0.10  # 10% pérdida promedio
        costo_nutrientes_por_planta = 0.30  # S/ por planta para todo el ciclo
        consumo_agua_diario = 0.3  # litros por planta
        temperatura_optima = (15, 25)  # rango en °C
        ph_optimo = (6.0, 6.8)
        rendimiento_promedio = 0.35  # kg por planta
        densidad_siembra = 16  # plantas por m²

    elif especie == "Espinaca":
        tiempo_produccion = 45  # días promedio en Perú
        tasa_perdida = 0.12  # 12% pérdida promedio
        costo_nutrientes_por_planta = 0.25  # S/ por planta para todo el ciclo
        consumo_agua_diario = 0.25  # litros por planta
        temperatura_optima = (15, 24)  # rango en °C
        ph_optimo = (6.0, 7.0)
        rendimiento_promedio = 0.25  # kg por planta
        densidad_siembra = 20  # plantas por m²

    else:
        st.error("Especie no reconocida.")
        return

    # Cálculos de producción
    area_requerida = cantidad_plantas / densidad_siembra  # m²
    plantas_vendibles = cantidad_plantas * (1 - tasa_perdida)
    produccion_total = plantas_vendibles * rendimiento_promedio  # kg totales
    
    # Cálculos de costos
    costo_total_semillas = cantidad_plantas * costo_semilla
    costo_total_nutrientes = cantidad_plantas * costo_nutrientes_por_planta
    
    # Costos de infraestructura y operación (por ciclo)
    costo_sistema_riego = 0.5 * area_requerida  # S/ por m²
    costo_mano_obra = (1200 * (tiempo_produccion / 30))  # Sueldo mensual prorrateado
    costo_energia = 200 * (tiempo_produccion / 30)  # Costo mensual prorrateado
    
    # Consumo de recursos
    consumo_total_agua = cantidad_plantas * consumo_agua_diario * tiempo_produccion
    
    # Costos totales
    costo_total_produccion = (costo_total_semillas + costo_total_nutrientes +
                             costo_sistema_riego + costo_mano_obra + costo_energia)
    
    # Ingresos y rentabilidad
    ingreso_estimado = produccion_total * precio_venta
    ganancia = ingreso_estimado - costo_total_produccion
    rentabilidad = (ganancia / costo_total_produccion) * 100 if costo_total_produccion > 0 else 0
    costo_por_kg = costo_total_produccion / produccion_total if produccion_total > 0 else 0

    resultados = {
        "Producción":
        {
            "Área Requerida (m²)": redondear_cantidad(area_requerida),
            "Plantas Vendibles": redondear_cantidad(plantas_vendibles),
            "Producción Total (kg)": redondear_cantidad(produccion_total),
            "Tiempo de Producción (días)": tiempo_produccion
        },
        "Parámetros Técnicos":
        {
            "Temperatura Óptima (°C)": f"{temperatura_optima[0]} - {temperatura_optima[1]}",
            "pH Óptimo": f"{ph_optimo[0]} - {ph_optimo[1]}",
            "Densidad de Siembra (plantas/m²)": densidad_siembra
        },
        "Costos":
        {
            "Costo de Semillas": formatear_numero(costo_total_semillas),
            "Costo de Nutrientes": formatear_numero(costo_total_nutrientes),
            "Costo de Mano de Obra": formatear_numero(costo_mano_obra),
            "Costo de Sistema de Riego": formatear_numero(costo_sistema_riego),
            "Costo de Energía": formatear_numero(costo_energia),
            "Costo Total de Producción": formatear_numero(costo_total_produccion),
            "Costo por Kg Producido": formatear_numero(costo_por_kg)
        },
        "Recursos":
        {
            "Consumo Total de Agua (litros)": redondear_cantidad(consumo_total_agua)
        },
        "Rentabilidad":
        {
            "Ingreso Estimado": formatear_numero(ingreso_estimado),
            "Ganancia Estimada": formatear_numero(ganancia),
            "Rentabilidad (%)": f"{rentabilidad:.2f}%"
        }
    }

    tablas = {
        "Costos de Producción": [
            ["Semillas", formatear_numero(costo_total_semillas)],
            ["Nutrientes", formatear_numero(costo_total_nutrientes)],
            ["Mano de Obra", formatear_numero(costo_mano_obra)],
            ["Sistema de Riego", formatear_numero(costo_sistema_riego)],
            ["Energía", formatear_numero(costo_energia)]
        ]
    }
    return resultados, tablas

# Interfaz de usuario mejorada
st.sidebar.header("Configuración")
producto = st.sidebar.selectbox("Selecciona el producto", ["Tilapia", "Trucha", "Lechuga", "Espinaca"])

if producto in ["Tilapia", "Trucha"]:
    st.header(f"Producción de {producto}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cantidad_alevines = st.number_input("Cantidad de Alevines", min_value=100, step=100, value=1000)
    with col2:
        costo_alevin = st.number_input("Costo por Alevín (S/)", min_value=0.1, step=0.1, value=0.5)
    with col3:
        precio_venta_kilo = st.number_input("Precio de Venta por Kilo (S/)", 
                                          min_value=1.0, step=0.5,
                                          value=29.0 if producto == "Tilapia" else 24.0)  # Valores por defecto según mercado

    if st.button(f"Calcular Producción de {producto}", type="primary"):
        resultados, tablas = calcular_produccion_peces(producto, cantidad_alevines, costo_alevin, precio_venta_kilo)
