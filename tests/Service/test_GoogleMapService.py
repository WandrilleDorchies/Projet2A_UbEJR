import pytest


class TestGoogleMapService:
    def test_validate_address_ok(self, google_map_service):
        """Test: Adresse valide dans la zone de livraison"""
        address = "51 Rue Blaise Pascal, 35170 Bruz, France"

        result = google_map_service.validate_address(address)

        assert result is True

    def test_validate_address_unknown(self, google_map_service):
        """Test: Adresse inexistante lève une erreur"""
        address = "Whisky vert : jugez cinq fox d'aplomb"

        with pytest.raises(ValueError, match="Address not found"):
            google_map_service.validate_address(address)

    def test_validate_address_too_far(self, google_map_service):
        """Test: Adresse trop éloignée lève une erreur"""
        address = "44 Rue Pierre Maître, 51100 Reims, France"

        with pytest.raises(ValueError, match="too far away"):
            google_map_service.validate_address(address)

    def test_extract_components_complete_address(self, google_map_service):
        """Test: Extraction des composants d'une adresse complète"""
        address = "51 Rue Blaise Pascal, 35170 Bruz, France"

        components = google_map_service.extract_components(address)

        assert components["address_number"] == 51
        assert components["address_street"] == "Rue Blaise Pascal"
        assert components["address_city"] == "Bruz"
        assert components["address_postal_code"] == 35170
        assert components["address_country"] == "France"

    def test_get_path_to_rennes(self, google_map_service):
        """Test: Récupération d'un itinéraire vers Rennes"""
        destination = "Place de la Mairie, 35000 Rennes, France"

        result = google_map_service.get_path(destination)

        assert result is not None
        assert "distance" in result
        assert "duration" in result
        assert "steps" in result

    def test_get_path_to_invalid_destination(self, google_map_service):
        """Test: Destination invalide lève une exception"""
        destination = "Whisky vert : jugez cinq fox d'aplomb"

        with pytest.raises(Exception, match="Error while computing path"):
            google_map_service.get_path(destination)
