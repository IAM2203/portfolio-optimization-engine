# QuantPort: Portfolio Optimization Engine

QuantPort is a quantitative finance tool built with Python that enables users to construct optimal investment portfolios based on **Modern Portfolio Theory (MPT)**. The application leverages advanced mathematical optimization to determine asset allocations that balance risk and return effectively.

## Key Features

- **Mean-Variance Optimization:** Uses quadratic programming to find the portfolio with the lowest risk for a given target return.
- **Long-Only Constraint:** Custom optimization logic that prevents short selling ($w_i \ge 0$), making it applicable for standard retail brokerage accounts.
- **Live Data Integration:** Seamless connection with the `yfinance` API to fetch real-time and historical adjusted closing prices.
- **Interactive Dashboard:** A clean, responsive UI built with Streamlit for real-time portfolio simulation and capital allocation.
- **Automated Financial Metrics:** Internal calculation of annualized return vectors ($\mu$) and covariance matrices ($\Sigma$).

## To-Do / Future Roadmap

- [ ] **Efficient Frontier Visualization:** Implement a Plotly graph to display the Risk vs. Return curve visually.
- [ ] **Maximum Sharpe Ratio (Auto-Optimize):** Add a feature to automatically find the "Tangency Portfolio" (the point of maximum efficiency).
- [ ] **Monte Carlo Simulations:** Generate and plot 10,000+ random portfolios to visualize the feasible set of allocations.
- [ ] **Historical Backtesting:** Allow users to test their optimized portfolio against past market data to validate the strategy.
- [ ] **Risk Metrics:** Integrate Value at Risk (VaR) and Conditional VaR (CVaR) calculations.
- [ ] **Export Reports:** Generate PDF summaries of the optimized portfolio and its expected performance.

## Tech Stack

* **Language:** [Python 3.9+](https://www.python.org/)
* **Dashboard:** [Streamlit](https://streamlit.io/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Mathematical Solver:** [SciPy (Optimize)](https://scipy.org/)
* **Financial Data:** [yfinance](https://aroussi.com/post/python-yahoo-finance)

## Project Structure

├── app.py                # Main Streamlit interface and UI logic

├── finanzas.py           # Financial engine (Lagrange & Optimization logic)

└── README.md             # Project documentation
