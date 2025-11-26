



# How to Run and Test

---

## Running the Wellness Orchestrator (Direct Mode)

### 1. Prerequisites

- **Python**: 3.10+ installed and on PATH  
- **Dependencies**: from the project root:

```powershell
python -m pip install -r requirements.txt
```

- **Google API key**: create a `.env` file in the project root with:

```env
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

### 2. How user identity works

The app uses a **user id** to tie together:

- Profile: [data/user_profiles.json](cci:7://file:///c:/Users/Pritha/Desktop/wellness/data/user_profiles.json:0:0-0:0)
- Long‑term memories: [data/user_memory.json](cci:7://file:///c:/Users/Pritha/Desktop/wellness/data/user_memory.json:0:0-0:0)

Rules:

- If `WELLNESS_USER_ID` env var is set, that value is used (e.g. `alice`, `bob`).
- Otherwise, a random ID is generated once and stored in `data/user_id.txt` and reused across runs.

So:

- **Same user** ⇒ same `WELLNESS_USER_ID` (or same `data/user_id.txt`)  
- **Different user** ⇒ use a different `WELLNESS_USER_ID`.

### 3. Starting the app

From the project root:

```powershell
# (Optional) pick a user id for this run
$env:WELLNESS_USER_ID = "alice"

# Run the orchestrator
python app.py
```

You should see:

```text
=== Wellness Orchestrator (Direct Mode) ===
Type your wellness goals or questions. Press Ctrl+C to exit.
```

Then you can type directly:

```text
You > I want to reduce my arm fat
```

### 4. What to expect

- The **Chief Wellness Officer (CWO)** is the only entry point.
- CWO may:
  - Fetch your profile (age, weight, gender, fitness level).
  - Load your past memories (previous goals, stress issues, etc.).
  - Route to:
    - `exercise_coach` for exercise plans.
    - `mindfulness_orchestrator` for stress / crisis / mindfulness.

You’ll see logging like:

```text
🔧 Tool call: get_user_profile
✅ Tool response: get_user_profile
🔧 Tool call: exercise_coach
...
⏱️  Total time: 3.47s
🤖 CWO: ...
```

### 5. Suggested scenarios to try

#### A. New user, exercise goal

```powershell
$env:WELLNESS_USER_ID = "alice"
python app.py
```

Conversation:

```text
You > I want to reduce my arm fat
# CWO will ask for age, weight, gender, fitness level
You > 36, 54kg
You > gender is female
You > beginner
```

- CWO completes your **exercise profile**.
- Then routes to `exercise_coach`, which calls [generate_workout_plan](cci:1://file:///c:/Users/Pritha/Desktop/wellness/exercise_agent/exercise_tools.py:104:0-132:15).
- CWO summarizes a personalized plan.

#### B. Resuming as the same user

Later:

```powershell
$env:WELLNESS_USER_ID = "alice"
python app.py
```

Examples:

- If you say `I want another plan`, CWO can:
  - Reuse your stored profile from [data/user_profiles.json](cci:7://file:///c:/Users/Pritha/Desktop/wellness/data/user_profiles.json:0:0-0:0).
  - Load any stored memories (e.g., “arm‑fat reduction” goals) and reference them.

#### C. Different user

```powershell
$env:WELLNESS_USER_ID = "bob"
python app.py
You > I am stressed
```

- CWO will route to `mindfulness_orchestrator`.
- This user starts with a **clean slate**: no profile, no memories.

#### D. Crisis scenario (mindfulness)

Using any user id:

```text
You > I want to commit suicide
```

- CWO will prioritize crisis support:
  - Route through the mindfulness stack.
  - Provide emergency resources rather than exercise plans.

### 6. Where state is stored

- **Profiles** (per user): [data/user_profiles.json](cci:7://file:///c:/Users/Pritha/Desktop/wellness/data/user_profiles.json:0:0-0:0)
- **Long‑term memories** (per user): [data/user_memory.json](cci:7://file:///c:/Users/Pritha/Desktop/wellness/data/user_memory.json:0:0-0:0)
- **Default user id** (if no `WELLNESS_USER_ID`): `data/user_id.txt`

You can inspect these files after test runs to see what the app has learned about each user.

---

You can hand this note to others; they just need Python + `requirements.txt` + a `GOOGLE_API_KEY` to reproduce and explore different user journeys.