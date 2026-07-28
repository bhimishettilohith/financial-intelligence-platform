def test_min_roe(client):

    response = client.get("/api/v1/screener?min_roe=15")

    assert response.status_code == 200

    companies = response.json()

    for company in companies:

        assert company["return_on_equity_pct"] >= 15


def test_invalid_parameter(client):

    response = client.get("/api/v1/screener?max_pe=25")

    assert response.status_code == 400
