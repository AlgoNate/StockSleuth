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
         <tr key={s.symbol}>
      <td>{s.symbol}</td>
      <td>{s.name}</td>
      <td>${s.price.toFixed(2)}</td>
      <td>{s.percent_change.toFixed(2)}%</td>
    </tr>
  ))}
</tbody>
    </table>
  );
}
