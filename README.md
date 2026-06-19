# Stock EDA Dashboard (Apple & Google)

A Streamlit app for exploratory data analysis (EDA) on Apple (AAPL) and Google (GOOGL) stock data — visualizing price trends and patterns through interactive charts.

## Features

- Interactive exploration of AAPL and GOOGL historical stock data
- Visualizations and charts (e.g. price trends, volume, moving averages, returns)
- Live data fetched via yfinance
- Filters/widgets to slice the data (e.g. by date range or ticker)

## Tech Stack

- **Python**
- **Streamlit** – app framework
- **Pandas** – data manipulation
- **Plotly** – interactive visualizations
- **yfinance** – stock market data API

## Project Structure

```
.
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/dragangolic/Stock-EDA.git
   cd your-repo-name
   ```

2. (Optional) Create a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Live Demo

> Add your Streamlit Cloud URL here, e.g. `https://your-app-name.streamlit.app`

## Data

Stock data is fetched live using the [yfinance](https://pypi.org/project/yfinance/) library, pulling historical price and volume data for:

- **AAPL** – Apple Inc.
- **GOOGL** – Alphabet Inc. (Google)

## Disclaimer

This project is for educational and exploratory purposes only. It does not constitute financial advice.

## License

This project is open source and available under the [MIT License](LICENSE).
