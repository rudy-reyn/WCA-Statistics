#!/usr/bin/env python3
#
"""Get a persons rank on each day they competed and for each event
   
they've ever competed in, by best solve times and by average solve times.
Make sure you have the competitions dataset and the results dataset
in the same working directory when running this. I'm thinking some more
work could be done to prevent having to do so much work for each iteration.
"""
import sys
import pandas as pd

def find_rank(df, personId, as_of, agg) -> pd.DataFrame:
    # Find a person's rank on a pre-specified date
    filtered = df.loc[df.date <= as_of].groupby("personId").min(agg)
    filtered = filtered.sort_values(by="best").reset_index()

    # Player's current ranking is their index position
    filtered["rank"] = filtered.index + 1
    person_ranking = filtered.loc[filtered.personId == personId]
    person_ranking.insert(0, "date", as_of)

    return person_ranking

def get_person_attributes(df, personId) -> dict:
    filtered = df.loc[df.personId == personId]
    events_competed = tuple(filtered.eventId.unique())
    dates_competed = tuple(filtered.date.unique())

    person_attributes = {
        "events_competed": events_competed,
        "dates_competed": dates_competed
    }

    return person_attributes

def get_person_ranks(df, personId, event="333", agg="best", all_events=False):
    # persons rank on each day they have ever competed
    person_rankings = pd.DataFrame()
    person_attributes = get_person_attributes(df, personId)
    dates_competed = person_attributes["dates_competed"]

    # Generates a csv for all events a competitor has competed on
    if all_events:
        events_competed = person_attributes["events_competed"]

        for event in events_competed:
            # is_event prevents having to aggregate each
            # iteration without filtering the dataframe in place
            is_event = df.eventId == event
            person_rankings = pd.DataFrame()

            for date in dates_competed:
                rank_at_date = find_rank(df.loc[is_event], personId, date, agg)
                person_rankings = person_rankings.append(rank_at_date)

            person_rankings = person_rankings.sort_values(by="date", ascending=False).set_index("date")
            person_rankings.to_csv(f"{personId}-{event}-{agg}-rankings.csv")

    else:
        for date in dates_competed:
            rank = find_rank(df, personId, event, as_of=date)
            person_rankings = person_rankings.append(rank)

        person_rankings = person_rankings.sort_values(by="date", ascending)


personId = input("personId: ")
all_events = input("All events (yes/y, no/n)? ")
agg = input("Aggregation (best/b, average/a)? ")

if agg == "b" or agg == "best":
    persons = pd.read_csv("persons_best_by_dates_competed.csv")
elif agg == "a" or agg == "average":
    persons = pd.read_csv("persons_best_average_by_dates_competed.csv")
else:
    print("invalid option", file=sys.stderr)
    sys.exit(1)

if all_events == "yes" or all_events == "y":
    get_person_ranks(persons, personId, agg=agg, all_events=True)
elif all_events == "no" or all_events == "n":
    event = input("Event: ")
    get_person_ranks(persons, personId, event, agg)
else:
    print("invalid option", file=sys.stderr)
    sys.exit(1)
