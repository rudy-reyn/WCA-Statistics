#!/usr/bin/env python3
#
"""Note: This is the original work that's been moved into two seperate files.


Get a persons rank on each day they competed and for each event
   
they've ever competed in, by best solve times and by average solve times.
Make sure you have the competitions dataset and the results dataset
in the same working directory when running this. I'm thinking some more
work could be done to prevent having to do so much work for each iteration.
"""
import numpy as np
import pandas as pd


personId = input("personId: ")
all_events = input("All events? (yes/y, no/n): ")
agg = input("Aggregation? (best/b, average/a): ")

def find_rank(df, personId, as_of, agg) -> "DataFrame":
    """Find a person rank on a pre specified date"""
    filtered = df.loc[
                df.date <= as_of
                ].groupby("personId").min(agg
                ).sort_values(by="best").reset_index()
    # Player's current ranking is their index position
    filtered["rank"] = filtered.index + 1
    person_ranking   = filtered.loc[filtered.personId == personId]
    person_ranking.insert(0, "date", as_of)
    return person_ranking


def get_person_attributes(df, personId) -> dict:
    """Get all events and competition dates for a competitor"""
    filtered = df.loc[df.personId == personId]
    events_competed = list(filtered.eventId.unique())
    dates_competed = list(filtered.date.unique())
    person_attributes = {"events_competed": events_competed, 
                         "dates_competed": dates_competed}
    return person_attributes


def get_person_ranks(df, personId, event="333", agg="best", all_events=False) -> "DataFrame":
    """Gets a persons rank on each day they competed"""
    person_rankings = pd.DataFrame()
    person_attributes = get_person_attributes(df, personId)
    dates_competed = person_attributes["dates_competed"]

    # Generates a csv for all events a competitor has competed on
    if all_events:
        events_competed = person_attributes["events_competed"]  
        
        for event in events_competed:
            # is_event prevents having to aggregate each 
            # iteration without filtering the dataframe in place
            is_event = df.eventId == event # Returns a series of boolean values
            person_rankings = pd.DataFrame()
            for date in dates_competed:
                rank_at_date = find_rank(df.loc[is_event], personId, date, agg)
                person_rankings = person_rankings.append(rank_at_date)
            # Saving resulting dataframe to csv by event and aggregation type
            person_rankings = person_rankings.sort_values(by="date", ascending=False).set_index("date")
            person_rankings.to_csv(f"{personId}-{event}-{agg}-rankings.csv")
    else:
        for date in dates_competed:
            person_rankings.append(find_rank(df, personId, event, as_of=date))
        person_rankings = person_rankings.sort_values(by="date", ascending=False).set_index("date")
        person_rankings.to_csv(f"{personId}-{event}-{agg}-rankings.csv")


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
             ]}
results_replace = {
            "best": {0: np.nan, -1: np.nan},
            "average": {0: np.nan, -1: np.nan}
            }

results = results.drop(**result_cols)
results.replace(results_replace, inplace=True)
non_value_cols = [col for col in results.columns if col[0] != "v"]
results = results[non_value_cols]

# Renaming to convert endDate and endDay columns
# to datetime and renaming id for joining with results
dates = ["year", "month", "day"]
rename_comp_cols = {"columns":{
             "id": "competitionId",
             "endMonth": "month", 
             "endDay": "day"
             }}

drop_comp_cols = {"columns":[
            "month", "day",
            ]}

# Modifying competition dataframe to combine with results dataframe
competitions = competitions.drop(**drop_comp_cols)
competitions.rename(**rename_comp_cols, inplace=True)
competitions["date"] = pd.to_datetime(competitions[dates])
competitions = competitions[["competitionId", "date"]]

# Merging competition table with results table
ranks = pd.merge(competitions, results, on="competitionId")

# Aggregating best solves per competition by person, 
# event, and date of the competition, sorting by initial date
ranks = ranks.groupby(["personId", "eventId", "date", "competitionId"]).min(agg)
ranks = ranks.reset_index().sort_values(by="date")

if agg == "best" or agg == "b":
    ranks.to_csv(f"persons_best_by_dates_competed.csv")
elif agg == "average" or agg == "a":
    ranks.to_csv(f"persons_best_average_by_dates_competed_.csv")
if all_events == "yes" or all_events == "y":
    
    get_person_ranks(ranks, personId, agg=agg, all_events=True)
else:
    event = input("Event: ")
    get_person_ranks(ranks, personId, event, agg)
