def test_get_sectors(client):

    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    sectors = response.json()

    assert len(sectors) == 10


def test_information_technology_sector(client):

    response = client.get("/api/v1/sectors/Information Technology/companies")

    assert response.status_code == 200

    companies = response.json()

    assert len(companies) == 5

    for company in companies:

        assert company["broad_sector"] == "Information Technology"

        assert "ticker" in company
        assert "company_name" in company
        assert "rank" in company
