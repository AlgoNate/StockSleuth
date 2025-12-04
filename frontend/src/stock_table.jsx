import React, { useEffect, useState } from "react";

const StockTable = () => {
  const [stockData, setStockData] = useState([]);
  const [watchlist, setWatchlist] = useState([]);

  useEffect(() => {
    // Fetch daily stock data
    fetch(`${process.env.PUBLIC_URL}/datafiles/daily_stock_data.json`)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch stock data");
        return response.json();
      })
      .then((data) => setStockData(data))
      .catch((error) => console.error("Stock data fetch error:", error));

    // Fetch watchlist
    fetch(`${process.env.PUBLIC_URL}/datafiles/watchlist.json`)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch watchlist");
        return response.json();
      })
      .then((data) => setWatchlist(data))
      .catch((error) => console.error("Watchlist fetch error:", error));
  }, []);

  return (
    <div className="stock-table-wrapper">
      <h2>Stock Watchlist</h2>
      <table className="stock-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Company</th>
            <th>Price</th>
            <th>Change</th>
            <th>Watchlist</th>
          </tr>
        </thead>
        <tbody>
          {stockData.map((stock) => {
            const inWatchlist = watchlist.includes(stock.symbol);
            return (
              <tr key={stock.symbol} className={inWatchlist ? "highlight" : ""}>
                <td>{stock.symbol}</td>
                <td>{stock.company}</td>
                <td>{stock.price}</td>
                <td>{stock.change}</td>
                <td>{inWatchlist ? "⭐" : ""}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable;
