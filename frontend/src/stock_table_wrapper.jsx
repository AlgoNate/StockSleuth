import React, { useState, useEffect } from "react";
import StockTable from "./stock_table";

export default function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState("");

  useEffect(() => {
    async function fetchWatchlist() {
      try {
        const response = await fetch("/collector/watchlist.json");
        if (!response.ok) throw new Error("Watchlist not found");
        const data = await response.json();
        setStocks(data.stocks || []);
        setLastUpdated(data.last_updated || "");
      } catch (error) {
        console.error("Error fetching watchlist:", error);
        setStocks([]);
        setLastUpdated("");
      }
    }

    fetchWatchlist();
  }, []);

  return (
    <div>
      <p>Last Updated: {lastUpdated}</p>
      <StockTable stocks={stocks} />
      {stocks.length === 0 && <p>No penny-stock data available.</p>}
    </div>
  );
}
