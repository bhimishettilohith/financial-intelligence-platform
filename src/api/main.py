"""
Sprint 6 - Day 38

FastAPI application entry point.
"""

from __future__ import annotations

import logging
import sqlite3
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    companies,
    documents,
    health,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "data" / "nifty100.db"

APP_VERSION = "1.0.0"

START_TIME = time.time()

# -----------------------------------------------------------------------------
# FastAPI
# -----------------------------------------------------------------------------

app = FastAPI(
    title="Financial Intelligence Platform API",
    version=APP_VERSION,
)

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------


def get_db_connection() -> sqlite3.Connection:
    """
    Return SQLite connection.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# Make available to routers
app.state.get_db_connection = get_db_connection
app.state.start_time = START_TIME
app.state.version = APP_VERSION

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Request Logging Middleware
# -----------------------------------------------------------------------------


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.perf_counter()

    response = await call_next(request)

    elapsed = (time.perf_counter() - start) * 1000

    logger.info(
        "%s %s completed in %.2f ms",
        request.method,
        request.url.path,
        elapsed,
    )

    return response


# -----------------------------------------------------------------------------
# Routers
# -----------------------------------------------------------------------------

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    companies.router,
    prefix="/api/v1",
    tags=["Companies"],
)

app.include_router(
    screener.router,
    prefix="/api/v1",
    tags=["Screener"],
)

app.include_router(
    sectors.router,
    prefix="/api/v1",
    tags=["Sectors"],
)

app.include_router(
    peers.router,
    prefix="/api/v1",
    tags=["Peers"],
)

app.include_router(
    valuation.router,
    prefix="/api/v1",
    tags=["Valuation"],
)

app.include_router(
    portfolio.router,
    prefix="/api/v1",
    tags=["Portfolio"],
)

app.include_router(
    documents.router,
    prefix="/api/v1",
    tags=["Documents"],
)
