import math
import os
from datetime import datetime
from typing import Optional

import googlemaps

from src.DAO.AddressDAO import AddressDAO
from src.Model.Address import Address
from src.utils.log_decorator import log


class GoogleMapService:
    """
    Service for interacting with Google Maps API to validate addresses and compute delivery routes.

    Attributes
    ----------
    ensai_address : str
        adress of ENSAI
    coord_ensai : dict
       Latitude and longitude of ENSAI
    coord_rennes : tuple
        Coordinates of the extremity of Rennes
    radius : float
        Maximum delivery distance from ENSAI
    """

    addressDAO: AddressDAO

    def __init__(self, address_dao: AddressDAO) -> None:
        self.__gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])
        self.ensai_address = "51 Rue Blaise Pascal, 35170 Bruz, France"

        ensai_geocode = self.__gmaps.geocode(self.ensai_address)
        self.coord_ensai = ensai_geocode[0]["geometry"]["location"]

        self.coord_rennes = (48.137922, -1.632842)
        self.radius = math.sqrt(
            (self.coord_rennes[0] - self.coord_ensai["lat"]) ** 2
            + (self.coord_rennes[1] - self.coord_ensai["lng"]) ** 2
        )
        self.address_dao = address_dao

    @log
    def validate_address(self, address: str) -> Optional[Address]:
        """
        Validate that an address exists and is within the delivery zone.
        The delivery zone is defined as a circle centered on ENSAI with radius
        extending to the extremity of Rennes.

        Args
        ----
        address (str): address to test

        Returns
        -------
        Address or None
            An Address object if valid and within range, None otherwise
        """

        result = self.__gmaps.geocode(address)

        if not result:
            return None

        coord_address = result[0]["geometry"]["location"]

        if (coord_address["lat"] - self.coord_ensai["lat"]) ** 2 + (
            coord_address["lng"] - self.coord_ensai["lng"]
        ) ** 2 > self.radius**2:
            raise ValueError("The destination is too far away to get delivered.")

        number = street = city = postal_code = country = None
        for component in result[0]["address_components"]:
            if "street_number" in component["types"]:
                number = component["long_name"]

            if "route" in component["types"]:
                street = component["long_name"]

            if "locality" in component["types"]:
                city = component["long_name"]

            if "postal_code" in component["types"]:
                postal_code = component["long_name"]

            if "country" in component["types"]:
                country = component["long_name"]
        try:
            address_validated = self.address_dao.create_address(
                number=int(number),
                street=street,
                city=city,
                postal_code=int(postal_code),
                country=country,
            )
            return address_validated

        except ValueError as e:
            raise ValueError(f"An error occured during the creation of the Address class : {e}")

    @log
    def get_path(self, destination: str) -> Optional[dict]:
        """
        Compute the driving route from ENSAI to a destination address.

        Args
        ----
        destination (str): address of the destination

        Returns
        -------
        dict: a dictionnary containing all the informations to print the path to the destination
        """
        now: datetime = datetime.now()

        try:
            directions_result = self.__gmaps.directions(
                self.ensai_address, destination, mode="driving", departure_time=now, language="fr"
            )

            if not directions_result:
                raise ValueError("No route found.")

        except Exception as e:
            raise Exception(f"Error while computing path: {e}")

        path = directions_result[0]["legs"][0]
        return path
