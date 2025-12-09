from src.config import Settings


def test_log_level_uppercased():
    settings = Settings(log_level="debug")
    assert settings.log_level == "DEBUG"


def test_tickers_universe_parsing():
    settings = Settings(tickers_universe="aapl, msft , nvda")
    assert settings.tickers_universe == ["AAPL", "MSFT", "NVDA"]
