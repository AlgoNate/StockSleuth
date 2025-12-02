import React, { useEffect, useState } from "react";
import { View, Text, ScrollView, StyleSheet } from "react-native";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const DATA_URL =
    "https://raw.githubusercontent.com/AlgoNate/StockSleuth/main/collector/daily_stock_data.json";

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const latest = data[data.length - 1];
          if (latest.stocks && Array.isArray(latest.stocks)) {
            setStocks(latest.stocks);
          } else {
            setStocks([]);
          }
        } else {
          setStocks([]);
        }
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError(err);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.header}>Top Penny Stocks</Text>

      {loading && <Text style={styles.info}>Loading stocks...</Text>}
      {error && <Text style={styles.error}>Error loading data.</Text>}

      {!loading && !error && stocks.length === 0 && (
        <Text style={styles.info}>No penny stock data available.</Text>
      )}

      {stocks.map((s) => (
        <View key={s.symbol} style={styles.card}>
          <Text style={styles.symbol}>{s.symbol}</Text>
          <Text style={styles.name}>{s.name}</Text>
          <Text
            style={[
              styles.price,
              s.percent_change >= 0 ? styles.positive : styles.negative
            ]}
          >
            ${s.price.toFixed(3)} ({s.percent_change.toFixed(2)}%)
          </Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#111"
  },
  content: {
    padding: 20
  },
  header: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 15,
    textAlign: "center"
  },
  info: {
    color: "#ccc",
    marginBottom: 10,
    textAlign: "center"
  },
  error: {
    color: "#ff4d4d",
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center"
  },
  card: {
    padding: 12,
    backgroundColor: "#222",
    marginBottom: 10,
    borderRadius: 8
  },
  symbol: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16
  },
  name: {
    color: "#ccc",
    marginBottom: 5
  },
  price: {
    fontSize: 14,
    fontWeight: "bold"
  },
  positive: {
    color: "#00b300"
  },
  negative: {
    color: "#ff4d4d"
  }
});
