import pandas as pd
from pathlib import Path
from datetime import datetime

EXCEL_PATH = Path("feedback.xlsx")


def init_excel():
    if not EXCEL_PATH.exists():
        df = pd.DataFrame(columns=[
            "timestamp",
            "query",
            "response",
            "route",
            "rating"
        ])
        df.to_excel(EXCEL_PATH, index=False)


def log_feedback(query, response, route, rating):
    new_data = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response,
        "route": route,
        "rating": rating
    }])

    if EXCEL_PATH.exists():
        existing = pd.read_excel(EXCEL_PATH)
        updated = pd.concat([existing, new_data], ignore_index=True)
    else:
        updated = new_data

    updated.to_excel(EXCEL_PATH, index=False)


def get_feedback_stats():
    if not EXCEL_PATH.exists():
        return {"total": 0, "thumbs_up": 0, "thumbs_down": 0}

    df = pd.read_excel(EXCEL_PATH)

    return {
        "total": len(df),
        "thumbs_up": len(df[df["rating"] == "👍"]),
        "thumbs_down": len(df[df["rating"] == "👎"])
    }