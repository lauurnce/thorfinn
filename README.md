# askeladd

I built this because my days pull in too many directions at once: studies, work, something I'm building, a group I lead, training, and money. The information never stops, and I was spending more energy sorting it than acting on it. So I set up a council of six advisors, each named after someone from Vinland Saga, to carry the noise for me. Each one reads only its own domain, writes only to its own tab, and never acts on my behalf. They advise, track and warn. I decide.

It's written as a baseline anyone can use. Swap in your own sources, fill in the bracketed context in each prompt, and drop any member you don't need.

<img src="art/leif.svg" align="left" width="300">

## Leif, the Navigator

Schedule, commitments and information triage. Leif spent years crossing seas to keep one promise. He reads the calendar, email, chat and every council tab each morning, and by 9:00 AM leaves one brief: top three, conflicts, one decision. Runs daily.

<br clear="left">

<img src="art/einar.svg" align="left" width="300">

## Einar, the Farmer

Studies and day-job work. Einar plows the same field every day until it yields. He tracks school and work deadlines and requests, and warns before exams and big deliverables. Runs twice a week.

<br clear="left">

<img src="art/askeladd.svg" align="left" width="300">

## Askeladd, the Strategist

Ventures, side projects and strategy. Askeladd always has a plan behind the plan. He reads the venture's metrics against its own targets, red-teams the assumptions, and watches the pipeline and upcoming applications or launches. Blunt by design. Runs Sunday evening.

<br clear="left">

<img src="art/thors.svg" align="left" width="300">

## Thors, the True Warrior

A team, club or organisation you lead. Thors led by protecting his people before himself. He watches plans and goals, event countdowns, owner follow-ups and membership, and reminds the leader to build the crew, not carry it. Runs Sunday.

<br clear="left">

<img src="art/canute.svg" align="left" width="300">

## Canute, the King

Finances. Canute learned to run a kingdom as an economy. He reads the finance sheet without ever touching it, reports spending against budget, flags unusual expenses, and keeps any group funds separate from personal money. Runs on the 1st of each month.

<br clear="left">

<img src="art/thorkell.svg" align="left" width="300">

## Thorkell, the Giant

Health and fitness. Thorkell loves a good fight and brings joy to the hard days. He reads the health log, counts sessions kept and nights slept, watches supplements and caffeine, and sets the week's plan with a grin. A coach, never a doctor. Runs Sunday.

<br clear="left">

## How it runs

- One Claude Project holds the charter as its instructions.
- Six scheduled tasks live inside that Project, one per member, each on its own cadence.
- Each member writes only to its own tab in a hub Sheet.
- Leif alone writes the daily brief.

## Layout

- `CHARTER.md`: the council charter that goes into the Project instructions, with placeholders to fill in.
- `SCHEDULE.md`: when each member runs and what it reads and writes.
- `members/`: one file per member with its role, scope, sources, cadence and prompt.
- `hub-sheet.md`: the structure of the hub Sheet and its tabs.
- `SETUP.md`: the checklist to get the council running.
- `CHANGELOG.md`: changes to the council over time.
