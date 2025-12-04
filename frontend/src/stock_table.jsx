// Base URL points to /collector/ in GitHub Pages
const BASE_URL = "https://algonate.github.io/StockSleuth/collector/";

// Fetch watchlist.json
fetch(BASE_URL + "watchlist.json", { cache: "no-cache" })
  .then(res => res.json())
  .then(data => console.log("Watchlist:", data));

// Fetch daily_stock_data.json
fetch(BASE_URL + "daily_stock_data.json", { cache: "no-cache" })
  .then(res => res.json())
  .then(data => console.log("Daily Stock Data:", data));
