import json
import pandas as pd
import requests

listing_file = "neurostore_listing.json"

with open(listing_file) as f:
    listing = json.load(f)

template_metadata_to_collate = "template_metadata.json"

with open(template_metadata_to_collate) as f:
    data = json.load(f)

for paper in listing["results"]:
    if paper["metadata"]:
        for key in data:
            value = "n/a"
            if key in paper["metadata"]:
                value = paper["metadata"][key]
            if value in [[], None, ""]:
                value = "n/a"
            data[key].append(value)

df = pd.DataFrame(data)
df.to_csv("neurovault_listing.tsv", sep="\t", index=False)
df = pd.read_csv("neurovault_listing.tsv", sep="\t")

print(len(df))

# exclude rows with n/a values in all columns
df = df.dropna(how="all")

print(len(df))

# compute percentage of n/a values there are in each column of dataframe
na_percentage = 100 - df.isna().sum() / len(df) * 100


# use plotly to plot the percentage of n/a values in each column
import plotly.express as px

fig = px.bar(
    na_percentage,
    x=na_percentage.index,
    y=na_percentage.values,
    title="Percentage of n/a values in each column of the NeuroVault listing",
)
fig.show()


# drop rows that do not have field_strength
df = df.dropna(subset=["field_strength"])

# replot
na_percentage = 100 - df.isna().sum() / len(df) * 100

fig = px.bar(
    na_percentage,
    x=na_percentage.index,
    y=na_percentage.values,
    title="Percentage of n/a values for papers that mention field_strength",
)
fig.show()
