'''
Štruktúra:
    -   prvy riadok širka, výška mapy - oddelené medzerou
    -   rozloženie pascí, jedla, ...

Hint:
    - . - empty tile
    - F - food
    - D - deadly trap
    - T - trap, doesn't necessarily kills an agent
    - [code of the bias/agent type] - spawn area for agents with certain bias
        -   NBA - non biased agent
        -   LA - loss aversion
        -   OC - overconfidence
        -   BW - bandwagon effect
'''

import random

class MapGenerator:

    def __init__(self):
        self.width = 50
        self.height = 50

        self.spawn_points = {(12, 12): "NBA", (12, 37): "LA", (37, 12): "OC", (37 ,37): "BW"}
        self.safe_zones = []
        self.all_oasis = []

        self.oasis_coords = [
            [(0,0), (5,5), (44, 0), (49, 5), (0, 44), (5, 49), (44, 44), (49, 49)],
            [(0, 19), (5, 30), (44, 19), (49, 30)],
            [(19, 0), (30, 5), (19, 44), (30, 49)],
            [(19, 19), (30, 30)]
        ]

        self.amount_of_cells = self.width * self.height
        self.amount_of_food = 0.1
        self.amount_of_traps = 0.05
        self.amount_of_deadly_traps = 0.01

        self.safe_zones_amount_of_objects = 0.1
        self.middle_zones_amount_of_objects = 0.3
        self.oasis_amount_of_objects = 0.6

        self.food = set()
        self.traps = set()
        self.deadly_traps = set()
        self.spawn_point_radius = 5
        self.occupied_coords = {(12, 12), (12, 37), (37, 12), (37, 37)}

    def get_random_coord(self):
        return (random.randrange(0, self.width), random.randrange(0, self.height))

    def get_neighborhood(self, coord):
        neighborhood = set()
        for dx in range(-self.spawn_point_radius, self.spawn_point_radius + 1):
            for dy in range(-self.spawn_point_radius, self.spawn_point_radius + 1):
                x = coord[0] + dx
                y = coord[1] + dy
                if 0 <= x < self.width and 0 <= y < self.height and (x, y) != coord:
                    neighborhood.add((x, y))
        return neighborhood

    def get_not_middle_zone_cells(self):
        not_middle = set()
        for safe_zone in self.safe_zones:
            for cell in safe_zone:
                not_middle.add(cell)
        for oasis in self.all_oasis:
            for cell in oasis:
                not_middle.add(cell)
        return not_middle

    def get_all_cells(self):
        cells = set()
        for i in range(self.width):
            for j in range(self.height):
                cells.add((i, j))
        return cells

    def get_middle_zone_cells(self):
        return self.get_all_cells().difference(self.get_not_middle_zone_cells())

    def get_safe_zones(self):
        for spawn_point in self.spawn_points.keys():
            self.safe_zones.append(self.get_neighborhood(spawn_point))

    def get_zone(self, top_left, bottom_right):
        cells = set()
        for x in range(top_left[0], bottom_right[0] + 1):
            for y in range(top_left[1], bottom_right[1] + 1):
                cells.add((x, y))
        return cells

    def get_oasis(self):
        for zone in self.oasis_coords:
            oasis = set()
            for i in range(0, len(zone), 2):
                cells = self.get_zone(zone[i], zone[i + 1])
                oasis = oasis.union(cells)
            self.all_oasis.append(oasis)

    def compute_object_cells(self):
        all_cells = self.width * self.height
        food_cells = all_cells * self.amount_of_food
        traps_cells = all_cells * self.amount_of_traps
        deadly_traps_cells = all_cells * self.amount_of_deadly_traps
        return food_cells, traps_cells, deadly_traps_cells

    def coord_is_acceptable(self, coord):
        return coord not in self.spawn_points.keys() and coord not in self.food and coord not in self.traps and coord not in self.deadly_traps

    def compute_object_cells_for_safe_zones(self, food_cells):
        food_cells_in_one_zone = int(food_cells * self.safe_zones_amount_of_objects / len(self.safe_zones))

        for i, safe_zone in enumerate(self.safe_zones):
            while len(self.food) < food_cells_in_one_zone * (i + 1):
                coord = random.choice(list(safe_zone))
                if coord not in self.occupied_coords:
                    self.food.add(coord)
                    self.occupied_coords.add(coord)

    def compute_cells_for_oasis(self, food_cells, trap_cells, deadly_traps_cells):
        food_cells_in_one_zone = int(food_cells * self.oasis_amount_of_objects / len(self.all_oasis))
        trap_cells_in_one_zone = int(trap_cells * self.oasis_amount_of_objects / len(self.all_oasis))
        deadly_traps_cells_in_one_zone = int(deadly_traps_cells / len(self.all_oasis))

        oasis_food = set()
        oasis_traps = set()
        oasis_deadly_traps = set()

        for i, one_oasis in enumerate(self.all_oasis):
            while len(oasis_food) < food_cells_in_one_zone * (i + 1):
                coord = random.choice(list(one_oasis))
                if coord not in self.occupied_coords:
                    oasis_food.add(coord)
                    self.occupied_coords.add(coord)

            while len(oasis_traps) < trap_cells_in_one_zone * (i + 1):
                coord = random.choice(list(one_oasis))
                if coord not in self.occupied_coords:
                    oasis_traps.add(coord)
                    self.occupied_coords.add(coord)

            while len(oasis_deadly_traps) < deadly_traps_cells_in_one_zone * (i + 1):
                coord = random.choice(list(one_oasis))
                if coord not in self.occupied_coords:
                    oasis_deadly_traps.add(coord)
                    self.occupied_coords.add(coord)

        self.food = self.food.union(oasis_food)
        self.traps = self.traps.union(oasis_traps)
        self.deadly_traps = self.deadly_traps.union(oasis_deadly_traps)

    def compute_cells_for_middle_zones(self):
        middle_zone_cells = self.get_middle_zone_cells()

        while len(self.food) < self.amount_of_cells * self.amount_of_food:
            coord = random.choice(list(middle_zone_cells))
            if coord not in self.occupied_coords:
                self.food.add(coord)
                self.occupied_coords.add(coord)

        while len(self.traps) < self.amount_of_cells * self.amount_of_traps:
            coord = random.choice(list(middle_zone_cells))
            if coord not in self.occupied_coords:
                self.traps.add(coord)
                self.occupied_coords.add(coord)

    def create_map(self):
        self.get_safe_zones()
        self.get_oasis()

        food_cells, trap_cells, deadly_traps_cells = self.compute_object_cells()
        self.compute_object_cells_for_safe_zones(food_cells)
        self.compute_cells_for_oasis(food_cells, trap_cells, deadly_traps_cells)
        self.compute_cells_for_middle_zones()

        map_data = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) in self.spawn_points.keys():
                    row.append(self.spawn_points[(x, y)])
                elif (x, y) in self.food:
                    row.append("F")
                elif (x, y) in self.traps:
                    row.append("T")
                elif (x, y) in self.deadly_traps:
                    row.append("D")
                else:
                    row.append(".")
            map_data.append(row)
        return map_data

    def write_map_to_file(self):
        current_map = self.create_map()
        with open("map.txt", "w") as f:
            f.write(f'{self.width} {self.height}\n')
            for row in current_map:
                f.write(" ".join(row) + "\n")
        print(f"Expected food: {self.amount_of_cells * self.amount_of_food}, real food: {len(self.food)}")
        print(f"Expected traps: {self.amount_of_cells * self.amount_of_traps}, real traps: {len(self.traps)}")
        print(f"Expected deadly traps: {self.amount_of_cells * self.amount_of_deadly_traps}, real deadly traps: {len(self.deadly_traps)}")

mapa = MapGenerator()
mapa.create_map()
mapa.write_map_to_file()