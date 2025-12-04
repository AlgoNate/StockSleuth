useEffect(() => {
  async function loadData() {
    try {
      const response = await fetch("./datafiles/watchlist.json", { cache: "no-cache" });
      if (!response.ok) {
        console.error("Failed to fetch watchlist:", response.status);
        setStocks([]);
        return;
      }
      const data = await response.json();
      setStocks(data);
    } catch (error) {
      console.error("Error loading watchlist:", error);
      setStocks([]);
    }
  }

  loadData();
}, []);
