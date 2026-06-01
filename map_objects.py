import mesa

class Food(mesa.Agent):
    def __init__(self, unique_id, model, cell, energy=10):
        super().__init__(model)
        self.unique_id = unique_id
        self.type = "food"
        self.energy = energy
        self.active = True
        self.cell = cell


    def __str__(self):
        return ' '.join([
            "id:", str(self.unique_id),
            "energy:", str(self.energy)
        ])

class DeadlyTrap(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(model)
        self.unique_id = unique_id
        self.type = "deadly_trap"

    def __str__(self):
        return ' '.join([
            "id:", str(self.unique_id)
        ])

class Trap(mesa.Agent):
    def __init__(self, unique_id, model, energy=20):
        super().__init__(model)
        self.unique_id = unique_id
        self.type = "trap"
        self.energy = energy

    def __str__(self):
        return ' '.join([
            "id:", str(self.unique_id),
            "energy:", str(self.energy)
        ])