import React, { useState, useEffect } from "react";
import TopMoversTable from "./components/TopMoversTable";

// URL to your published JSON on GitHub Pages
const DATA_URL = "https://algonate.github.io/StockSleuth/collector/daily_stock_data.json";

function App() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not OK");
        return res.json();
      })
      .then((data) => {
        if (data.length > 0) {
          // Use only the latest entry
          setStocks(data[data.length - 1].stocks);
        }
      })
      .catch((err) => console.error("Error fetching data:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading top penny stocks...</p>;

  return (
    <div className="App">
      <h1>Top Penny Stocks</h1>
      <TopMoversTable stocks={stocks} />
    </div>
  );
}

export default App;
