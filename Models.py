class Task:
    def __init__(userId, taskId, carbonCost, taskType):
        self.userId = userId
        self.taskId = taskId
        self.taskType = taskType
        self.carbonCost = carbonCost


class Journey(Task):
    def __init__(self, taskId, carbonCost, taskType, origin, destination, journeyType, distance):
        super().__init__(taskId, carbonCost, taskType)
        self.origin = origin
        self.destination = destination
        self.journeyType = journeyType
        self.distance = distance


class BikeJourney(Journey):
    def __init__(self, taskId, carbonCost, taskType, origin, destination, journeyType, distance, isElectric):
        super().__init__(taskId, carbonCost, taskType, origin, destination, journeyType, distance)
        self.isElectric = isElectric


class CarJourney(Journey):
    def __init__(self, taskId, carbonCost, taskType, origin, destination, journeyType, distance, carMake, carModel,
                 passengers, carId):
        super().__init__(taskId, carbonCost, taskType, origin, destination, journeyType, distance)
        self.carMake = carMake
        self.carModel = carModel
        self.passengers = passengers
        self.carId = carId


class WalkingJourney(Journey):
    def __init__(self, taskId, carbonCost, taskType, origin, destination, journeyType, distance):
        super().__init__(taskId, carbonCost, taskType, origin, destination, journeyType, distance)
