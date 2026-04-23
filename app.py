import streamlit as st
import finanzas as fin

# 1. Configuración de la interfaz
st.set_page_config(page_title="Analizador Financiero", layout="wide")
st.title("📈 Mi Tablero de Análisis de Acciones")

# 2. Entrada de datos en la barra lateral
st.sidebar.header("Panel de Control")
ticker_input = st.sidebar.text_input("Ingresa un Ticker:", "AAPL") # "AAPL" es el valor por defecto

# Intentamos cargar los datos
try:
    accion, historial, info = fin.obtener_datos(ticker_input)

    # 4. Mostrar métricas principales
    # Usamos columnas para que se vea como un dashboard profesional
    col1, col2, col3 = st.columns(3)
    
    with col1:
        precio_actual = info.get('currentPrice', 0)
        st.metric("Precio Actual", f"${precio_actual:,.2f}")
    
    with col2:
        # Cálculo simple: ¿cuánto varió el precio hoy?
        cambio = info.get('regularMarketChangePercent', 0)
        st.metric("Variación Hoy", f"{cambio:.2f}%")
        
    with col3:
        # Dato de la función ticker
        st.metric("Sector", info.get('sector', 'N/A'))

    # 5. Visualización del gráfico
    st.subheader(f"Movimiento de {info.get('longName', ticker_input)} (Últimos 5 años)")
    st.line_chart(historial['Close'])

except Exception as e:
    st.error(f"No pudimos encontrar el ticker '{ticker_input}'. Revisa si está bien escrito.")

st.sidebar.markdown("---")
st.sidebar.header("📂 Configurador de Portafolio")

# 1. Entrada de Tickers (separados por coma)
tickers_portafolio = st.sidebar.text_input("Lista de Tickers (ej: AAPL, MSFT, TSLA):", "AAPL, MSFT, NVDA")

# 2. Capital total
capital_total = st.sidebar.number_input("Capital total a invertir ($):", value=2000000)

# 3. Convertir el texto en una lista real de Python
lista_tickers = [t.strip().upper() for t in tickers_portafolio.split(",")]

# 4. Rendimiento objetivo
min_r, max_r = fin.obtener_limites_rendimiento(lista_tickers)
media_ponderada = (min_r + max_r) / 2
rend_obj = st.sidebar.slider(
    "Rendimiento Objetivo", 
    float(min_r), 
    float(max_r), 
    float(media_ponderada),
    format="%.4f"
)

# Botón para calcular portafolio
if st.sidebar.button("Simular Portafolio"):
    st.header("📋 Análisis del Portafolio")
    
    with st.spinner("Calculando matrices y resolviendo Lagrange..."):
        # Llamamos a tu función externa
        #df_final = fin.optimizacion_lagrange(lista_tickers, capital_total, rend_obj)
        df_final = fin.optimizar_portafolio_solo_largos(lista_tickers, capital_total, rend_obj * 252)
        # Mostramos la tabla
        st.subheader("Configuración Óptima de Activos")
        
        # Formateamos la tabla para que se vea bonita
        st.table(df_final)
        
        st.success("Cálculo completado exitosamente.")
