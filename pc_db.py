import sqlite3
import time
import datetime

from dateutil import parser

db_file = "pcs.db"
conn = None
try:
    conn = sqlite3.connect(db_file)
except sqlite3.Error as e:
    print(e)
cur = conn.cursor()

def query(q):
    cur.execute(q)
    return cur.fetchall()

def date_result_query(rider, stage_type, rank_cutoff = 999, season_cutoff = 2000):
    res = query("""
            SELECT date, stage_rank FROM results INNER JOIN races ON results.race = races.slug 
            WHERE rider = '%s' AND stage_type = '%s' AND stage_rank <= %d AND season >= %d ORDER BY date
        """ % (rider, stage_type, rank_cutoff, season_cutoff))
    dates = [parser.parse(row[0]) for row in res]
    ranks = [row[1] for row in res]
    return (dates, ranks)

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