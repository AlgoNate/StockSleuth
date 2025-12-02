import React, { useState, useEffect } from "react";

const DATA_URL = "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          setStocks(data[data.length - 1].stocks);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="App" style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Top Penny Stocks</h1>
      <div style={{ overflowX: "auto" }}>
        <table border="1" cellPadding="8" cellSpacing="0">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Price</th>
              <th>% Change</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((s) => (
              <tr key={s.symbol}>
                <td>{s.symbol}</td>
                <td>{s.name}</td>
                <td>${s.price.toFixed(2)}</td>
                <td>{s.percent_change.toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
