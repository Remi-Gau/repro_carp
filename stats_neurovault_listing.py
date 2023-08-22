import pandas as pd
from rich import print
import plotly.express as px

def main():

    df = pd.read_csv("neurovault_listing.tsv", sep="\t")
    print(f"Number of collections from neurovault: {len(df)}")

    # exclude rows with n/a values in all columns
    df = df.dropna(how="all")

    print(f"Number of collections with some metadata: {len(df)}")
    plot_percentage_missing(df, title="Percentage of non missing values in each column of the NeuroVault listing")

    # drop rows that do not have field_strength
    df = df.dropna(subset=["field_strength"])
    print(f"Number of collections with field_strength: {len(df)}")
    plot_percentage_missing(df, title="Percentage of n/a values for papers that mention field_strength")


def plot_percentage_missing(df: pd.DataFrame, title: str) -> None:
    # use plotly to plot the percentage of n/a values in each column
    na_percentage = 100 - df.isna().sum() / len(df) * 100
    fig = px.bar(
        na_percentage,
        x=na_percentage.index,
        y=na_percentage.values,
        title=title,
    )
    fig.show()


if __name__ == "__main__":
    main()