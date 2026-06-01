import mesa
from map_objects import *

class LossAversion(mesa.Agent):

    def __init__(self, unique_id, model, energy, generation, vision=1, partial_vision=2, uncertain_vision=3, coefficient=2.0):
        super().__init__(model)
        self.unique_id = unique_id
        self.energy = energy
        self.generation = generation
        self.vision = vision
        self.partial_vision = partial_vision
        self.uncertain_vision = uncertain_vision
        self.coefficient = coefficient
        self.age = 0
        self.bias_type = "LA"

    def __str__(self):
        return ' '.join([
            "id:", str(self.unique_id),
            "pos:", str(self.pos),
            "energy:", str(self.energy),
            "gen:", str(self.generation),
            "coef:", str(self.coefficient)
        ])

    def step(self):
        self.model.agent_step(self)

    def move(self):
        if self.pos is None:
            return

        neighboring_cells = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.uncertain_vision
        )

        acceptable_cells = {}
        step = []

        for cell in neighboring_cells:
            distance = self.model.compute_distance(self.pos, cell)

            if distance <= self.vision:
                gain, loss = self.model.compute_cell_utility(cell, self)
                utility = gain - (loss * self.coefficient)
                if utility > - self.energy:
                    step.append(cell)
            elif distance <= self.partial_vision:
                if self.model.is_cell_safe(cell, self):
                    utility = self.model.unknown_cell_gain
                else:
                    utility = self.model.unknown_cell_loss * self.coefficient
            else:
                utility = self.model.unknown_cell_loss * self.coefficient * 2

            if utility > -self.energy:
                if utility not in acceptable_cells:
                    acceptable_cells[utility] = []
                acceptable_cells[utility].append(cell)

        if not acceptable_cells or not step:
            self.energy -= 1
            return

        sorted_utilities = sorted(acceptable_cells.keys(), reverse=True)
        best_utility = sorted_utilities[0]

        destination = self.model.random.choice(acceptable_cells[best_utility])

        if destination in step:
            new_position = destination
        else:
            new_position = self.model.find_closest_cell(destination, step)

        self.energy -= 1
        self.model.grid.move_agent(self, new_position)

    def reproduce(self):
        self.model.reproduce(self)