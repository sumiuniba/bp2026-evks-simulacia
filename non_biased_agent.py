import mesa
from map_objects import *

class NonBiasedAgent(mesa.Agent):

    def __init__(self, unique_id, model, energy, generation, vision=1, partial_vision=2, uncertain_vision=3, coefficient=1.0):
        super().__init__(model)
        self.unique_id = unique_id
        self.energy = energy
        self.generation = generation
        self.vision = vision
        self.partial_vision = partial_vision
        self.uncertain_vision = uncertain_vision
        self.coefficient = coefficient
        self.age = 0
        self.bias_type = "NBA"

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

        acceptable_cells = []
        step = []

        for cell in neighboring_cells:
            cell_contents = self.model.grid.get_cell_list_contents(cell)
            distance = self.model.compute_distance(self.pos, cell)

            if distance == 1:
                has_deadly_trap = any(isinstance(obj, DeadlyTrap) for obj in cell_contents)
                if not has_deadly_trap:
                    acceptable_cells.append(cell)
                    step.append(cell)
            else:
                acceptable_cells.append(cell)

        if not acceptable_cells or not step:
            self.energy -= 1
            return

        destination = self.random.choice(acceptable_cells)

        if destination in step:
            new_position = destination
        else:
            new_position = self.model.find_closest_cell(destination, step, without_deadly_traps=True)

        self.energy -= 1
        self.model.grid.move_agent(self, new_position)

    def reproduce(self):
        self.model.reproduce(self)