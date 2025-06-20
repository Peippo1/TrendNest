SELECT
    FORMAT_DATE('%Y-%m', PARSE_DATE('%Y-%m-%d', date)) AS month,
    ROUND(AVG(CAST(Close AS FLOAT64)), 2) AS avg_close,
    ROUND(AVG(CAST(Volume AS INT64))) AS avg_volume
FROM `trendnest
-463421.trendnest.cleaned_stock_data`
WHERE Ticker = 'AAPL'
GROUP BY month
ORDER BY month;