import solara
from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from model import HungerGames
from map_objects import *

file = "final_map.txt"

nba_color = "blue"
la_color = "gray"
oc_color = "orange"
bw_color = "pink"

def agent_portrayal(agent):
    portrayal = {"color": "gray", "marker": "o", "size": 30}

    if isinstance(agent, Food):
        portrayal.update({"color": "green", "marker": "s", "size": 20})
    elif isinstance(agent, Trap):
        portrayal.update({"color": "orange", "marker": "x", "size": 20})
    elif isinstance(agent, DeadlyTrap):
        portrayal.update({"color": "red", "marker": "d", "size": 20})

    elif getattr(agent, "bias_type", None) == "NBA":
        portrayal.update({"color": nba_color})
    elif getattr(agent, "bias_type", None) == "LA":
        portrayal.update({"color": la_color})
    elif getattr(agent, "bias_type", None) == "OC":
        portrayal.update({"color": oc_color})
    elif getattr(agent, "bias_type", None) == "BW":
        portrayal.update({"color": bw_color})
    return portrayal

model_params = {
    "map_file_name": file,
}

model_instance = HungerGames(map_file_name=file)

space_component = make_space_component(agent_portrayal)

plot_population = make_plot_component({
    "Total Number of Agents": "black",
    "Non Biased Agents": nba_color,
    "Loss Aversion Agents": la_color,
    "Overconfidence Agents": oc_color,
    "Bandwagon Effect Agents": bw_color
    })

plot_generations = make_plot_component({
    "Generations NBA": nba_color,
    "Generations LA": la_color,
    "Generations OC": oc_color,
    "Generations BW": bw_color
})

plot_energy = make_plot_component({
    "NBA Average Energy": nba_color,
    "LA Average Energy": la_color,
    "OC Average Energy": oc_color,
    "BW Average Energy": bw_color
})

plot_coefficients = make_plot_component({
    "Average LA coefficient": la_color,
    "Average OC coefficient": oc_color,
    "Average BW coefficient": bw_color
})

page = SolaraViz(
    model_instance,
    components=[
        space_component,
        plot_population,
        plot_generations,
        plot_coefficients,
        plot_energy
    ],
    model_params=model_params,
    name="Evolutionary explanations of cognitive biases"
)

# solara run visualization.py