import datetime

from freezegun import freeze_time

from src.Service.JWTService import JwtService

jwt_service = JwtService("mysecret")


@freeze_time("2024-08-26 12:00:00")
def test_encode_jwt():
    user_id = "myUser"
    jwtResponse = jwt_service.encode_jwt(user_id=user_id)
    assert (
        jwtResponse.access_token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibXlVc2VyIiwiZXhwaXJ5X3RpbWVzdGFtcCI6MTcyNDY3NDIwMC4wfQ.eUjNbpMCDNuPESsMHF2dpeRlDl6fMJmjUWsHSZT_n1Q"  # noqa: E501
    )


@freeze_time("2024-08-26 12:00:00")
def test_decode_jwt():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibXlVc2VyIiwiZXhwaXJ5X3RpbWVzdGFtcCI6MTcyNDY3NDIwMC4wfQ.eUjNbpMCDNuPESsMHF2dpeRlDl6fMJmjUWsHSZT_n1Q"  # noqa: E501
    decoded_jwt = jwt_service.decode_jwt(jwt)
    assert decoded_jwt.get("user_id") == "myUser"
    assert datetime.datetime.fromtimestamp(
        decoded_jwt.get("expiry_timestamp")
    ) == datetime.datetime.fromisoformat("2024-08-26 12:10:00")
