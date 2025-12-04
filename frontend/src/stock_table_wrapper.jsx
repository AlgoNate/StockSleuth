import React, { useState, useEffect } from "react";

function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        // Fetch the JSON from the public folder
        const response = await fetch("/datafiles/watchlist.json", { cache: "no-cache" });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setStocks(data);
      } catch (err) {
        console.error("Error loading watchlist:", err);
        setError("Failed to load stock data.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return <p>Loading stocks...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (stocks.length === 0) {
    return <p>No stocks to display.</p>;
  }

  return (
    <div>
      <h2>Stock Watchlist</h2>
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Name</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr key={stock.symbol}>
              <td>{stock.symbol}</td>
              <td>{stock.name}</td>
              <td>{stock.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StockTableWrapper;
