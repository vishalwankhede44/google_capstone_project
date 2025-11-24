# Wellness Planning Multi-Agent Application

A capstone project featuring a multi-agent system that creates personalized wellness plans using Google's Agent Development Kit (ADK) and Gemini models.

## Features

- **Multi-Agent Architecture with Google ADK**: Chief Wellness Officer coordinates 4 specialist agents
  - Mindfulness Agent
  - Nutrition Agent
  - Exercise Agent
  - Calendar Agent

- **MCP (Model Context Protocol) Integration** 🆕
  - 📅 **Calendar MCP**: Real Google Calendar integration for conflict-free scheduling
  - 🌤️ **Weather MCP**: Live weather data for adaptive exercise planning
  - Optional features that enhance real-world applicability

- **Powered by Google Gemini**: Uses Gemini 2.0 Flash for fast, intelligent responses
- **Personalized Plans**: Based on user profile (age, weight, height) and goals
- **Agent Collaboration**: Agents are aware of each other's plans for better integration
- **Interactive Dashboard**: View all plans and track progress
- **Progress Logging**: Daily check-ins and activity completion tracking
- **Conflict Resolution**: Calendar agent resolves scheduling conflicts

## Technology Stack

- **Backend**: Flask + Python
- **Database**: SQLite
- **AI**: Google ADK + Gemini 2.0 Flash (free tier)
- **MCP Integration**: Calendar & Weather APIs (optional)
- **Frontend**: HTML/CSS/JavaScript (vanilla)

## Quick Start

> **Note**: MCP integration is OPTIONAL. The app works perfectly without it!

### 1. Install Dependencies

```bash
cd wellness_app
pip install -r requirements.txt
```

### 2. Get Google API Key (Free)

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

**Note**: Google AI Studio provides free tier access to Gemini models - perfect for capstone projects!

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. (Optional) Enable MCP Integration

**For enhanced real-world integration**, you can enable MCP features:

#### Weather MCP (Recommended - Easy Setup)
Get live weather forecasts for adaptive exercise planning:

1. Get free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Update `.env`:
   ```
   ENABLE_WEATHER_MCP=true
   WEATHER_API_KEY=your_openweathermap_key
   WEATHER_LOCATION=New York
   ```

#### Calendar MCP (Advanced)
Integrate with real Google Calendar:

See **[MCP_SETUP.md](MCP_SETUP.md)** for detailed instructions.

**Testing MCP**:
```bash
python test_mcp.py
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Step 1: Create Your Profile
- Enter your name, age, weight, and height
- This information is used to personalize all plans

### Step 2: State Your Goal
- Example: "Help me reduce stress"
- The Chief Wellness Officer will analyze and route to specialists

### Step 3: Review Your Plans
- **Overview Tab**: See your unified weekly schedule
- **Mindfulness Tab**: Meditation and stress reduction techniques
- **Nutrition Tab**: Personalized meal plans and nutrition guidance
- **Exercise Tab**: Custom workout routines
- **Progress Tab**: Log daily activities and track your journey

### Step 4: Track Progress
- Log daily mood and stress levels
- Mark completed activities
- Add notes about your experience

## Architecture - Google ADK Implementation

### Agent Flow with Google Gemini

```
User Goal → Chief Wellness Officer (Gemini)
              ↓
    ┌─────────┼─────────┬─────────┐
    ↓         ↓         ↓         ↓
Mindfulness Nutrition Exercise Calendar
   Agent      Agent     Agent    Agent
(Gemini)   (Gemini)  (Gemini)  (Gemini)
    ↓         ↓         ↓         ↓
    └─────────┼─────────┴─────────┘
              ↓
    Unified Weekly Schedule (Gemini)
```

### Agent Collaboration with Shared Context

Each agent receives shared context including:
- User profile
- Original goal
- CWO analysis
- Plans from previous agents

This allows:
- Nutrition agent to align with exercise needs
- Exercise agent to incorporate mindfulness practices
- Calendar agent to resolve all scheduling conflicts

### Google ADK Benefits

1. **Free Tier**: Generous quota for development and demos
2. **Fast Response**: Gemini 2.0 Flash optimized for speed
3. **Context Length**: Large context window for sharing agent outputs
4. **Reliability**: Google's production infrastructure
5. **Easy Integration**: Simple Python SDK

## Database Schema

- **User**: Profile information
- **Goal**: User's wellness goals
- **Plan**: AI-generated wellness plans
- **ProgressLog**: Daily tracking data

## API Endpoints

### User Management
- `POST /api/create-user` - Create user profile
- `GET /api/get-user/<user_id>` - Retrieve user data

### Goal & Plan Management
- `POST /api/submit-goal` - Submit wellness goal and generate plan
- `GET /api/get-plan/<goal_id>` - Retrieve existing plan

### Progress Tracking
- `POST /api/log-progress` - Log daily progress
- `GET /api/get-progress/<goal_id>` - Get progress history

## Extending the Application

### Adding New Agents

1. Create new agent file in `agents/` directory:

```python
from google.genai import types

