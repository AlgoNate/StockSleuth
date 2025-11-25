import React from "react";

export default function TopMoversTable({ stocks }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Price</th>
          <th>% Change</th>
        </tr>
      </thead>
      <tbody>
        {stocks.map(s => (
          <tr key={s.symbol} style={{ borderBottom: "1px solid #333" }}>
            <td>{s.symbol}</td>
            <td>${s.price.toFixed(3)}</td>
            <td style={{ color: s.percent_change>0 ? "lime" : "red" }}>{s.percent_change.toFixed(2)}%</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
