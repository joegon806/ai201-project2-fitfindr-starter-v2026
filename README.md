# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a tool that lets you thrift for clothes items and form outfit posts with them. To use, enter `python app.py ask '<item>'`, replacing `item` with a description of a clothes item you want. FitFindr searches through thrift listings for the best item that matches what you want, and then generates an outfit using the item and other clothes items from your own wardrobe. Finally, FitFindr prints out a caption you can use to write a post about the new item and your new outfit. 

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings for clothes items that match the user's provided description, size (optional), and price (optional).
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
`description` (string), `size` (string, optional), `max_price` (float)
- **Returns:** A list of the matching clothes listing dicts.
- **When it has nothing:** If there are no matching clothes listings, returns an empty list.

### `suggest_outfit`

- **What it does:** Takes an item listing and generates up to two full outfits using the item along with clothes items in the user's wardrobe.
- **Inputs:** `new_item` (dict), `wardrobe` (dict) 
- **Returns:** A string suggesting up to two outfits.
- **When it has nothing:** If `wardrobe` is empty, returns a string with general styling advice.

### `create_fit_card`

- **What it does:** Generates a caption someone would write for a post about a new item and its potential outfit.
- **Inputs:** `outfit` (string), `new_item` (dict)
- **Returns:** A string caption of 2-4 sentences.
- **When it has nothing:** If `outfit` is empty, returns a message describing only `new_item` instead.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in session["error"] naming what the user could change, and return the session without calling suggest_outfit. Otherwise take the first result, put it in session["selected_item"], and continue.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex

**What moves through the session:** `"query"`, `"parsed"`, `"search_results"`, `"selected_item"`, `"wardrobe"`, `"outfit_suggestion"`, `"fit_card"`, `"error"`

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'
[1] parse_query
      in:  vintage graphic tee under $30, size M
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, 90s Silk Slip Dress — Floral, Midi Length … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1: - Top: Y2K Baby Tee — Butterfly Print - Bottom: Baggy straight-leg jeans, dark wash - Shoes: Chunky …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Score! Finally tracked down this super cute Y2K butterfly baby tee on Depop for just $18, and the pastel pink …

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit 1:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Baggy straight-leg jeans, dark wash
- Shoes: Chunky white sneakers
- Accessories: Black crossbody bag

Outfit 2:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Wide-leg khaki trousers
- Shoes: Chunky white sneakers
- Outerwear: Vintage black denim jacket

  Fit card: Score! Finally tracked down this super cute Y2K butterfly baby tee on Depop for just $18, and the pastel pink and purple print is giving major early 2000s nostalgia. I'm totally planning to style it with dark wash baggy jeans and chunky white sneakers for an effortless off-duty look, or dress it down a bit with some wide-leg khaki trousers and a vintage black denim jacket.

2 model calls this session, 1197 prompt + 174 output tokens
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Outfit 1:
- Top: White ribbed tank top
- Bottom: Vintage Levi's 501 Jeans — Medium Wash
- Shoes: Chunky white sneakers
- Accessories: Brown leather belt

Outfit 2:
- Top: Oversized grey crewneck sweatshirt
- Bottom: Vintage Levi's 501 Jeans — Medium Wash
- Shoes: Black combat boots
- Outerwear: Vintage black denim jacket
- Accessories: Brown leather belt, Black crossbody bag
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these classic vintage Levi's 501 jeans on Depop for just $38, and they honestly have the ultimate 90s streetwear vibe with that broken-in medium wash. I'm keeping it effortless and styling them with a crisp white tee and my go-to white sneakers for the easiest weekend fit. Perfect distressing at the knees without any actual damage—such a solid denim find!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude for ideas for the state criterion.
- *What came back:* Four ideas: Option A was about the state passing through stages, Option B was about state appearing in the final output, Option C was about state not leaking between runs, and Option D was about state being None on an empty search result.
- *What I changed:* I used and modified Option A, because it's the most crucial criterion to maintain for the system, and is straightforward to test.

**Moment 2**

- *What I asked for:* I asked Claude to review my code for the three tools.
- *What came back:* Claude commended my code's structure, but caught a few bugs, typos, and other oversights.
- *What I changed:* I reviewed and implemented the suggested fixes if they were appropriate for the functionality outlined in the docstrings.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. trace report shows passing state | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card mentions other items in outfit | 3 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. all items match | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

### matching query completes
File: ```agent.py```, Function: ```run_agent```
```
Query: vintage graphic tee under $30
Wardrobe: example

Try 1
stopped early: no
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
search_results: 10
Outfit suggestion:

Outfit 1:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Baggy straight-leg jeans, dark wash
- Shoes: Chunky white sneakers
- Outerwear: Vintage black denim jacket
- Accessories: Black crossbody bag

Outfit 2:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Wide-leg khaki trousers
- Shoes: Black combat boots
- Accessories: Brown leather belt

Fit card:

Scored this adorable Y2K butterfly baby tee on Depop for just $18 and I am obsessed with the nostalgic pastel print! It gives off the ultimate early 2000s indie-sleaze vibe, and I can't wait to style it either casually with dark-wash baggy jeans and chunky sneakers or edge it up with wide-leg trousers and combat boots.
```

