from map_objects import *
from non_biased_agent import *
from loss_aversion import *
from overconfidence import *
from bandwagon import *

import mesa
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class HungerGames(mesa.Model):

    def __init__(self, map_file_name):
        super().__init__()
        self.bias_types = {"NBA", "LA", "OC", "BW"}
        self.bias_classes = (NonBiasedAgent, LossAversion, Overconfidence, BandwagonEffect)
        self.spawn_point_radius = 5
        self.initial_energy = 100
        self.initial_number_of_agents_in_a_group = 8
        self.energy_limit_for_reproduction = 150
        self.energy_cost_for_reproduction = 0.75
        self.unknown_cell_gain = 5
        self.unknown_cell_loss = -5
        #self.max_steps = 1500
        self.steps_for_food_regrowth = 10
        self.agent_lifespan = 200
        self.limit_for_overcrowding = 2 # only for bandwagon effect

        self.number_of_agents = 0
        self.generation = 0
        self.amount_of_food = 0
        self.number_of_traps = 0
        self.number_of_deadly_traps = 0
        self.number_of_steps = 0
        self.max_generation = {}
        self.dead_agents = []
        self.regrowing_food = {}
        self.step_in_which_was_the_last_agent_alive = {"NBA": self.number_of_steps, "LA": self.number_of_steps, "OC": self.number_of_steps, "BW": self.number_of_steps}
        self.starvation_deaths = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.trap_deaths = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.fight_deaths = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.old_age_deaths = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.number_of_energy_transfers = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.number_of_initiated_fights = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.fights_won = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.fights_lost = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}
        self.total_number_of_agents_per_group = {"NBA": 0, "LA": 0, "OC": 0, "BW": 0}

        self.spawn_points = {"NBA": (), "LA": (), "OC": (), "BW": ()}
        self.food = set()
        self.traps = set()
        self.deadly_traps = set()
        self.width, self.height = self.initialize_map(map_file_name)
        self.number_of_steps = 0

        self.grid = MultiGrid(self.width, self.height, torus=True)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total Number of Agents": lambda m: m.number_of_agents,
                "Active Agents": lambda m: sum(1 for a in m.agents if getattr(a, "bias_type", None) is not None),

                "Non Biased Agents": lambda m: m.get_number_of_nba_agents(),
                "Total NBA Agents": lambda m: m.total_number_of_agents_per_group["NBA"],
                "Average NBA coefficient": lambda m: m.get_average_nba_coefficient(),
                "Generations NBA": lambda m: max(m.max_generation.get("NBA", {0})) if m.max_generation.get("NBA") else 0,
                "NBA Last Alive in Step": lambda m: m.step_in_which_was_the_last_agent_alive["NBA"],
                "NBA Average Energy": lambda m: sum(a.energy for a in m.agents if getattr(a, "bias_type", None) == "NBA") / max(1, m.get_number_of_nba_agents()),
                "NBA Starvation Deaths": lambda m: m.starvation_deaths["NBA"],
                "NBA Trap Deaths": lambda m: m.trap_deaths["NBA"],
                "NBA Fight Deaths": lambda m: m.fight_deaths["NBA"],
                "NBA Old Age Deaths": lambda m: m.old_age_deaths["NBA"],
                "NBA Number of Energy Transfers": lambda m: m.number_of_energy_transfers["NBA"],
                "NBA Initiated Fights": lambda m: m.number_of_initiated_fights["NBA"],
                "NBA Fights Won": lambda m: m.fights_won["NBA"],
                "NBA Fights Lost": lambda m: m.fights_lost["NBA"],

                "Loss Aversion Agents": lambda m: m.get_number_of_la_agents(),
                "Total LA Agents": lambda m: m.total_number_of_agents_per_group["LA"],
                "Average LA coefficient": lambda m: m.get_average_la_coefficient(),
                "Generations LA": lambda m: max(m.max_generation.get("LA", {0})) if m.max_generation.get("LA") else 0,
                "LA Last Alive in Step": lambda m: m.step_in_which_was_the_last_agent_alive["LA"],
                "LA Average Energy": lambda m: sum(a.energy for a in m.agents if getattr(a, "bias_type", None) == "LA") / max(1,m.get_number_of_la_agents()),
                "LA Starvation Deaths": lambda m: m.starvation_deaths["LA"],
                "LA Trap Deaths": lambda m: m.trap_deaths["LA"],
                "LA Fight Deaths": lambda m: m.fight_deaths["LA"],
                "LA Old Age Deaths": lambda m: m.old_age_deaths["LA"],
                "LA Number of Energy Transfers": lambda m: m.number_of_energy_transfers["LA"],
                "LA Initiated Fights": lambda m: m.number_of_initiated_fights["LA"],
                "LA Fights Won": lambda m: m.fights_won["LA"],
                "LA Fights Lost": lambda m: m.fights_lost["LA"],

                "Overconfidence Agents": lambda m: m.get_number_of_oc_agents(),
                "Total OC Agents": lambda m: m.total_number_of_agents_per_group["OC"],
                "Average OC coefficient": lambda m: m.get_average_oc_coefficient(),
                "Generations OC": lambda m: max(m.max_generation.get("OC", {0})) if m.max_generation.get("OC") else 0,
                "OC Last Alive in Step": lambda m: m.step_in_which_was_the_last_agent_alive["OC"],
                "OC Average Energy": lambda m: sum(a.energy for a in m.agents if getattr(a, "bias_type", None) == "OC") / max(1,m.get_number_of_oc_agents()),
                "OC Starvation Deaths": lambda m: m.starvation_deaths["OC"],
                "OC Trap Deaths": lambda m: m.trap_deaths["OC"],
                "OC Fight Deaths": lambda m: m.fight_deaths["OC"],
                "OC Old Age Deaths": lambda m: m.old_age_deaths["OC"],
                "OC Number of Energy Transfers": lambda m: m.number_of_energy_transfers["OC"],
                "OC Initiated Fights": lambda m: m.number_of_initiated_fights["OC"],
                "OC Fights Won": lambda m: m.fights_won["OC"],
                "OC Fights Lost": lambda m: m.fights_lost["OC"],

                "Bandwagon Effect Agents": lambda m: m.get_number_of_bw_agents(),
                "Total BW Agents": lambda m: m.total_number_of_agents_per_group["BW"],
                "Average BW coefficient": lambda m: m.get_average_bw_coefficient(),
                "Generations BW": lambda m: max(m.max_generation.get("BW", {0})) if m.max_generation.get("BW") else 0,
                "BW Last Alive in Step": lambda m: m.step_in_which_was_the_last_agent_alive["BW"],
                "BW Average Energy": lambda m: sum(a.energy for a in m.agents if getattr(a, "bias_type", None) == "BW") / max(1,m.get_number_of_bw_agents()),
                "BW Starvation Deaths": lambda m: m.starvation_deaths["BW"],
                "BW Trap Deaths": lambda m: m.trap_deaths["BW"],
                "BW Fight Deaths": lambda m: m.fight_deaths["BW"],
                "BW Old Age Deaths": lambda m: m.old_age_deaths["BW"],
                "BW Number of Energy Transfers": lambda m: m.number_of_energy_transfers["BW"],
                "BW Initiated Fights": lambda m: m.number_of_initiated_fights["BW"],
                "BW Fights Won": lambda m: m.fights_won["BW"],
                "BW Fights Lost": lambda m: m.fights_lost["BW"]
            }
        )

        self.initialize_food()
        self.initialize_all_traps()
        self.initialize_agents()

    def initialize_agents(self):
        for bias in self.bias_types:
            for i in range(self.initial_number_of_agents_in_a_group):
                self.create_agent(bias, self.generation)

    def create_agent(self, bias, generation, energy=None, coefficient=None):
        if energy is None:
            energy = self.initial_energy
        spawn_point = self.spawn_points[bias]

        neighboring_cells = self.grid.get_neighborhood(
            spawn_point,
            moore=True,
            include_center=True,
            radius=self.spawn_point_radius
        )

        acceptable_cells = []
        for cell in neighboring_cells:
            cell_contents = self.grid.get_cell_list_contents(cell)

            has_deadly_trap = any(isinstance(obj, (Trap, DeadlyTrap)) for obj in cell_contents)
            has_agent = any(getattr(obj, "bias_type", None) in self.bias_types for obj in cell_contents)

            if not has_deadly_trap and not has_agent:
                acceptable_cells.append(cell)

        if not acceptable_cells:
            print("No space for agent. Creation failed.")
            return

        new_position = self.random.choice(acceptable_cells)

        self.increase_number_of_agents()
        agent_id = self.encode_agent_id(bias, generation, self.number_of_agents)

        if bias not in self.max_generation.keys():
            self.max_generation[bias] = set()
        self.max_generation[bias].add(generation)

        if bias == "NBA":
            agent = NonBiasedAgent(agent_id, self, energy, generation)
            self.grid.place_agent(agent, new_position)
            self.agents.add(agent)
        elif bias == "LA":
            agent = LossAversion(agent_id, self, energy, generation)
            self.grid.place_agent(agent, new_position)
            self.agents.add(agent)
        elif bias == "OC":
            agent = Overconfidence(agent_id, self, energy, generation)
            self.grid.place_agent(agent, new_position)
            self.agents.add(agent)
        elif bias == "BW":
            agent = BandwagonEffect(agent_id, self, energy, generation)
            self.grid.place_agent(agent, new_position)
            self.agents.add(agent)

        if coefficient is not None:
            self.update_coefficient(agent, coefficient)

        self.total_number_of_agents_per_group[bias] += 1

    def initialize_food(self):
        for (x, y) in self.food:
            self.increase_amount_of_food()
            food = Food(f'F_{self.amount_of_food}', self, (x, y))
            self.grid.place_agent(food, (x, y))

    def initialize_all_traps(self):
        for (x, y) in self.traps:
            self.increase_number_of_traps()
            trap = Trap(f'T_{self.number_of_traps}', self)
            self.grid.place_agent(trap, (x, y))

        for (x, y) in self.deadly_traps:
            self.increase_number_of_deadly_traps()
            deadly_trap = DeadlyTrap(f'DT_{self.number_of_deadly_traps}', self)
            self.grid.place_agent(deadly_trap, (x, y))

    def initialize_map(self, map_file_name):
        with (open(map_file_name, "r") as map_file):
            width, height = map(int, map_file.readline().split())
            for y, line in enumerate(map_file):
                row = line.strip().split(" ")
                for x, cell in enumerate(row):
                    if cell in self.spawn_points:
                        self.spawn_points[cell] = (x, y)
                    elif cell == "F":
                        self.food.add((x, y))
                    elif cell == "T":
                        self.traps.add((x, y))
                    elif cell == "D":
                        self.deadly_traps.add((x, y))
        return width, height

    def increase_amount_of_food(self):
        self.amount_of_food += 1

    def increase_number_of_traps(self):
        self.number_of_traps += 1

    def increase_number_of_deadly_traps(self):
        self.number_of_deadly_traps += 1

    def increase_number_of_agents(self):
        self.number_of_agents += 1

    def encode_agent_id(self, agent_type, generation, agent_num):
        return f'{agent_type}_{generation}_{agent_num}'

    def update_step_in_which_was_the_last_agent_alive(self):
        if self.get_number_of_nba_agents() > 0:
            self.step_in_which_was_the_last_agent_alive["NBA"] = self.number_of_steps
        if self.get_number_of_la_agents() > 0:
            self.step_in_which_was_the_last_agent_alive["LA"] = self.number_of_steps
        if self.get_number_of_oc_agents() > 0:
            self.step_in_which_was_the_last_agent_alive["OC"] = self.number_of_steps
        if self.get_number_of_bw_agents() > 0:
            self.step_in_which_was_the_last_agent_alive["BW"] = self.number_of_steps

    def step(self):
        if not self.running:
            return

        self.agents.shuffle_do("step")

        self.check_food_regrowth()

        for dead_agent in self.dead_agents:
            if dead_agent in self.agents:
                self.agents.remove(dead_agent)
        self.dead_agents.clear()

        self.datacollector.collect(self)

        nba = self.get_number_of_nba_agents()
        la = self.get_number_of_la_agents()
        oc = self.get_number_of_oc_agents()
        bw = self.get_number_of_bw_agents()
        active_agents = self.get_number_of_active_agents()

        if active_agents == 0:
            self.running = False
            print()
            print("Active_agents =", active_agents)
            print(f"NBA: {nba} LA: {la} OC: {oc} BW: {bw}")
            print(f"Simulation ended: All agents are dead or {self.max_steps} steps have been reached.")
            print("Steps:", self.number_of_steps)
            print("Number of generations:", self.max_generation)

            average_coefficient = self.get_average_bias_coefficient()
            print(f"Average coefficient: {average_coefficient}")
        else:
            self.number_of_steps += 1
            self.update_step_in_which_was_the_last_agent_alive()

    def get_number_of_nba_agents(self):
        return sum(1 for a in self.agents if getattr(a, "bias_type", None) == "NBA")

    def get_number_of_la_agents(self):
        return sum(1 for a in self.agents if getattr(a, "bias_type", None) == "LA")

    def get_number_of_oc_agents(self):
        return sum(1 for a in self.agents if getattr(a, "bias_type", None) == "OC")

    def get_number_of_bw_agents(self):
        return sum(1 for a in self.agents if getattr(a, "bias_type", None) == "BW")

    def get_number_of_active_agents(self):
        return sum(1 for a in self.agents if isinstance(a, (NonBiasedAgent, LossAversion, Overconfidence, BandwagonEffect)))

    def get_number_of_agents_with_bias(self, bias):
        if bias == "NBA":
            return self.get_number_of_nba_agents()
        if bias == "LA":
            return self.get_number_of_la_agents()
        if bias == "OC":
            return self.get_number_of_oc_agents()
        if bias == "BW":
            return self.get_number_of_bw_agents()

    def get_average_nba_coefficient(self):
        return sum(a.coefficient for a in self.agents if getattr(a, "bias_type", None) == "NBA") / max(1, self.get_number_of_nba_agents())

    def get_average_la_coefficient(self):
        return sum(a.coefficient for a in self.agents if getattr(a, "bias_type", None) == "LA") / max(1, self.get_number_of_la_agents())

    def get_average_oc_coefficient(self):
        return sum(a.coefficient for a in self.agents if getattr(a, "bias_type", None) == "OC") / max(1, self.get_number_of_oc_agents())

    def get_average_bw_coefficient(self):
        return sum(a.coefficient for a in self.agents if getattr(a, "bias_type", None) == "BW") / max(1, self.get_number_of_bw_agents())

    def get_average_bias_coefficient(self):
        return {"NBA": self.get_average_nba_coefficient(), "LA": self.get_average_la_coefficient(), "OC": self.get_average_oc_coefficient(), "BW": self.get_average_bw_coefficient()}

    def is_agent_alive(self, agent):
        if isinstance(agent, (Food, DeadlyTrap, Trap)):
            return

        if agent.pos is None:
            return False

        if (agent.energy <= 0 or agent.age >= self.agent_lifespan) and agent.pos is not None :
            self.grid.remove_agent(agent)
            self.dead_agents.append(agent)
            agent.pos = None
            return False
        return True

    def get_random_coord(self):
        return (self.random.randrange(0, self.width), self.random.randrange(0, self.height))

    def agent_eat(self, agent):
        if agent is None or agent.pos is None:
            return

        cell_contents = self.grid.get_cell_list_contents(agent.pos)

        for obj in cell_contents:
            if isinstance(obj, Food) and obj.active:
                agent.energy += obj.energy
                obj.active = False
                self.regrowing_food[obj] = self.steps_for_food_regrowth + 1
                self.grid.remove_agent(obj)
                self.amount_of_food -= 1
                return

    def check_food_regrowth(self):
        for food in list(self.regrowing_food.keys()):
            self.regrowing_food[food] -= 1

            if self.regrowing_food[food] <= 0:
                food.active = True
                self.grid.place_agent(food, food.cell)
                self.amount_of_food += 1

                del self.regrowing_food[food]

    def check_for_traps(self, agent):
        if agent is None or agent.pos is None:
            return

        cell_contents = self.grid.get_cell_list_contents(agent.pos)

        stepped_on_trap = False

        for obj in cell_contents:
            if isinstance(obj, Trap):
                agent.energy -= obj.energy
                stepped_on_trap = True
            if isinstance(obj, DeadlyTrap):
                agent.energy = 0
                stepped_on_trap = True

        if not self.is_agent_alive(agent):
            if stepped_on_trap:
                self.trap_deaths[agent.bias_type] += 1

    def reproduce(self, agent):
        if agent is None or agent.pos is None:
            return

        if agent.energy >= self.energy_limit_for_reproduction:
            old_energy = agent.energy
            agent.energy = int(old_energy * self.energy_cost_for_reproduction)
            child_energy = old_energy - agent.energy
            coefficient_mutation = self.mutate_coefficient(agent.coefficient)
            self.create_agent(agent.bias_type, agent.generation + 1, child_energy, coefficient=coefficient_mutation)

    def mutate_coefficient(self, coefficient, sigma=0.1, lower_bound=0.0):
        mutation = self.random.gauss(0, sigma)
        new_coefficient = coefficient + mutation
        return max(lower_bound, new_coefficient)

    def fight(self, agent):
        if agent is None or agent.pos is None:
            return

        cell_contents = self.grid.get_cell_list_contents(agent.pos)
        competitors = [a for a in cell_contents if getattr(a, "bias_type", None) is not None and a is not agent and a.bias_type != agent.bias_type]

        if not competitors:
            return

        opponent = self.random.choice(competitors)
        total_energy = agent.energy + opponent.energy
        probability_agent_wins = agent.energy / total_energy if total_energy > 0 else 0.5

        if self.random.random() < probability_agent_wins:
            winner, loser = agent, opponent
        else:
            winner, loser = opponent, agent

        lower_value = int(min(loser.energy, winner.energy) // 4)
        higher_value = int(max(loser.energy, winner.energy) // 4)
        damage = self.random.randint(lower_value, max(lower_value + 1, higher_value))
        loser.energy -= damage
        winner.energy += int(damage * 0.8)

        self.number_of_initiated_fights[agent.bias_type] += 1
        self.fights_won[winner.bias_type] += 1
        self.fights_lost[loser.bias_type] += 1

        self.is_agent_alive(winner)

        if not self.is_agent_alive(loser):
            self.fight_deaths[loser.bias_type] += 1

    def compute_distance(self, pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])

        torus_x = min(dx, self.width - dx)
        torus_y = min(dy, self.height - dy)

        return max(torus_x, torus_y)

    def is_deadly_trap_on_cell(self, cell):
        return any(isinstance(obj, DeadlyTrap) for obj in self.grid.get_cell_list_contents(cell))


    def find_closest_cell(self, pos, possible_steps, return_all_possible_steps=False, without_deadly_traps=False):
        distances = {}

        if not possible_steps:
            return [pos] if return_all_possible_steps else pos

        for cell in possible_steps:
            dist = self.compute_distance(pos, cell)

            if without_deadly_traps:
                if not self.is_deadly_trap_on_cell(cell):
                    if dist not in distances:
                        distances[dist] = []
                    distances[dist].append(cell)
            else:
                if dist not in distances:
                    distances[dist] = []
                distances[dist].append(cell)

        if not distances:
            return [pos] if return_all_possible_steps else pos

        sorted_keys = sorted(distances.keys())
        min_dist = sorted_keys[0]

        if return_all_possible_steps:
            return distances[min_dist]

        return self.random.choice(distances[min_dist])

    def agent_increase_age(self, agent):
        agent.age += 1

    def agent_step(self, agent):
        if not self.is_agent_alive(agent):
            return

        agent.move()

        if not self.is_agent_alive(agent):
            self.starvation_deaths[agent.bias_type] += 1
            return

        self.agent_eat(agent)

        self.check_for_traps(agent)

        if not self.is_agent_alive(agent):
            return

        self.fight(agent)

        if not self.is_agent_alive(agent):
            return

        self.kin_selection(agent)
        agent.reproduce()

        self.agent_increase_age(agent)

        if not self.is_agent_alive(agent):
            self.old_age_deaths[agent.bias_type] += 1
            return

    def is_cell_safe(self, cell, agent):
        cell_contents = self.grid.get_cell_list_contents(cell)

        for obj in cell_contents:
            if isinstance(obj, (DeadlyTrap, Trap)):
                return False
            obj_type = getattr(obj, "bias_type", None)
            if obj_type is not None:
                if agent.bias_type != "OC" and getattr(obj, "bias_type", None) != agent.bias_type:
                    return False
        return True

    def compute_cell_utility(self, cell, agent, optimism_strength=10):
        gain = 0
        loss = 0
        optimism = 0

        for obj in self.grid.get_cell_list_contents(cell):
            if isinstance(obj, DeadlyTrap):
                loss += 1000
            elif isinstance(obj, Trap):
                loss += obj.energy
            elif isinstance(obj, Food):
                gain += obj.energy
            elif getattr(obj, "bias_type", None) is not None and getattr(obj, "bias_type", None) != agent.bias_type:
                lower_value = int(min(agent.energy, obj.energy) // 4)
                higher_value = int(max(agent.energy, obj.energy) // 4)

                if agent.bias_type == "OC":
                    optimism = optimism_strength

                if (agent.energy + optimism) > obj.energy:
                    gain += lower_value
                else:
                    loss += higher_value

        return gain, loss

    def is_object(self, agent):
        if isinstance(agent, (Food, DeadlyTrap, Trap)):
            return True
        return False

    def compute_social_bonus(self, agent, social_bonus=3):
        if self.is_object(agent):
            return

        possible_steps = {}

        strength_of_social_bonus = agent.energy / 100.0

        bw_agents = [a for a in self.agents if getattr(a, "bias_type", None) == agent.bias_type and a.unique_id != agent.unique_id and a.pos is not None]
        neighbors = self.grid.get_neighborhood(
            agent.pos,
            moore=True,
            include_center=False,
            radius=agent.vision
        )

        for ally in bw_agents:
            possible_cells = self.find_closest_cell(ally.pos, neighbors, return_all_possible_steps=True)
            for cell in possible_cells:
                if cell not in possible_steps:
                    possible_steps[cell] = 0
                possible_steps[cell] += social_bonus * strength_of_social_bonus

        return possible_steps

    def overcrowded_cell(self, cell, agent):
        cell_contents = self.grid.get_cell_list_contents(cell)
        count = 0
        for content in cell_contents:
            if getattr(content, "bias_type", None) == agent.bias_type:
                count += 1

        if count >= self.limit_for_overcrowding:
            return True

        return False

    def update_coefficient(self, agent, coefficient):
        if isinstance(agent, NonBiasedAgent):
            return
        agent.coefficient = coefficient

    def kin_selection(self, agent):
        if agent.pos is None:
            return

        cell_contents = self.grid.get_cell_list_contents(agent.pos)
        kin = [a for a in cell_contents if getattr(a, "bias_type", None) == agent.bias_type and a != agent]

        if len(kin) == 0:
            return

        most_starving_agent = kin[0]
        for receiver in kin:
            if receiver.energy < most_starving_agent.energy:
                most_starving_agent = receiver

        self.transfer_energy_between_two_agents(agent, most_starving_agent)

    def transfer_energy_between_two_agents(self, giver, receiver, transfer_coefficient=0.2, min_giver_energy=50, max_receiver_energy=20):
        if min_giver_energy <= giver.energy and receiver.energy <= max_receiver_energy:
            transfer_energy = int(giver.energy * transfer_coefficient)
            giver.energy -= transfer_energy
            receiver.energy += transfer_energy
            self.number_of_energy_transfers[giver.bias_type] += 1