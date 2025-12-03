import React, { useState, useEffect } from "react";
import StockTable from "./stock_table";
import "./stock_table.css";

export default function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchWatchlist() {
      try {
        // ✅ Use relative path for GitHub Pages
        const response = await fetch("./collector/watchlist.json");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStocks(data.stocks || []);
        setLastUpdated(data.last_updated || null);
      } catch (error) {
        console.error("Failed to fetch watchlist:", error);
        setStocks([]);
        setLastUpdated(null);
      } finally {
        setLoading(false);
      }
    }

    fetchWatchlist();
  }, []);

  if (loading) return <p>Loading penny-stock data...</p>;

  if (!stocks || stocks.length === 0)
    return <p>No penny‑stock data available.</p>;

  return <StockTable stocks={stocks} lastUpdated={lastUpdated} />;
}
