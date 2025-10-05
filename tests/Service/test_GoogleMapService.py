from src.Model.Address import Address
from src.Service.GoogleMapService import GoogleMapService


def test_validate_address_ok():
    GMService = GoogleMapService()
    adress = "51 Rue Blaise Pascal, 35170 Bruz, France"

    result = GMService.validate_address(adress)

    assert isinstance(result, Address)
    assert result.number == 51
    assert result.street == "Rue Blaise Pascal"
    assert result.city == "Bruz"
    assert result.postal_code == 35170
    assert result.country == "France"


def test_validate_address_unknown():
    GMService = GoogleMapService()
    adress = "Whisky vert : jugez cinq fox d'aplomb"

    result = GMService.validate_address(adress)

    assert not result


def test_validate_address_too_far():
    GMService = GoogleMapService()
    adress = "44 Rue Pierre Maître, 51100 Reims, France"

    result = GMService.validate_address(adress)

    assert not result


def test_get_path_to_rennes():
    GMService = GoogleMapService()
    destination = "Place de la Mairie, 35000 Rennes, France"

    result = GMService.get_path(destination)

    assert result is not None
    assert "distance" in result
    assert "duration" in result
    assert "steps" in result


def test_get_path_to_invalid_destination():
    GMService = GoogleMapService()
    destination = "Whisky vert : jugez cinq fox d'aplomb"

    result = GMService.get_path(destination)

    assert result is None
