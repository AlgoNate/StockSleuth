import React, { useState, useEffect } from "react";

function App() {
  const [stocks, setStocks] = useState([]);
  const DATA_URL = "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

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
    <div style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <h1>Top Penny Stocks</h1>
      {stocks.length === 0 ? (
        <p>No data available.</p>
      ) : (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th style={thStyle}>Symbol</th>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Price ($)</th>
              <th style={thStyle}>% Change</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock) => (
              <tr key={stock.symbol}>
                <td style={tdStyle}>{stock.symbol}</td>
                <td style={tdStyle}>{stock.name}</td>
                <td style={tdStyle}>{stock.price.toFixed(2)}</td>
                <td style={tdStyle}>{stock.percent_change.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

const thStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  backgroundColor: "#f2f2f2",
  textAlign: "left",
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: "8px",
};

export default App;
