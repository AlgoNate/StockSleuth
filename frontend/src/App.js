import React, { useEffect, useState } from "react";
import { DATA_URL } from "./config";
import TopMoversTable from "./components/TopMoversTable";

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
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
      <TopMoversTable stocks={stocks} />
    </div>
  );
}

export default App;
