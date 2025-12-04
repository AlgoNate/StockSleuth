import React, { useEffect, useState } from "react";

function StockTableWrapper() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        // Use relative path based on current location
        const basePath = window.location.pathname.replace(/\/$/, "");
        const response = await fetch(`${basePath}/datafiles/watchlist.json`, {
          cache: "no-cache"
        });

        if (!response.ok) {
          console.error("Failed to fetch watchlist:", response.status);
          setStocks([]);
          return;
        }

        const data = await response.json();
        setStocks(data);
      } catch (error) {
        console.error("Error loading watchlist:", error);
        setStocks([]);
      }
    }

    loadData();
  }, []);

  return (
    <div>
      {stocks.length === 0 ? (
        <p>No stock data available</p>
      ) : (
        <table>
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
      )}
    </div>
  );
}

export default StockTableWrapper;
