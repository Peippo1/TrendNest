-- Query to fetch the most recent close prices per ticker

SELECT
  Ticker,
  date,
  CAST(Close AS FLOAT64) AS latest_close
FROM `trendnest-463421.trendnest.cleaned_stock_data`
WHERE PARSE_DATE('%Y-%m-%d', date) = (
  SELECT MAX(PARSE_DATE('%Y-%m-%d', date))
  FROM `trendnest-463421.trendnest.cleaned_stock_data`
)
ORDER BY Ticker;