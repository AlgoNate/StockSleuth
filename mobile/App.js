import React, { useEffect, useState } from "react";
import { View, Text, ScrollView, StyleSheet } from "react-native";

export default function App() {
  const [stocks, setStocks] = useState([]);
  const DATA_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/penny-momentum-screener/main/collector/daily_stock_data.json";

  useEffect(() => {
    fetch(DATA_URL).then(res => res.json()).then(data => setStocks(data));
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.header}>Top 25 Penny Movers</Text>
      {stocks.map(s => (
        <View key={s.symbol} style={styles.card}>
          <Text>{s.symbol}: ${s.price.toFixed(3)} ({s.percent_change.toFixed(2)}%)</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container:{padding:20,backgroundColor:'#111'},
  header:{fontSize:24,fontWeight:'bold',color:'#fff',marginBottom:10},
  card:{padding:10,backgroundColor:'#222',marginBottom:5,borderRadius:5,color:'#fff'}
});
