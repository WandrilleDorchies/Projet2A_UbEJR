import pytest

from src.Model.Address import Address
from src.Service.GoogleMapService import GoogleMapService


class TestGoogleMapService:
    def test_validate_address_ok(self, address_dao):
        GMService = GoogleMapService(address_dao)
        adress = "51 Rue Blaise Pascal, 35170 Bruz, France"

        result = GMService.validate_address(adress)

        assert isinstance(result, Address)
        assert result.address_number == 51
        assert result.address_street == "Rue Blaise Pascal"
        assert result.address_city == "Bruz"
        assert result.address_postal_code == 35170
        assert result.address_country == "France"

    def test_validate_address_unknown(self, address_dao):
        GMService = GoogleMapService(address_dao)
        adress = "Whisky vert : jugez cinq fox d'aplomb"

        result = GMService.validate_address(adress)

        assert not result

    def test_validate_address_too_far(self, address_dao):
        GMService = GoogleMapService(address_dao)
        adress = "44 Rue Pierre Maître, 51100 Reims, France"

        result = GMService.validate_address(adress)

        assert not result

    def test_get_path_to_rennes(self, address_dao):
        GMService = GoogleMapService(address_dao)
        destination = "Place de la Mairie, 35000 Rennes, France"

        result = GMService.get_path(destination)

        assert result is not None
        assert "distance" in result
        assert "duration" in result
        assert "steps" in result

    def test_get_path_to_invalid_destination(self, address_dao):
        GMService = GoogleMapService(address_dao)
        destination = "Whisky vert : jugez cinq fox d'aplomb"
        with pytest.raises(Exception, match="Error while computing path: NOT_FOUND"):
            GMService.get_path(destination)
