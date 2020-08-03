import pc_db as db
from pc_race import load
from dateutil import parser
import numpy as np

import matplotlib.pyplot as plt

stage_points = [
    50,
    44,
    40,
    36,
    32,
    30,
    28,
    26,
    24,
    22,
    20,
    18,
    16,
    14,
    12,
    10,
    8,
    6,
    4,
    2
]

def std_difference(mean, std, x):
    return (x - mean) / std

def get_rider_itt_score_graph(rider, date_cutoff = '2030-12-31'):
    races = db.rider_race_query(rider, 'ITT', 999, date_cutoff)
    dates = []
    scores = []
    for race, speed, date in races:
        mean, std = db.get_statistics_for_race(race)
        dates.append(parser.parse(date))
        scores.append(std_difference(mean, std, speed))
    return (dates, scores)

def get_rider_itt_score(rider, date_cutoff = '2030-12-31'):
    _, scores = get_rider_itt_score_graph(rider, date_cutoff)
    if len(scores) == 0:
        return 0
    weights = np.linspace(1, len(scores) + 1, len(scores))
    return np.average(scores, None, weights)

def sort_dict_by_values(dicty):
    return {k: v for k, v in sorted(dicty.items(), key=lambda item: item[1])}

def predict_race(slug):
    riders = db.get_riders_of_race(slug)
    date = db.get_date_of_race(slug)
    rider_scores = {}
    for rider in riders:
        rider_scores[rider] = get_rider_itt_score(rider, date)
    best_riders = list(reversed(list(sort_dict_by_values(rider_scores).keys())))[:20]
    total_points = 0
    for rider in best_riders:
        if rider in riders[:20]:
            total_points += stage_points[riders.index(rider)]
    print(best_riders)
    print("Total points: %d" % total_points)

# predict_race('vuelta-a-espana/2019/stage-10')

# get_rider_itt_score_graph('tom-dumoulin')
# mean, std = db.get_statistics_for_race("tour-de-france/2019/stage-13")
# mean, std = db.get_statistics_for_race("tour-de-france/2019/stage-13")
# print(mean)
# print(std)
# for rider in riders:
#     plt.plot(*db.date_result_query(rider, 'REGULAR', 10, 2019), label = rider)

# for rider in riders:
#     dates, scores = get_rider_itt_score_graph(rider)
#     plt.plot(dates, scores, label = rider)
#     weights = np.arange(1, len(scores) + 1, 1)
#     print(weights)
#     print(len(weights))
#     print(len(scores))
#     print("%s average score: %f" % (rider, )



dates, scores = get_rider_itt_score_graph('nathan-van-hooydonck')
plt.plot(dates, scores)
plt.legend(loc="upper left")
plt.show()