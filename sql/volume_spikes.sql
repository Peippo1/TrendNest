-- Query to find high volume trading days

SELECT
  `date`,
  `Ticker`,
  CAST(`Volume` AS INT64) AS volume
FROM `trendnest-463421.trendnest.cleaned_stock_data`
WHERE CAST(`Volume` AS INT64) > 100000000
ORDER BY volume DESC;