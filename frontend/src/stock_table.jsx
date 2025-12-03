// Fetch watchlist.json
fetch(`${process.env.PUBLIC_URL}/collector/watchlist.json`)
  .then(response => response.json())
  .then(data => {
    setWatchlist(data);
  });

// Fetch daily_stock_data.json
fetch(`${process.env.PUBLIC_URL}/collector/daily_stock_data.json`)
  .then(response => response.json())
  .then(data => {
    setStockData(data);
  });
