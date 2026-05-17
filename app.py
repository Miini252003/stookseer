from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session

from modules.auth import AuthManager
from modules.comparison import normalize_prices
from modules.data import fetch_stock_history
from modules.indicators import add_technical_indicators
from modules.predictor import HybridPredictor


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = os.getenv("STOCKSEER_SECRET_KEY", "stockseer-dev-secret-key")

auth_manager = AuthManager(BASE_DIR / "users.json")
predictor = HybridPredictor(seq_len=30, epochs=10, batch_size=32)


def _json_error(message: str, status: int = 400):
    return jsonify({"success": False, "error": message}), status


def _optional_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip().lower()
    password = str(data.get("password", ""))
    name = str(data.get("name", "")).strip() or username

    if not username or not password:
        return _json_error("Username and password are required.")

    success, message = auth_manager.register_user(username, password, name)
    if not success:
        return _json_error(message, 409)

    return jsonify({"success": True, "message": message})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip().lower()
    password = str(data.get("password", ""))

    if not username or not password:
        return _json_error("Username and password are required.")

    valid, profile = auth_manager.validate_user(username, password)
    if not valid:
        return _json_error("Invalid username or password.", 401)

    session["user"] = username
    session["name"] = profile.get("name", username)
    return jsonify({"success": True, "name": session["name"]})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})


@app.route("/api/me", methods=["GET"])
def me():
    if "user" not in session:
        return _json_error("Not authenticated.", 401)
    return jsonify({"success": True, "user": session["user"], "name": session["name"]})


@app.route("/api/stocks/<ticker>/history", methods=["GET"])
def stock_history(ticker: str):
    if "user" not in session:
        return _json_error("Login required.", 401)

    days = max(90, min(_optional_int(request.args.get("days"), 365), 3650))
    try:
        df = fetch_stock_history(ticker=ticker, days=days)
        df = add_technical_indicators(df)
    except Exception as exc:  # pragma: no cover - defensive runtime error path
        return _json_error(f"Unable to fetch stock data: {exc}", 500)

    payload = {
        "ticker": ticker.upper(),
        "days": days,
        "history": [
            {
                "date": idx.strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]),
                "sma_20": float(row["SMA_20"]),
                "ema_20": float(row["EMA_20"]),
                "rsi_14": float(row["RSI_14"]),
                "bb_upper": float(row["BB_UPPER"]),
                "bb_lower": float(row["BB_LOWER"]),
            }
            for idx, row in df.iterrows()
        ],
    }
    return jsonify({"success": True, **payload})


@app.route("/api/stocks/<ticker>/predict", methods=["GET"])
def stock_predict(ticker: str):
    if "user" not in session:
        return _json_error("Login required.", 401)

    days = max(120, min(_optional_int(request.args.get("days"), 730), 3650))
    horizon = max(1, min(_optional_int(request.args.get("n_days"), 7), 30))

    try:
        df = fetch_stock_history(ticker=ticker, days=days)
        df = add_technical_indicators(df)
        result = predictor.predict_next_n(ticker=ticker, history_df=df, n_days=horizon)
    except ValueError as exc:
        return _json_error(str(exc), 422)
    except Exception as exc:  # pragma: no cover - defensive runtime error path
        return _json_error(f"Prediction failed: {exc}", 500)

    return jsonify({"success": True, "ticker": ticker.upper(), **result})


@app.route("/api/stocks/compare", methods=["GET"])
def stock_compare():
    if "user" not in session:
        return _json_error("Login required.", 401)

    ticker_a = str(request.args.get("ticker_a", "")).strip().upper()
    ticker_b = str(request.args.get("ticker_b", "")).strip().upper()
    days = max(60, min(_optional_int(request.args.get("days"), 365), 3650))

    if not ticker_a or not ticker_b:
        return _json_error("ticker_a and ticker_b are required.")

    try:
        df_a = fetch_stock_history(ticker=ticker_a, days=days)
        df_b = fetch_stock_history(ticker=ticker_b, days=days)
    except Exception as exc:  # pragma: no cover - defensive runtime error path
        return _json_error(f"Unable to fetch comparison data: {exc}", 500)

    series_a = df_a["Close"].tolist()
    series_b = df_b["Close"].tolist()
    date_axis = [d.strftime("%Y-%m-%d") for d in df_a.index]

    return jsonify(
        {
            "success": True,
            "ticker_a": ticker_a,
            "ticker_b": ticker_b,
            "dates": date_axis,
            "normalized_a": normalize_prices(series_a),
            "normalized_b": normalize_prices(series_b),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
