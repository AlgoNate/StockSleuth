import React, { useEffect, useState } from 'react';
import { DATA_PATH } from './config';

const StockTable = () => {
  const [watchlist, setWatchlist] = useState([]);
  const [dailyData, setDailyData] = useState([]);

  useEffect(() => {
    // Fetch watchlist.json
    fetch(`${DATA_PATH}/watchlist.json`)
      .then((res) => res.json())
      .then((data) => setWatchlist(data))
      .catch((err) => console.error("Error fetching watchlist:", err));

    // Fetch daily_stock_data.json
    fetch(`${DATA_PATH}/daily_stock_data.json`)
      .then((res) => res.json())
      .then((data) => setDailyData(data))
      .catch((err) => console.error("Error fetching daily stock data:", err));
  }, []);

  return (
    <div>
      <h2>Stock Watchlist</h2>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
          {watchlist.map((stock, index) => (
            <tr key={index}>
              <td>{stock.symbol}</td>
              <td>{dailyData[stock.symbol]?.price || 'N/A'}</td>
              <td>{dailyData[stock.symbol]?.change || 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable;
