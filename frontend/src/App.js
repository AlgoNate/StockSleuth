import React, { useState, useEffect } from "react";

// URL to your JSON data in the repo
const DATA_URL = "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          // Use the latest entry (last item in array)
          setStocks(data[data.length - 1].stocks);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Top Penny Stocks</h1>
      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Price ($)</th>
              <th>% Change</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock) => (
              <tr key={stock.symbol}>
                <td>{stock.symbol}</td>
                <td>{stock.name}</td>
                <td>{stock.price.toFixed(2)}</td>
                <td style={{ color: stock.percent_change >= 0 ? "green" : "red" }}>
                  {stock.percent_change.toFixed(2)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Simple inline styles for responsiveness and scrollable table
const styles = {
  container: {
    padding: "20px",
    fontFamily: "Arial, sans-serif"
  },
  heading: {
    textAlign: "center",
    marginBottom: "20px"
  },
  tableWrapper: {
    overflowX: "auto"
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    minWidth: "400px"
  },
  th: {
    borderBottom: "2px solid #000",
    padding: "10px",
    textAlign: "left"
  },
  td: {
    borderBottom: "1px solid #ddd",
    padding: "10px"
  }
};

export default App;
