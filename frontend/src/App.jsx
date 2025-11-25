import React, { useEffect, useState } from "react";
import TopMoversTable from "./components/TopMoversTable";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const DATA_URL = "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

  useEffect(() => {
    fetch(DATA_URL)
      .then(res => res.json())
      .then(data => setStocks(data));
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh", background: "#111", color: "#fff" }}>
      <aside style={{ width: "220px", padding: "20px", borderRight: "1px solid #333" }}>
        <h1 style={{ fontSize: "24px", marginBottom: "20px" }}>Momentum Screener</h1>
        <ul><li>Top Movers</li></ul>
      </aside>
      <main style={{ flex: 1, padding: "20px" }}>
        <h2 style={{ fontSize: "22px", marginBottom: "10px" }}>Top 25 Penny Stock Movers</h2>
        <TopMoversTable stocks={stocks} />
      </main>
    </div>
  );
}
