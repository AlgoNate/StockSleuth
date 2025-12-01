import React from "react";

function TopMoversTable({ stocks }) {
  if (!stocks || stocks.length === 0) {
    return <p>No stock data available.</p>;
  }

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={headerStyle}>Symbol</th>
          <th style={headerStyle}>Name</th>
          <th style={headerStyle}>Price ($)</th>
          <th style={headerStyle}>% Change</th>
        </tr>
      </thead>
      <tbody>
        {stocks.map((stock) => (
          <tr key={stock.symbol} style={rowStyle}>
            <td style={cellStyle}>{stock.symbol}</td>
            <td style={cellStyle}>{stock.name}</td>
            <td style={cellStyle}>{stock.price.toFixed(2)}</td>
            <td
              style={{
                ...cellStyle,
                color: stock.percent_change >= 0 ? "green" : "red",
              }}
            >
              {stock.percent_change.toFixed(2)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Inline styles for simplicity
const headerStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  backgroundColor: "#f4f4f4",
  textAlign: "left",
};

const rowStyle = {
  borderBottom: "1px solid #ddd",
};

const cellStyle = {
  border: "1px solid #ddd",
  padding: "8px",
};

export default TopMoversTable;
