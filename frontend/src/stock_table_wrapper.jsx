// stock_table_wrapper.jsx

import React, { useEffect, useState } from "react";

const StockTableWrapper = () => {
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWatchlist = async () => {
      try {
        // Adjusted URL to fetch from GitHub Pages
        const response = await fetch(
          "https://algonate.github.io/StockSleuth/collector/watchlist.json"
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setWatchlist(data);
      } catch (error) {
        console.error("Error fetching watchlist:", error);
        setWatchlist([]);
      } finally {
        setLoading(false);
      }
    };

    fetchWatchlist();
  }, []);

  if (loading) return <p>Loading watchlist...</p>;
  if (!watchlist.length) return <p>No penny-stock data available</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Price</th>
          <th>Change</th>
        </tr>
      </thead>
      <tbody>
        {watchlist.map((stock) => (
          <tr key={stock.symbol}>
            <td>{stock.symbol}</td>
            <td>{stock.price}</td>
            <td>{stock.change}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default StockTableWrapper;
