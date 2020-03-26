# calculate the carbon cost of a bike journey
def calcBikeJourneyCost(distance, isElectric):
    # isElectric: Boolean to determine if bike is electric or not
    # distance: distance of journey in metres
    distance = distance / 1000
    if isElectric:
        # https://wsd-pfb-sparkinfluence.s3.amazonaws.com/uploads/2019/05/E-bike-Potential-Paper-05_15_19-Final.pdf
        # where data on emissions / km come from
        return distance * 7.89

    else:
        # argument to be made about the carbon cost of producing bike AND energy cost of food
        return 0
