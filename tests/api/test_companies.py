def test_get_companies(client):

    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 92

    assert len(body["data"]) == 92


def test_get_tcs(client):

    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == "TCS"


def test_invalid_company(client):

    response = client.get("/api/v1/companies/INVALID")

    assert response.status_code == 404
