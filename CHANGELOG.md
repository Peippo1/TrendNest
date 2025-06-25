# Changelog

## [v1.2.1] – 2025-06-21
### Added
- Full pipeline loop for top 10 performing tickers.
- Flattened yfinance MultiIndex columns for clean BigQuery compatibility.
- Timestamp parsing and cleaning for Gemini summaries.
- Diagnostic output for column schema validation.

### Fixed
- Type error in Gemini summary step caused by inconsistent 'date' types.
- Residual multi-ticker column duplication.

### Improved
- AI summary clarity and structure.
- Logging consistency across pipeline stages.

## [v1.1.2] – 2025-06-21
### Added
- Support for dynamic multi-ticker analysis (top 10 performing stocks)
- Flattened column handling for BigQuery compatibility
- Improved BigQuery schema with descriptions and required fields
- Secure `.env` and `.gcp/` handling with gitignore enforcement

### Fixed
- Bug with non-string column names in upload step
- Gemini summary formatting

### Notes
This release makes the pipeline fully production-ready for multiple tickers, with AI summaries and cloud integration.