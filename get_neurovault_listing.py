import json
import pandas as pd
from rich import print
import requests

DEBUG = False

listing_file = "neurostore_listing.json"

with open("token.txt") as f:
    TOKEN = f.read().strip()

def main():

    with open(listing_file) as f:
        listing = json.load(f)

    template_metadata_to_collate = "template_metadata.json"

    with open(template_metadata_to_collate) as f:
        data = json.load(f)
    data["doi"] = []
    data["pmid"] = []

    for paper in listing["results"]:

        if DEBUG and len(data["doi"]) > 10:
            break

        if paper["metadata"]:

            for key in data:
                value = "n/a"
                if key in paper["metadata"]:
                    value = paper["metadata"][key]
                if value in [[], None, ""]:
                    value = "n/a"
                data[key].append(value)

            doi = paper.get("doi")
            data["doi"][-1] = doi

            pmid = paper.get("pmid") or get_pmid_from_doi(doi=paper["doi"])
            data["pmid"][-1] = pmid


    df = pd.DataFrame(data)
    df.to_csv("neurovault_listing.tsv", sep="\t", index=False)


def get_pmid_from_doi(doi: str):
    # https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/
    my_tool = "repro_carp"
    my_email = "remi.gau@gmail.com"
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool={my_tool}&email={my_email}&ids={doi}&format=json"
    print(url)
    r = requests.get(url)
    if r.status_code != 200 or r.json()["records"][0].get("status") == "error":
        print(f"[red] Error with doi {doi}")
        return None
    return r.json()["records"][0]["pmid"]


if __name__ == "__main__":
    main()