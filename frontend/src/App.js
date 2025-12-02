import React, { useEffect, useState } from "react";

// URL to your GitHub JSON data
const DATA_URL = "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          // Get latest entry
          setStocks(data[data.length - 1].stocks);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div style={{ padding: "1rem", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ textAlign: "center" }}>Top Penny Stocks</h1>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={thStyle}>Symbol</th>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Price ($)</th>
              <th style={thStyle}>% Change</th>
              <th style={thStyle}>History (last 7 days)</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock) => (
              <tr key={stock.symbol}>
                <td style={tdStyle}>{stock.symbol}</td>
                <td style={tdStyle}>{stock.name}</td>
                <td style={tdStyle}>{stock.price.toFixed(2)}</td>
                <td style={{ ...tdStyle, color: stock.percent_change >= 0 ? "green" : "red" }}>
                  {stock.percent_change.toFixed(2)}%
                </td>
                <td style={tdStyle}>
                  {stock.history ? stock.history.slice(-7).join(", ") : "N/A"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Styles
const thStyle = {
  border: "1px solid #ddd",
  padding: "0.5rem",
  backgroundColor: "#f2f2f2",
  textAlign: "left",
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: "0.5rem",
};

export default App;
