import random

class Car:
    # Constructor method to initialize the Car object
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0  # Default mileage is 0 when the car is new
        self.Q = {}     ## Initiate Q table

    # Method to drive the car and increase the mileage
    def drive(self, miles):
        self.mileage += miles
        print(f"You drove {miles} miles. Total mileage is now {self.mileage} miles.")

    def get_Q(self, state, action):
        1==1        

        print("action = ", action)
        print("state = ", state)

        if (state, action) in self.Q:
            print("self.Q[(state, action)]", self.Q[(state, action)])
        else:
            self.Q[(state, action)] = random.uniform(0, 1)         
            print("No self.Q[(state, action)]")
            print("self.Q[(state, action)] = ", self.Q[(state, action)])

    def play(self):
        state = 1
        action = 5
        self.Q[(state, action)] = 5

        self.get_Q(state, 4)

        i = 1
        while i < 6:
            i += 1
            print(i)
            if i == 3:
                break
        

    # Method to display information about the car
    def display_info(self):
        print(f"{self.year} {self.brand} {self.model}. Mileage: {self.mileage} miles.")

# Create an instance of the Car class
my_car = Car("Toyota", "Camry", 2022)

# Display information about the car
my_car.display_info()

# Drive the car for 100 miles
my_car.drive(100)

my_car.play()

# Display updated information about the car
my_car.display_info()
