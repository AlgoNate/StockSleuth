import React, { useState, useEffect } from "react";
import StockTable from "./stock_table";

export default function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    async function fetchWatchlist() {
      try {
        const response = await fetch("/collector/watchlist.json");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStocks(data.stocks || []);
        setLastUpdated(data.last_updated || null);
      } catch (err) {
        console.error("Failed to fetch watchlist:", err);
        setStocks([]);
        setLastUpdated(null);
      }
    }

    fetchWatchlist();

    // Optional: auto-refresh every 5 minutes
    const interval = setInterval(fetchWatchlist, 300000);
    return () => clearInterval(interval);
  }, []);

  return <StockTable stocks={stocks} lastUpdated={lastUpdated} />;
}
