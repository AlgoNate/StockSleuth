import React, { useState, useEffect } from "react";
import StockTable from "./stock_table";

export default function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
  fetch("/StockSleuth/collector/watchlist.json")
    .then((res) => res.json())
    .then((data) => setStocks(data.stocks || []))
    .catch((err) => console.error("Error loading watchlist:", err));
}, []);
      }
    }

    fetchWatchlist();

    const interval = setInterval(fetchWatchlist, 300000); // auto-refresh every 5 min
    return () => clearInterval(interval);
  }, []);

  return <StockTable stocks={stocks} lastUpdated={lastUpdated} />;
}
