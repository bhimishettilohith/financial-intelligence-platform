"""
Sprint 6 - Day 38

Health endpoint.
"""

from __future__ import annotations

import time

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request):

    db_status = "connected"
    row_counts = {}

    try:

        conn = request.app.state.get_db_connection()

        cursor = conn.cursor()

        tables = [
            "companies",
            "profitandloss",
            "balancesheet",
            "cashflow",
            "analysis",
            "documents",
            "prosandcons",
            "financial_ratios",
            "computed_financial_ratios",
            "sectors",
            "peer_groups",
            "peer_percentiles",
            "stock_prices",
        ]

        for table in tables:

            try:

                cursor.execute(f"SELECT COUNT(*) FROM {table}")

                row_counts[table] = cursor.fetchone()[0]

            except Exception:

                row_counts[table] = None

        conn.close()

    except Exception as e:

        db_status = "disconnected"

        row_counts = {}

        return {
            "status": "error",
            "database": db_status,
            "error": str(e),
        }

    uptime = round(
        time.time() - request.app.state.start_time,
        2,
    )

    return {
        "status": "ok",
        "database": db_status,
        "version": request.app.state.version,
        "uptime_seconds": uptime,
        "db_row_counts": row_counts,
    }
