import React, { useState, useEffect } from "react";
import StockTable from "./stock_table";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch("/api/stocks"); // Replace with your API
      const data = await res.json();
      setStocks(data.stocks);
      setLastUpdated(data.lastUpdated); // Must be ISO timestamp
    }

    fetchData();
    const interval = setInterval(fetchData, 60000); // refresh every 1 minute
    return () => clearInterval(interval);
  }, []);

  return <stock_table stocks={stocks} lastUpdated={lastUpdated} />;
}
