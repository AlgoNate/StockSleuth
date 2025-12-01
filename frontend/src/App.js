import React, { useState, useEffect } from "react";
import TopMoversTable from "./components/TopMoversTable";

// URL to the raw JSON on GitHub
const DATA_URL =
  "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then((data) => {
        if (data.length > 0) {
          // Use the latest entry (last item in array)
          setStocks(data[data.length - 1].stocks);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="App">
      <h1>Top Penny Stocks</h1>
      {stocks.length > 0 ? (
        <TopMoversTable stocks={stocks} />
      ) : (
        <p>Loading stock data...</p>
      )}
    </div>
  );
}

export default App;
