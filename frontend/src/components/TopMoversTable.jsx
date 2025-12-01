import React from "react";

export default function TopMoversTable({ stocks }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Name</th>
          <th>Price</th>
          <th>% Change</th>
        </tr>
      </thead>
      <tbody>
        {stocks.map((stock) => (
          <tr key={stock.symbol}>
            <td>{stock.symbol}</td>
            <td>{stock.name}</td>
            <td>${stock.price.toFixed(2)}</td>
            <td
              style={{
                color: stock.percent_change >= 0 ? "green" : "red",
              }}
            >
              {stock.percent_change}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
