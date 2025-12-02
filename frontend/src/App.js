import React, { useEffect, useState } from "react";
import { Sparklines, SparklinesLine } from "react-sparklines";

const DATA_URL = "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          const latest = data[data.length - 1].stocks.map((s) => ({
            ...s,
            percent_change:
              s.history && s.history.length > 1
                ? ((s.history[s.history.length - 1] - s.history[s.history.length - 2]) / s.history[s.history.length - 2]) * 100
                : 0,
          }));
          setStocks(latest);
        }
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="App" style={{ padding: "20px" }}>
      <h1>Top Penny Stocks</h1>
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Name</th>
            <th>Price</th>
            <th>% Change</th>
            <th>Trend</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((s, idx) => (
            <tr key={idx}>
              <td>{s.symbol}</td>
              <td>{s.name}</td>
              <td>${s.price.toFixed(2)}</td>
              <td style={{ color: s.percent_change >= 0 ? "green" : "red" }}>
                {s.percent_change.toFixed(2)}%
              </td>
              <td>
                {s.history ? (
                  <Sparklines data={s.history}>
                    <SparklinesLine color={s.percent_change >= 0 ? "green" : "red"} />
                  </Sparklines>
                ) : (
                  "—"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
