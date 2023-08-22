import pandas as pd
from rich import print
import requests

DEBUG = False

with open("token.txt") as f:
    TOKEN = f.read().strip()

def main():

    df = pd.read_csv("neurovault_listing.tsv", sep="\t")
    print(f"Number of collections from neurovault: {len(df)}")

    # pmids to txt
    with open("pmids.txt", "w") as f:
        pmids = df["pmid"].dropna().unique()
        pmids = [str(int(pmid)) for pmid in pmids]
        for pmid in pmids:
            f.write(f"{pmid}\n")

    data = df.to_dict(orient="list")

    data["year"] = []
    data["title"] = []
    data["source_title"] = []

    for i, doi in enumerate(data["doi"]):

        if i % 20 == 0:
            print(f"Processing {i+1} / {len(data['doi'])}")

        if doi:
            if metadata := get_metadata_from_doi(doi):
                metadata = metadata[0]
                year = metadata["year"]
                title = metadata["title"]
                source_title = metadata["source_title"]
        data["year"].append(year)
        data["title"].append(title)
        data["source_title"].append(source_title)

    df = pd.DataFrame(data)
    df.to_csv("neurovault_listing_augmented.tsv", sep="\t", index=False)

def get_metadata_from_doi(doi: str) -> dict[str, str]:
    headers = {"authorization": TOKEN}
    api_call = f"https://opencitations.net/index/coci/api/v1/metadata/{doi}"
    r = requests.get(api_call, headers=headers)
    if r.status_code == 200:
        return r.json()
    print(f"[red]Error: {r.status_code}[/red]")
    return {}


if __name__ == "__main__":
    main()