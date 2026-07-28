def test_health_endpoint(client):

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert "db_row_counts" in data

    expected_tables = {
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
    }

    assert expected_tables.issubset(data["db_row_counts"].keys())
