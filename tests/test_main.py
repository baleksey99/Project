import sys
from unittest.mock import patch
import pytest

# Импортируем главный модуль
from src.main import (
    cmd_currency_rates,
    main
)


@patch("src.main.cmd_greeting")
def test_main_greeting(mock_cmd):
    """Тест main(): вызов команды greeting."""
    test_args = ["greeting"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called()


@patch("src.main.cmd_spending_by_category")
def test_main_spending(mock_cmd):
    """Тест main(): вызов команды spending."""
    test_args = ["spending", "Еда", "2025-03-15"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with("Еда", "2025-03-15")


@patch("src.main.cmd_investment_bank")
def test_main_investment(mock_cmd):
    """Тест main(): вызов команды investment."""
    test_args = ["investment", "2025-03", "100.0"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with("2025-03", 100.0)


@patch("src.main.cmd_currency_rates")
def test_main_rates(mock_cmd):
    """Тест main(): вызов команды rates."""
    test_args = ["rates", "USD", "EUR"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with(["USD", "EUR"])


@patch("src.main.cmd_stock_prices")
def test_main_stocks(mock_cmd):
    """Тест main(): вызов команды stocks."""
    test_args = ["stocks", "AAPL", "GOOGL"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with(["AAPL", "GOOGL"])


@patch("src.main.cmd_homepage")
def test_main_homepage(mock_cmd):
    """Тест main(): вызов команды homepage."""
    test_args = ["homepage"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called()


@patch("src.main.cmd_greeting")
def test_main_greetings(mock_cmd):
    test_args = ["greeting"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called()


@patch("src.main.cmd_spending_by_category")
def test_main_spendings(mock_cmd):
    test_args = ["spending", "Еда", "2025-03-15"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with("Еда", "2025-03-15")


@patch("src.main.cmd_investment_bank")
def test_main_investments(mock_cmd):
    test_args = ["investment", "2025-03", "100.0"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with("2025-03", 100.0)


@patch("src.main.cmd_currency_rates")
def test_main_rate(mock_cmd):
    test_args = ["rates", "USD", "EUR"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with(["USD", "EUR"])


@patch("src.main.cmd_stock_prices")
def test_main_stock(mock_cmd):
    test_args = ["stocks", "AAPL", "GOOGL"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called_with(["AAPL", "GOOGL"])


@patch("src.main.cmd_homepage")
def test_main_homepages(mock_cmd):
    test_args = ["homepage"]
    with patch.object(sys, "argv", ["cli.py"] + test_args):
        main()
    mock_cmd.assert_called()


def test_main_help(capsys):
    """Тест: вызов --help выводит справку."""
    with patch.object(sys, "argv", ["cli.py", "--help"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0  # normal exit

    captured = capsys.readouterr()
    assert "Доступные команды" in captured.out
    assert "greeting" in captured.out
    assert "spending" in captured.out


@patch("src.utils.get_currency_rates")
def test_cmd_currency_rates_empty(mock_rates, capsys):
    """Тест cmd_currency_rates: пустой ответ."""
    mock_rates.return_value = []

    cmd_currency_rates(["XYZ"])
    captured = capsys.readouterr()
    assert "Нет данных для валют: ['XYZ']" in captured.out or not captured.out.strip()
