#!/usr/bin/env python3
"""Grouping competitors with the date of the competition 
they competed in with the best solve they've had as of that date. 
"""
from numpy import nan
import pandas as pd

results = pd.read_table("WCA_export_results.tsv")
competitions = pd.read_table("WCA_export_competitions.tsv")

# Dropping irrelevant columns from the results table
result_cols = {
    "columns": [
        "personCountryId",
        "pos", "formatId",
        "roundTypeId",
        "regionalSingleRecord",
        "regionalAverageRecord"
    ]
}

results_replace = {
    "best": {0: nan, -1: nan},
    "average": {0: nan, -1: nan}
}

results = results.drop(**result_cols)
results.replace(results_replace, inplace=True)
results = results[col for col in results.columns if col[0] != "v"]

# Renaming to convert endDate and endDay columns
# to datetime and renaming id for joining with results
dates = ["year", "month", "day"]
rename_comp_cols = {
    "columns": {
        "id": "competitionId",
        "endMonth": "month",
        "endDay": "day"
    }
}

drop_comp_cols = {
    "columns": ("month", "day")
}

# Modifying competition dataframe to combine with results dataframe
competitions = competitions.drop(**drop_comp_cols)
competitions.rename(**rename_comp_cols, inplace=True)

competitions["date"] = pd.to_datetime(competitions[dates])
competitions = competitions[["competitionId", "date"]]

comp_results = pd.merge(competitions, results, on="competitionId")

# Aggregating best solves per competition by person, event, and
# date of the competition, sorting by initial date, saving to csv
best = comp_results.groupby(["personId", "eventId", "date", "competitionId"]).min("best")
best = best.reset_index().sort_values(by="date")
best.to_csv(f"persons_best_by_dates_competed.csv")

avg = comp_results.groupby(["personId", "eventId", "date", "competitionId"]).min("average")
avg = avg.reset_index().sort_values(by="date")
avg.to_csv(f"persons_best_average_by_dates_competed_.csv")
