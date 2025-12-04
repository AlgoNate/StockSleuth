import React, { useEffect, useState } from "react";

const BASE_URL = "https://<username>.github.io/<repo-name>/datafiles/"; 
// Replace <username> and <repo-name> with your GitHub username and repo

export default function StockTable() {
  const [watchlist, setWatchlist] = useState([]);
  const [stockData, setStockData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: "symbol", direction: "asc" });
  const [lastUpdated, setLastUpdated] = useState(null);
  const [loading, setLoading] = useState(false);

  // Step 2 — Fetch data safely with loading indicator
  const fetchData = async () => {
    setLoading(true);
    try {
      const [watchlistRes, stockRes] = await Promise.all([
        fetch(BASE_URL + "watchlist.json", { cache: "no-cache" }),
        fetch(BASE_URL + "daily_stock_data.json", { cache: "no-cache" })
      ]);

      const watchlistJson = await watchlistRes.json();
      const stockJson = await stockRes.json();

      setWatchlist(watchlistJson);
      setStockData(stockJson);
      setLastUpdated(new Date()); // Set local timestamp
    } catch (err) {
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  // Step 3 — Auto-refresh every 5 minutes
  useEffect(() => {
    fetchData(); // initial fetch
    const interval = setInterval(fetchData, 5 * 60 * 1000); // 5 min
    return () => clearInterval(interval); // cleanup
  }, []);

  // Step 4 — Merge watchlist with stock data
  const displayData = watchlist.map(symbol => {
    const stock = stockData.find(s => s.symbol === symbol);
    return stock || { symbol, name: "-", price: "-", change: "-" };
  });

  // Step 5 — Sort function
  const sortedData = [...displayData].sort((a, b) => {
    if (a[sortConfig.key] === undefined) return 1;
    if (b[sortConfig.key] === undefined) return -1;

    let aValue = a[sortConfig.key];
    let bValue = b[sortConfig.key];

    if (sortConfig.key === "price" || sortConfig.key === "change") {
      aValue = parseFloat(aValue) || 0;
      bValue = parseFloat(bValue) || 0;
    }

    if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
    return 0;
  });

  const requestSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  return (
    <div>
      {/* Step 6 — Display last updated and loading indicator */}
      <p style={{ fontSize: "0.9em", fontStyle: "italic" }}>
        {loading ? "Refreshing..." : lastUpdated ? `Last updated: ${lastUpdated.toLocaleString()}` : "Loading..."}
      </p>

      {/* Step 7 — Stock table */}
      <table style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th style={{ cursor: "pointer" }} onClick={() => requestSort("symbol")}>Symbol</th>
            <th style={{ cursor: "pointer" }} onClick={() => requestSort("name")}>Name</th>
            <th style={{ cursor: "pointer" }} onClick={() => requestSort("price")}>Price</th>
            <th style={{ cursor: "pointer" }} onClick={() => requestSort("change")}>Change</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map(stock => (
            <tr key={stock.symbol}>
              <td>{stock.symbol}</td>
              <td>{stock.name}</td>
              <td>{stock.price}</td>
              <td style={{ color: parseFloat(stock.change) > 0 ? "green" : parseFloat(stock.change) < 0 ? "red" : "black" }}>
                {stock.change}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
