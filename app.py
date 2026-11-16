#!/usr/bin/env python3
"""
FitFindr — command line.

    python app.py ask 'vintage graphic tee under $30, size M'
    python app.py ask                     keep asking until you quit
    python app.py ask --empty-wardrobe    run as a user with nothing saved
    python app.py listings                browse the data  (Milestone 1)
    python app.py fields                  what fields a listing has
    python app.py examples                queries worth trying, including a dud
    python app.py add                     add a new clothing item to the wardrobe

Add --trace to any `ask` to print the loop step by step.

⚠️ Quote your query with SINGLE quotes. In PowerShell, "under $30" in double
quotes silently becomes "under " — PowerShell reads $30 as a variable and
substitutes nothing, so you search with no price ceiling and get no error
telling you why. Single quotes are literal in PowerShell, bash and zsh alike.
"""

import argparse
import sys
import json
import config
from utils.run_log import log_run

# Every query here except the last one has something real to find in
# data/listings.json. If you add your own, check it against the data first — a
# query that finds nothing because the item doesn't exist looks exactly like a
# search tool that's broken.
EXAMPLE_QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
    "designer ballgown size XXS under $5",   # matches nothing, on purpose
]


def cmd_fields(args):
    """Milestone 1 — you can't filter on a field that isn't there."""
    from utils.data_loader import load_listings, get_example_wardrobe

    listing = load_listings()[0]
    print("A listing has these fields:\n")
    for key, value in listing.items():
        shown = str(value)
        if len(shown) > 58:
            shown = shown[:58] + "…"
        print(f"  {key:<14} {type(value).__name__:<6} {shown}")

    item = get_example_wardrobe()["items"][0]
    print("\nA wardrobe item has these fields:\n")
    for key, value in item.items():
        shown = str(value)
        if len(shown) > 58:
            shown = shown[:58] + "…"
        print(f"  {key:<14} {type(value).__name__:<6} {shown}")

    print(
        "\nThese are what search_listings can filter on. Read a few whole "
        "listings\nwith `python app.py listings` before you write it."
    )


def cmd_listings(args):
    """Milestone 1 — read the data before you write tools against it."""
    from utils.data_loader import load_listings

    listings = load_listings()

    if args.full:
        import json
        for listing in listings[: args.n]:
            print(json.dumps(listing, indent=2))
            print()
        return

    print(f"{len(listings)} listings.\n")
    print(f"{'id':<6}{'price':>8}  {'size':<22}{'platform':<11}title")
    print("-" * 92)
    for listing in listings[: args.n]:
        print(
            f"{str(listing['id']):<6}"
            f"{listing['price']:>8.2f}  "
            f"{str(listing['size']):<22}"
            f"{listing['platform']:<11}"
            f"{listing['title'][:38]}"
        )
    if len(listings) > args.n:
        print(f"\n… {len(listings) - args.n} more. Use -n {len(listings)} to see them all.")
    print("\nRead five or six all the way through: python app.py listings --full -n 6")


def cmd_examples(args):
    print("Queries worth trying:\n")
    for query in EXAMPLE_QUERIES[:-1]:
        print(f"  python app.py ask '{query}'")
    print(f"\nAnd one the data cannot match — this is the empty-search branch:\n")
    print(f"  python app.py ask '{EXAMPLE_QUERIES[-1]}'")
    print(
        "\nSingle quotes on purpose. In PowerShell a query in \"double quotes\"\n"
        "loses the $30 — it gets read as a variable — and you search with no\n"
        "price ceiling, with nothing to tell you it happened."
    )


