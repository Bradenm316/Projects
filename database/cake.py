class Cake:
    def __init__(self):
        self.flavors = []
        self.toppings = []
        self.fillings = []

    def add_flavor(self, flavor):
        self.flavors.append(flavor)

    def add_topping(self, topping):
        self.toppings.append(topping)

    def add_filling(self, filling):
        self.fillings.append(filling)

    def get_flavors(self):
        return self.flavors

    def get_toppings(self):
        return self.toppings

    def get_fillings(self):
        return self.fillings
