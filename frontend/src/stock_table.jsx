import React, { useEffect, useState } from "react";

const BASE_URL = "https://<username>.github.io/<repo-name>/datafiles/"; 
// Replace <username> and <repo-name> with your GitHub username and repo

export default function StockTable() {
  const [watchlist, setWatchlist] = useState([]);
  const [stockData, setStockData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: "symbol", direction: "asc" });

  // Function to fetch both JSON files
  const fetchData = () => {
    fetch(BASE_URL + "watchlist.json", { cache: "no-cache" })
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch((err) => console.error("Error fetching watchlist:", err));

    fetch(BASE_URL + "daily_stock_data.json", { cache: "no-cache" })
      .then((res) => res.json())
      .then((data) => setStockData(data))
      .catch((err) => console.error("Error fetching stock data:", err));
  };

  // Fetch initially and then set up interval
  useEffect(() => {
    fetchData(); // Initial fetch

    const interval = setInterval(() => {
      fetchData();
    }, 300000); // 300000 ms = 5 minutes

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  const displayData = watchlist.map((symbol) => {
    const stock = stockData.find((s) => s.symbol === symbol);
    return stock || { symbol, name: "-", price: "-", change: "-" };
  });

  // Sorting function
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
        {sortedData.map((stock) => (
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
  );
}
