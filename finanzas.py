import yfinance as yf
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def obtener_datos(simbolo):
    # Creamos el objeto ticker
    ticket_obj = yf.Ticker(simbolo)
    
    # beta, razon precio utilidad, capitalizacion de mercado

    # Obtenemos historial y la info
    hist = ticket_obj.history(period="10y")
    info = ticket_obj.info
    
    return ticket_obj, hist, info

def optimizacion_lagrange(tickers, capital_total, rend_obj):
    data = yf.download(tickers, period='1y')['Close']

    retornos = data.pct_change().dropna()
    mu = retornos.mean().values
    S = retornos.cov().values

    n = len(tickers)

    top_block = np.hstack((2 * S, mu.reshape(-1, 1), np.ones((n, 1))))
    mid_row = np.hstack((mu, 0, 0))
    bottom_row = np.hstack((np.ones(n), 0, 0))

    A = np.vstack((top_block, mid_row, bottom_row))

    b = np.zeros(n + 2)
    b[n] = rend_obj
    b[n + 1] = 1

    try:
        x = np.linalg.solve(A, b)
        pesos = x[:n]
        resultado = []
        for i, t in enumerate(tickers):
            monto = capital_total * pesos[i]
            resultado.append({
                "Ticker": t,
                "Peso (%)": pesos[i] * 100,
                "Inversión ($)": monto
            })
        return pd.DataFrame(resultado)
    except Exception as e:
        return f'Error en el cálculo: {e}'

def obtener_limites_rendimiento(tickers):
    datos = yf.download(tickers, period="1y")['Close']
    retornos_diarios = datos.pct_change().dropna()
    media_diaria = retornos_diarios.mean()
    
    # El rendimiento mínimo razonable (la acción que menos rinde)
    # y el máximo razonable (la que más rinde)
    return media_diaria.min(), media_diaria.max()

def optimizar_portafolio_solo_largos(tickers, capital_total, rendimiento_obj_anual):
    # 1. Descarga y cálculo de parámetros internos
    data = yf.download(tickers, period="1y")['Close']
    retornos_diarios = data.pct_change().dropna()
    
    # Anualizamos para que el rendimiento objetivo sea más fácil de entender (ej. 0.15 para 15%)
    mu = retornos_diarios.mean() * 252
    S = retornos_diarios.cov() * 252
    n = len(tickers)
    
    # 2. Función Objetivo: Minimizar la Varianza del Portafolio
    def varianza_portafolio(w):
        return np.dot(w.T, np.dot(S, w))

    # 3. Restricciones
    constraints = [
        # Restricción 1: La suma de los pesos debe ser 1 (100%)
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        # Restricción 2: El rendimiento esperado debe ser IGUAL al objetivo
        {'type': 'eq', 'fun': lambda w: np.sum(mu * w) - rendimiento_obj_anual}
    ]

    # 4. LA CLAVE: Bounds (Límites)
    # Esto define que cada peso está entre 0.0 y 1.0 (Sin ventas en corto)
    bounds = tuple((0, 1) for _ in range(n))

    # 5. Ejecución de la optimización
    init_guess = n * [1. / n]
    resultado = minimize(varianza_portafolio, init_guess, 
                         method='SLSQP', bounds=bounds, constraints=constraints)

    if not resultado.success:
        # Si el rendimiento objetivo es imposible de lograr sin cortos, 
        # la función avisará.
        return None

    pesos_optimos = resultado.x

    # 6. Construcción del DataFrame de salida
    df_resultado = pd.DataFrame({
        "Ticker": tickers,
        "Peso (%)": pesos_optimos * 100,
        "Inversión ($)": pesos_optimos * capital_total
    })

    return df_resultado
