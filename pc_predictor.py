import pc_db as db
from pc_race import load

import matplotlib.pyplot as plt

race = load("race.json")
riders = race['riders']

for rider in riders:
    plt.plot(*db.date_result_query(rider, 'REGULAR', 10, 2018), label = rider)

plt.legend(loc="upper left")
plt.show()