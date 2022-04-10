class InvalidLatitude(ValueError):
    def __str__(self) -> str:
        return "Invalid value for latitude accepted values are > -90 and < 90"


class InvalidLongitude(ValueError):
    def __str__(self) -> str:
        return (
            "Invalid value for longitude accepted values are > -180 and < 180"
        )


class EmptyFile(Exception):
    def __str__(self) -> str:
        return "Empty file or content invalid."
