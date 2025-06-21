

# Changelog

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