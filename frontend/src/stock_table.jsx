// Before (likely incorrect)
fetch('collector/watchlist.json')
  .then(response => response.json())
  .then(data => {
    setWatchlist(data);
  });

// After (works for GitHub Pages deployment)
fetch(`${process.env.PUBLIC_URL}/collector/watchlist.json`)
  .then(response => response.json())
  .then(data => {
    setWatchlist(data);
  });
