import math
import os
from datetime import datetime
from typing import Dict, Optional, Union

import googlemaps

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

    def __init__(self) -> None:
        self.__gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])
        self.ensai_address = "51 Rue Blaise Pascal, 35170 Bruz, France"

        ensai_geocode = self.__gmaps.geocode(self.ensai_address)
        self.coord_ensai = ensai_geocode[0]["geometry"]["location"]

        self.coord_rennes = (48.137922, -1.632842)
        self.radius = math.sqrt(
            (self.coord_rennes[0] - self.coord_ensai["lat"]) ** 2
            + (self.coord_rennes[1] - self.coord_ensai["lng"]) ** 2
        )

    @log
    def validate_address(self, address: str) -> bool:
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

        if len(result) == 0:
            raise ValueError("[GoogleMapService]: Invalid address.")

        fields = ["route", "street_number", "locality", "postal_code", "country"]
        components_types = [component["types"] for component in result[0]["address_components"]]
        components_types_flat = [
            component for components in components_types for component in components
        ]
        for field in fields:
            if field not in components_types_flat:
                raise ValueError("[GoogleMapService]: Address not found.")

        coord_address = result[0]["geometry"]["location"]

        if (coord_address["lat"] - self.coord_ensai["lat"]) ** 2 + (
            coord_address["lng"] - self.coord_ensai["lng"]
        ) ** 2 > self.radius**2:
            raise ValueError("[GoogleMapService]: Destination is too far away.")

        return True

    @log
    def extract_components(self, address: str) -> Dict[str, Union[str, int]]:
        """
        _summary_

        Parameters
        ----------
        address : str
            a complete address as a single string

        Returns
        -------
        Dict[str, Union[str, int]]
            _description_
        """
        result = self.__gmaps.geocode(address)

        number = street = city = postal_code = country = None

        for component in result[0]["address_components"]:
            if "route" in component["types"]:
                street = component["long_name"]

            if "street_number" in component["types"]:
                number = component["long_name"]

            if "locality" in component["types"]:
                city = component["long_name"]

            if "postal_code" in component["types"]:
                postal_code = component["long_name"]

            if "country" in component["types"]:
                country = component["long_name"]

        return {
            "address_number": int(number),
            "address_street": street,
            "address_city": city,
            "address_postal_code": int(postal_code),
            "address_country": country,
        }

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
            raise Exception(f"Error while computing path: {e}") from e

        path = directions_result[0]["legs"][0]
        return path