### impossible query stops early
File: ```agent.py```, Function: ```_nothing_found_message```
```
Query: designer ballgown size XXS under $5
Wardrobe: example

Try 1
stopped early: yes — Nothing in the listings matched description 'designer ballgown', size XXS, under $5. Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
selected_item: (none)
search_results: 0
```

### trace report shows passing state
File: ```trace.py```, Function: ```step```
```
Query: vintage graphic tee under $30
Wardrobe: example

Try 1
...
Trace:

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1: - Top: Y2K Baby Tee — Butterfly Print - Bottom: Baggy straight-leg jeans, dark wash - Shoes: Chunky …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Scored the ultimate early 2000s butterfly baby tee on Depop for just $18, and it’s giving major nostalgia! I'm…
```

### fit card mentions other items in outfit
File: ```tools.py```, Function: ```create_fit_card```
```
Query: vintage graphic tee under $30
Wardrobe: example

Try 1
...
Fit card:

Found this absolute dream of a Y2K butterfly baby tee on Depop for just $18, and it’s giving major early 2000s mall-rat energy. I’m already planning to style it two ways: either keep it classic with baggy dark-wash denim and chunky kicks, or toughen it up with wide-leg khakis, combat boots, and a black denim jacket. Such a steal for the collection!
```

### all items match
File: ```tools.py```, Function: ```suggest_outfit```
```
Query: vintage graphic tee under $30
Wardrobe: example

Try 1
...
Outfit suggestion:

Outfit 1:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Baggy straight-leg jeans, dark wash
- Shoes: Chunky white sneakers
- Accessories: Black crossbody bag
...
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | matching query completes | 5 of 5 | MET | The system had no problem going through all steps of a run for the matching query, on all 5 tries. |
| 2 | impossible query stops early | 5 of 5 | MET | For all 5 tries, the system stopped the run early, citing that no items in the listings matched the impossible query. |
| 3 | trace report shows passing state | 5 of 5 | MET | For all 5 tries, The trace report successfully prints out the item listing and the output at each stage, showing the same item listing passing through each stage of the system. |
| 4 | fit card mentions other items in outfit | 3 of 5 | MET | All 5 outfit cards mention items in the outfit other than the thrifted item, and it doesn't force itself to say all of the items. Strangely, the caption never mentions Accessories at all. |
| 5 | all items match | 4 of 5 | MISSED | In all 5 tries, many of the clothes have no matching keywords with the other outfit items. |

**Diagnoses**

Criterion 5 MISSED: Every item in an outfit has at least one word in the description or style tags that matches with another item in the same outfit.
Although 2 of the outfits from the trial runs do meet this criterion with every item matching another item by some keyword, many of the outfit items do not match any other items. The tool that creates outfits, `suggest_outfit` in `tools.py`, does not specify in its prompt to match items by keyword. Its only guidance for matching items is to `"Take in consideration the items' styles and colors, when forming an outfit"`; otherwise, it's complete up to the judgement of the LLM to match the items in a fitting way to make the outfit.
The tool works as directed; rather, this criterion was written with an unfounded expectation in mind that the tool would naturally match items closely by their keywords.

ORIGINAL: Every item in an outfit has at least one word in the description or style tags that matches with another item in the same outfit.
REVISED: In every outfit, there are at least two items that match at least one word with each other in the description or style tags.
WHY: This new crtierion allows the system the freedom to be subjective in matching items, while the requirement of two matching items maintains that the system must have some sort of logic to the matching. I also plan on adding this criterion directly into the prompt for generating an outfit so that the LLM can meet the criterion directly.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  vintage graphic tee
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1: - Top: Y2K Baby Tee — Butterfly Print - Bottom: Baggy straight-leg jeans, dark wash - Shoes: Chunky …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Score! Finally tracked down this super cute Y2K butterfly baby tee on Depop for just $18, and the pastel pink …

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit 1:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Baggy straight-leg jeans, dark wash
- Shoes: Chunky white sneakers
- Accessories: Black crossbody bag

Outfit 2:
- Top: Y2K Baby Tee — Butterfly Print
- Bottom: Wide-leg khaki trousers
- Shoes: Chunky white sneakers
- Outerwear: Vintage black denim jacket

  Fit card: Score! Finally tracked down this super cute Y2K butterfly baby tee on Depop for just $18, and the pastel pink and purple print is giving major early 2000s nostalgia. I'm totally planning to style it with dark wash baggy jeans and chunky white sneakers for an effortless off-duty look, or dress it down a bit with some wide-leg khaki trousers and a vintage black denim jacket.

0 model calls this session, 2 served from cache
```

**Empty search**

```
[1] parse_query
      in:  empty search
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

  Nothing in the listings matched description 'empty search'.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'.

0 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
