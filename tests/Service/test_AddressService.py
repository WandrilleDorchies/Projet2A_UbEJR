from typing import List, Optional
from unittest.mock import Mock, create_autospec

import pytest
from src.utils.GoogleMapService import GoogleMapService

from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address
from src.Service.AddressService import AddressService


class TestAddressService:
    
    @pytest.fixture
    def mock_address_dao(self):
        return create_autospec(AddressDAO)
    
    @pytest.fixture
    def mock_gm_service(self):
        return create_autospec(GoogleMapService)
    
    @pytest.fixture
    def address_service(self, mock_address_dao, mock_gm_service):
        return AddressService(mock_address_dao, mock_gm_service)
    
    @pytest.fixture
    def sample_address(self):
        return Address(
            address_id=1,
            address_number=123,
            address_street="Main St",
            address_city="Test City",
            address_postal_code=12345,
            address_country="Test Country"
        )

    # Tests for get_address_by_id
    def test_get_address_by_id_success(self, address_service, mock_address_dao, sample_address):
        # Arrange
        mock_address_dao.get_address_by_id.return_value = sample_address
        
        # Act
        result = address_service.get_address_by_id(1)
        
        # Assert
        assert result == sample_address
        mock_address_dao.get_address_by_id.assert_called_once_with(1)

    def test_get_address_by_id_not_found(self, address_service, mock_address_dao):
        # Arrange
        mock_address_dao.get_address_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Cannot find: Address with ID 1 not found."):
            address_service.get_address_by_id(1)

    # Tests for get_address_by_customer_id
    def test_get_address_by_customer_id_success(self, address_service, mock_address_dao, sample_address):
        # Arrange
        mock_address_dao.get_address_by_customer_id.return_value = sample_address
        
        # Act
        result = address_service.get_address_by_customer_id(1)
        
        # Assert
        assert result == sample_address
        mock_address_dao.get_address_by_customer_id.assert_called_once_with(1)

    def test_get_address_by_customer_id_not_found(self, address_service, mock_address_dao):
        # Arrange
        mock_address_dao.get_address_by_customer_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Cannot find Address for customer ID 1 not found."):
            address_service.get_address_by_customer_id(1)

    # Tests for get_all_address
    def test_get_all_address_success(self, address_service, mock_address_dao, sample_address):
        # Arrange
        addresses = [sample_address]
        mock_address_dao.get_all_address.return_value = addresses
        
        # Act
        result = address_service.get_all_address()
        
        # Assert
        assert result == addresses
        mock_address_dao.get_all_address.assert_called_once()

    def test_get_all_address_empty(self, address_service, mock_address_dao):
        # Arrange
        mock_address_dao.get_all_address.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="No adresses in the database."):
            address_service.get_all_address()

    def test_get_all_address_empty_list(self, address_service, mock_address_dao):
        # Arrange
        mock_address_dao.get_all_address.return_value = []
        
        # Act & Assert
        with pytest.raises(ValueError, match="No adresses in the database."):
            address_service.get_all_address()

    # Tests for create_address
    def test_create_address_success(self, address_service, mock_address_dao, mock_gm_service, sample_address):
        # Arrange
        address_string = "123 Main St, 12345 Test City, Test Country"
        components = {
            'address_number': 123,
            'address_street': "Main St",
            'address_city': "Test City",
            'address_postal_code': 12345,
            'address_country': "Test Country"
        }
        mock_gm_service.extract_components.return_value = components
        mock_address_dao.create_address.return_value = sample_address
        
        # Act
        result = address_service.create_address(address_string)
        
        # Assert
        assert result == sample_address
        mock_gm_service.validate_address.assert_called_once_with(address_string)
        mock_gm_service.extract_components.assert_called_once_with(address_string)
        mock_address_dao.create_address.assert_called_once_with(**components)

    # Tests for update_address
    def test_update_address_success(self, address_service, mock_address_dao, mock_gm_service, sample_address):
        # Arrange
        address_id = 1
        update_data = {
            'address_street': "New St",
            'address_city': "New City"
        }
        expected_components = {
            'address_number': 123,
            'address_street': "New St",
            'address_city': "New City",
            'address_postal_code': 12345,
            'address_country': "Test Country"
        }
        
        mock_address_dao.get_address_by_id.return_value = sample_address
        mock_gm_service.extract_components.return_value = expected_components
        mock_address_dao.update_address.return_value = sample_address
        
        # Act
        result = address_service.update_address(address_id, update_data)
        
        # Assert
        assert result == sample_address
        mock_address_dao.get_address_by_id.assert_called_once_with(address_id)
        expected_address_string = "123 New St,12345 New City, Test Country"
        mock_gm_service.validate_address.assert_called_once_with(expected_address_string)
        mock_gm_service.extract_components.assert_called_once_with(expected_address_string)
        mock_address_dao.update_address.assert_called_once_with(address_id, expected_components)

    def test_update_address_no_changes(self, address_service, mock_address_dao, sample_address):
        # Arrange
        address_id = 1
        update_data = {
            'address_street': None,
            'address_city': None
        }
        mock_address_dao.get_address_by_id.return_value = sample_address
        
        # Act & Assert
        with pytest.raises(ValueError, match="Cannot update address: You must change at least one field."):
            address_service.update_address(address_id, update_data)

    def test_update_address_partial_update(self, address_service, mock_address_dao, mock_gm_service, sample_address):
        # Arrange
        address_id = 1
        update_data = {
            'address_street': "New St",
            'address_city': None  # This should be filled with current value
        }
        expected_components = {
            'address_number': 123,
            'address_street': "New St",
            'address_city': "Test City",  # From current address
            'address_postal_code': 12345,
            'address_country': "Test Country"
        }
        
        mock_address_dao.get_address_by_id.return_value = sample_address
        mock_gm_service.extract_components.return_value = expected_components
        mock_address_dao.update_address.return_value = sample_address
        
        # Act
        result = address_service.update_address(address_id, update_data)
        
        # Assert
        assert result == sample_address
        expected_address_string = "123 New St,12345 Test City, Test Country"
        mock_gm_service.validate_address.assert_called_once_with(expected_address_string)

    # Tests for delete_address
    def test_delete_address_success(self, address_service, mock_address_dao, sample_address):
        # Arrange
        address_id = 1
        mock_address_dao.get_address_by_id.return_value = sample_address
        
        # Act
        address_service.delete_address(address_id)
        
        # Assert
        mock_address_dao.get_address_by_id.assert_called_once_with(address_id)
        mock_address_dao.delete_address_by_id.assert_called_once_with(address_id)

    def test_delete_address_not_found(self, address_service, mock_address_dao):
        # Arrange
        address_id = 1
        mock_address_dao.get_address_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Cannot find: Address with ID 1 not found."):
            address_service.delete_address(address_id)