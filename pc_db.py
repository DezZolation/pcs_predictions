import sqlite3
import time
import datetime
import statistics

from dateutil import parser
from enum import Enum

db_file = "pcs.db"
conn = None
try:
    conn = sqlite3.connect(db_file)
except sqlite3.Error as e:
    print(e)
cur = conn.cursor()

race_statistics_cache = {}

def query(q):
    cur.execute(q)
    return cur.fetchall()

def get_races_of_type(stage_type):
    res = query("""
            SELECT slug FROM races
            WHERE stage_type = '%s'
        """ % stage_type)
    slugs = [row[0] for row in res]
    return slugs

def get_statistics_for_race(slug):
    if slug in race_statistics_cache:
        return race_statistics_cache[slug]

    res = query("""
        SELECT (distance / stage_time * 3600) AS speed FROM results INNER JOIN races ON results.race = races.slug
        WHERE race = '%s'
    """ % slug)
    times = [row[0] for row in res if isinstance(row[0], float)]
    stage_mean = statistics.mean(times)
    std = statistics.pstdev(times)
    race_statistics_cache[slug] = (stage_mean, std)
    return race_statistics_cache[slug]

def get_date_of_race(slug):
    res = query("""
        SELECT date FROM races WHERE slug = '%s'
    """ % slug)
    return res[0][0]

def get_riders_of_race(slug):
    res = query("""
        SELECT rider FROM results WHERE race = '%s' AND stage_rank not null ORDER BY stage_rank
    """ % slug)
    return [row[0] for row in res]


# Time trials with differences from winner in seconds
# SELECT race, (distance/stage_time*3600) AS average_speed, stage_time, stage_rank, difficulty, distance, profile,
# stage_time - (SELECT stage_time FROM results WHERE race = slug AND stage_rank = 1) as time_difference_from_winner
# FROM races INNER JOIN results ON races.slug = results.race WHERE rider = "tom-dumoulin" AND stage_type = "ITT" ORDER BY stage_rank


# !!!
#     SELECT race, stage_time, 
# (SELECT COUNT(rider) FROM results AS r2 WHERE r1.race = r2.race AND r1.stage_time = r2.stage_time ) 
# FROM results AS r1 WHERE stage_rank = 1 LIMIT 100  

# class StageType(Enum):
#     ITT = "stage_type = 'ITT'"
#     TTT = "stage_type = 'TTT'"
#     SPRINT = "stage_type = 'REGULAR' AND "

def rider_race_query(rider, stage_type, rank_cutoff = 999, date_cutoff = '2030-12-31'):
    res = query("""
            SELECT race, (distance / stage_time * 3600) AS speed, date FROM results INNER JOIN races ON results.race = races.slug 
            WHERE rider = '%s' AND stage_type = '%s' AND stage_rank <= %d AND date < '%s' ORDER BY date
        """ % (rider, stage_type, rank_cutoff, date_cutoff))
    return res

def date_result_query(rider, stage_type, rank_cutoff = 999, season_cutoff = 2000):
    res = query("""
            SELECT date, stage_rank FROM results INNER JOIN races ON results.race = races.slug 
            WHERE rider = '%s' AND stage_type = '%s' AND stage_rank <= %d AND season >= %d ORDER BY date
        """ % (rider, stage_type, rank_cutoff, season_cutoff))
    dates = [parser.parse(row[0]) for row in res]
    ranks = [row[1] for row in res]
    return (dates, ranks)

def get_sprints():
    res = query("""
            SELECT * FROM results INNER JOIN races ON results.race = races.slug
            WHERE
        """)
    return res

# def effort_ratio_query(rider, stage_type, rank_cutoff = 20, season_cutoff = 2000):
#     res = query("""
#             SELECT COUNT(*) FROM results INNER JOIN races ON results.race = races.slug 
#             WHERE rider = '%s' AND stage_type = '%s' AND stage_rank <= %d AND season >= %d ORDER BY date
#         """ % (rider, stage_type, rank_cutoff, season_cutoff))
#     return

# def comparative_result_query(riders, stage_type, season_cutoff = 2000):
#     rider_sub_queries = []
#     for rider in riders:
#         rider_sub_queries.append("SELECT race, stage_rank FROM results WHERE rider = '%s")
#     res = query("""
#             SELECT date, t1.stage_rank, t2.stage_rank 
#             FROM %s t1 INNER JOIN %s t2 ON t1.race = t2.race
#             INNER JOIN (SELECT * FROM races WHERE stage_type = '%s' AND season >= %d) races ON t1.race = races.slug
#             ORDER BY date
#         """ % (*rider_sub_queries, stage_type, season_cutoff))
#     dates = [parser.parse(row[0]) for row in res]
#     ranks


# comparative_results = query("""
# SELECT t1.race, races.date, t1.stage_rank AS rider1, t2.stage_rank AS rider2 
# FROM (SELECT race, stage_rank FROM results WHERE rider = '%s') t1 
# INNER JOIN (SELECT race, stage_rank FROM results WHERE rider = '%s') t2 
# ON t1.race = t2.race INNER JOIN (SELECT * FROM races WHERE stage_type = 'ITT') races ON t1.race = races.slug ORDER BY date
# """ % (riders[0], riders[1]))