import React, { useState, useEffect } from "react";
import StockTable from "./StockTable";
import "./styles/globals.css";

function App() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const DATA_URL =
    "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const latest = data[data.length - 1];
          setStocks(latest.stocks || []);
          setLastUpdated(latest.timestamp || null);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="App container">
      <h1>StockSleuth — Penny Stock Dashboard</h1>
      <StockTable stocks={stocks} lastUpdated={lastUpdated} />
    </div>
  );
}

export default App;