def _ask_one(query, wardrobe, use_trace):
    from agent import run_agent
    import trace as trace_module

    if use_trace:
        trace_module.start_trace()

    session = run_agent(query, wardrobe)

    print()
    if session["error"]:
        print(f"  {session['error']}")
    else:
        item = session["selected_item"] or {}
        print(f"  Found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
        print()
        print(f"  Outfit:   {session['outfit_suggestion']}")
        print()
        print(f"  Fit card: {session['fit_card']}")
    print()

    if use_trace:
        text = trace_module.get_trace()
        if not text:
            print(
                "  (--trace printed nothing. You haven't added trace.step() calls to\n"
                "   run_agent() yet — that's unit 4, Milestone 2.)\n"
            )
    return session


def cmd_ask(args):
    from utils.data_loader import get_example_wardrobe, get_empty_wardrobe
    import generate

    wardrobe = get_empty_wardrobe() if args.empty_wardrobe else get_example_wardrobe()
    if args.empty_wardrobe:
        print("(running with an empty wardrobe)")

    try:
        if args.query:
            _ask_one(args.query, wardrobe, args.trace)
        else:
            print("Ask for something, or press Enter on an empty line to quit.\n")
            while True:
                try:
                    query = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if not query:
                    break
                _ask_one(query, wardrobe, args.trace)
    finally:
        print(generate.usage())

WARDROBE = config.ROOT / "data" / "wardrobe_schema.json"
def cmd_add(args):
    print("Adding new item to wardrobe")
    print("---------------------------")
    
     # Read the whole file into a Python dict
    with WARDROBE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    example_wardrobe = data["example_wardrobe"]
    items = example_wardrobe["items"]

    # Get the id of the last entry and make the next id
    id = "w_001"
    if items:
        last_id = items[-1]["id"]
        id_number = int(last_id[2:]) + 1
        id = "w_" + str(id_number).zfill(3)

    # Prompt for fields
    making_item = True
    while making_item:
        print("Enter the item's fields.")
        print()

        def nonempty_input(prompt: str = ""):
            # inputs, but if the user enters only whitespace, input again
            user_input = ""
            while not user_input:
                print(prompt, end="")
                user_input = input().strip()
                if not user_input:
                    print("*** Invalid input; please enter a value.")
            return user_input

        name = nonempty_input("Item Name: ")
        print()

        # category MUST be one of the established categories
        categories = ["tops", "bottoms", "shoes", "accessories", "outerwear"]
        print("The item's category MUST be one of the following: " + ", ".join(categories))
        categories = set(categories)
        category = None
        while not category:
            catg_input = nonempty_input("Category: ").lower()

            if catg_input not in categories:
                print("*** not a valid category.")
            else:
                category = catg_input
        print()

        # Input multiple entries comma-separated
        # also print out all the current colors in case the user wants to match them (match is not required)
        # do this for colors and style_tags
        def input_multiple(field_name: str):
            print(f'{field_name.capitalize()}: Enter every value separated by a comma.')
            
            entries = set()
            for item in items:
                entries.update(item[field_name])
            entries = sorted(entries)
            print(f'(For reference, other {field_name}: {entries})')

            entry_input = nonempty_input()
            entries = [entry.strip() for entry in entry_input.split(",")]

            print()
            return entries

        colors = input_multiple("colors")
        style_tags = input_multiple("style_tags")

        print("Any extra notes? (if not, keep blank and press Enter): ", end="")
        notes = input().strip() or None
        print()

        clothing_item = {
            "id": id,
            "name": name,
            "category": category,
            "colors": colors,
            "style_tags": style_tags,
            "notes": notes
            }
        
        for field, value in clothing_item.items():
            if field != "id":
                print(f'{field.capitalize()}: {value}')
        print("---------------------------")

        input_is_ok = 'x'
        acceptable_responses = {"y", "n"}
        while input_is_ok not in acceptable_responses:
            print("Is this okay? (y/n): ", end="")
            input_is_ok = input().strip().lower()

            if input_is_ok not in acceptable_responses:
                print("*** Invalid response")
            else:
                making_item = False if input_is_ok == 'y' else True
        print()

    # Append to the nested list
    data["example_wardrobe"]["items"].append(clothing_item)

    # Write the whole dict back, overwriting the file
    with WARDROBE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    log_run(event="add",
            item=clothing_item,
            wardrobe_size=len(data["example_wardrobe"]["items"]))

    print(f"{clothing_item['name']} has been added to the wardrobe.")

def build_parser():
    parser = argparse.ArgumentParser(
        prog="app.py",
        description="FitFindr",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_fields = sub.add_parser("fields", help="what fields the data has")
    p_fields.set_defaults(func=cmd_fields)

    p_list = sub.add_parser("listings", help="browse the listings data")
    p_list.add_argument("-n", type=int, default=15, help="how many to show")
    p_list.add_argument("--full", action="store_true", help="print whole records")
    p_list.set_defaults(func=cmd_listings)

    p_ex = sub.add_parser("examples", help="queries worth trying")
    p_ex.set_defaults(func=cmd_examples)

    p_ask = sub.add_parser("ask", help="run the agent")
    p_ask.add_argument("query", nargs="?")
    p_ask.add_argument("--trace", action="store_true", help="print the loop step by step")
    p_ask.add_argument(
        "--empty-wardrobe",
        action="store_true",
        help="run as a user with nothing saved — one of unit 4's failure modes",
    )
    p_ask.set_defaults(func=cmd_ask)

    p_ex = sub.add_parser("add", help="add a new clothing item to the wardrobe")
    p_ex.set_defaults(func=cmd_add)

    return parser


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — students read this, not a traceback
        print(f"\n{type(exc).__name__}: {exc}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