class SleepAgent:
    def __init__(self, google_client, model):
        self.client = google_client
        self.model = model
    
    def create_plan(self, shared_context):
        # Agent logic here
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a sleep specialist...",
                temperature=0.7,
                max_output_tokens=1500
            )
        )
        return response.text
```

2. Initialize in `ChiefWellnessOfficer.__init__`
3. Add to routing logic
4. Update shared context flow

### Customizing Gemini Models

Google provides several models:
- `gemini-2.0-flash-exp` - Fast, efficient (current)
- `gemini-1.5-pro` - More powerful, larger context
- `gemini-1.5-flash` - Balanced speed/quality

Change in `agents/chief_wellness_officer.py`:
```python
self.model = "gemini-1.5-pro"
```

### Adding Function Calling

Google ADK supports function calling for structured outputs:

```python
from google.genai import types

function_declarations = [
    types.FunctionDeclaration(
        name="schedule_activity",
        description="Schedule a wellness activity",
        parameters={
            "type": "object",
            "properties": {
                "activity": {"type": "string"},
                "time": {"type": "string"},
                "duration": {"type": "integer"}
            }
        }
    )
]

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=function_declarations)]
)
```

## Project Structure

```
wellness_app/
├── app.py                 # Flask application
├── agents/
│   ├── __init__.py
│   ├── chief_wellness_officer.py  # Uses Google ADK
│   ├── mindfulness_agent.py       # Gemini-powered
│   ├── nutrition_agent.py         # Gemini-powered
│   ├── exercise_agent.py          # Gemini-powered
│   └── calendar_agent.py          # Gemini-powered
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── requirements.txt
├── .env.example
└── README.md
```

## Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify API key is set correctly
- Restart the Flask application

### API Rate Limits
- Google AI Studio free tier is generous
- If hitting limits, implement caching or throttling
- Consider upgrading to paid tier for production

### Model Errors
- Check API key is valid at [Google AI Studio](https://aistudio.google.com/)
- Ensure you're using a supported model name
- Check network connectivity

### Database Errors
- Delete `wellness.db` to reset database
- Restart application to recreate tables

## License

MIT License - Free for educational and commercial use

## Google ADK vs Other Frameworks

**Why Google ADK for this project:**
- ✅ Free tier with generous quotas
- ✅ Fast Gemini 2.0 Flash model
- ✅ Easy Python integration
- ✅ Production-ready infrastructure
- ✅ Large context windows for agent collaboration
- ✅ Built-in safety features

**Comparison:**
| Feature | Google ADK | Groq | OpenAI |
|---------|-----------|------|--------|
| Free Tier | ✅ Generous | ✅ Limited | ❌ |
| Speed | ⚡ Fast | ⚡⚡ Very Fast | ⚡ Fast |
| Context | 🔥 Large | Medium | 🔥 Large |
| Capstone Ready | ✅ Yes | ✅ Yes | ⚠️ Costs $ |

## Demo Script for Presentation

1. **Show Profile Creation**
   - "I'm creating a profile for Sarah, 28 years old..."

2. **Submit Goal**
   - "Let's set a goal: Help me reduce stress and improve sleep"

3. **Show Agent Processing**
   - Point out loading states showing each agent working

4. **Review Plans**
   - Navigate through each tab
   - Highlight how agents are aware of each other

5. **Log Progress**
   - Add a sample progress entry
   - Show history building up

## Author

MiniMax Agent - Capstone Project 2025

## Acknowledgments

Built with Google's Agent Development Kit and Gemini models

## Future Enhancements

- [ ] Real calendar integration (Google Calendar API)
- [ ] Mobile responsive PWA
- [ ] Social features (community support)
- [ ] Wearable device integration (Google Fit)
- [ ] Advanced analytics with charts
- [ ] Voice input for daily check-ins
- [ ] Multi-language support (Gemini multilingual)
- [ ] PDF export of plans



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