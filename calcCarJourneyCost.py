# calculate the carbon cost of a car journey
def calcCarJourneyCost(distance=0, emissionsPerMile=0, passengers=1):
    # distance: distance in metres
    # emissionsPerMile: how much carbon released per mile driven in vehicle
    distance = distance / 1000
    emissionsPerKm = emissionsPerMile * 1.609

    return (emissionsPerKm * distance) / passengers

calcCarJourneyCost()


