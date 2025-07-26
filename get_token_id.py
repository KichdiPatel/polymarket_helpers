"""
This script is to convert the polymarket URL's into their token_ids
"""

import requests
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_token_id.py <slug>")
        print("Example: python get_token_id.py will-trump-remove-jerome-powell")
        sys.exit(1)

    slug = sys.argv[1]
    print(f"SLUG: {slug}")

    response = requests.get(
        "https://gamma-api.polymarket.com/events", params={"slug": slug}
    )

    response = response.json()[0]
    event_res = {}

    for market in response["markets"]:
        event_slug = market["slug"]
        outcomes = json.loads(market["outcomes"])
        token_ids = json.loads(market["clobTokenIds"])

        event_info = {}
        for i in range(len(outcomes)):
            event_info[outcomes[i]] = token_ids[i]

        event_res[event_slug] = event_info

    print(json.dumps(event_res, indent=2))
