import mesa
import pandas as pd
from model import HungerGames

params = {
    "map_file_name": "final_map.txt",
}

print("Starting batch run...")

results = mesa.batch_run(
    HungerGames,
    parameters=params,
    iterations=50,
    max_steps=1999,
    data_collection_period=1,  #1 kazdy krok simulacie, -1 len posledny krok
    display_progress=True
)

df = pd.DataFrame(results)

df.to_csv("results.csv", index=False)
print("Batch run complete! Data saved to hunger_games_results.csv")