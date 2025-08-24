"""
This script is to convert the polymarket URL's into their token_ids
"""

import json
import sys

import requests


def get_price(token_id: str) -> float | None:
    """
    Get the price of a token.

    Args:
        token_id: The ID of the token to get the price of.

    Returns:
        float: The price of the token.
    """
    base_url = "https://clob.polymarket.com/price"
    params = {"token_id": token_id, "side": "sell"}
    response = requests.request("GET", base_url, params=params)
    response_data = response.json()
    if response_data.get("error") == "No orderbook exists for the requested token id":
        return None

    return response.json()["price"]


def get_token_ids(slug):
    """
    Get the token IDs for a given slug.

    Args:
        slug: The slug of the event to get the token IDs for.

    Returns:
        dict: A dictionary of event slugs and their token IDs and prices.
    """
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
            price = get_price(token_ids[i])
            event_info[outcomes[i]] = (price, token_ids[i])

        event_res[event_slug] = event_info

    return event_res


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_token_id.py <slug>")
        print("Example: python get_token_id.py will-trump-remove-jerome-powell")
        sys.exit(1)

    slug = sys.argv[1]
    print(f"SLUG: {slug}")

    token_ids = get_token_ids(slug)
    print(json.dumps(token_ids, indent=2))
