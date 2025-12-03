import React, { useState, useEffect } from "react";
import StockTable from "./stock_table";

export default function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

 useEffect(() => {
  async function fetchWatchlist() {
    try {
      const response = await fetch("./collector/watchlist.json");
      const data = await response.json();
      setStocks(data.stocks || []);
      setLastUpdated(data.last_updated || null);
    } catch (err) {
      console.error("Error loading watchlist:", err);
    }
  }

  fetchWatchlist();
}, []);

  return <StockTable stocks={stocks} lastUpdated={lastUpdated} />;
}
