class Converter:
    # Conversion factors to meters
    conversion_factors = {
        "inches": 0.0254,
        "feet": 0.3048,
        "yards": 0.9144,
        "miles": 1609.344,
        "kilometers": 1000,
        "meters": 1,
        "centimeters": 0.01,
        "millimeters": 0.001,
    }

    def __init__(self, length: float, unit: str) -> None:
        self.length_in_meters = length * self.conversion_factors[unit.lower()]

    def inches(self) -> float:
        return self.length_in_meters / self.conversion_factors["inches"]

    def feet(self) -> float:
        return self.length_in_meters / self.conversion_factors["feet"]

    def yards(self) -> float:
        return self.length_in_meters / self.conversion_factors["yards"]

    def miles(self) -> float:
        return self.length_in_meters / self.conversion_factors["miles"]

    def kilometers(self) -> float:
        return self.length_in_meters / self.conversion_factors["kilometers"]
    
    def meters(self) -> float:
        return self.length_in_meters / self.conversion_factors["meters"]

    def centimeters(self) -> float:
        return self.length_in_meters / self.conversion_factors["centimeters"]

    def millimeters(self) -> float:
        return self.length_in_meters / self.conversion_factors["millimeters"]


def main():
    pass


if __name__ == "__main__":
    main()
