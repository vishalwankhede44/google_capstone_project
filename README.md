# **MiniMax Wellness Orchestrator**

### *A Multi-Agent AI Wellness Planner Powered by Google Gemini + Tool-Calling*

---

## 🌟 **1. Summary**

MiniMax Wellness Orchestrator is an **AI-powered, multi-agent wellness planning system** designed to deliver personalized recommendations across three key dimensions:

* **Exercise Coaching**
* **Nutrition Planning**
* **Mindfulness & Stress Reduction**

The project demonstrates **agentic reasoning**, **multi-tool orchestration**, **memory-augmented personalization**, and **real-world integrations**.

<img width="2816" height="1536" alt="Gemini_Generated_Image_xd38zqxd38zqxd38" src="https://github.com/user-attachments/assets/ab6edc37-7328-4f68-8e4b-b1326cd1f062" />


Instead of a single monolithic LLM prompt, this system uses a **Chief Wellness Officer (CWO)** agent that delegates tasks to specialized sub-agents. Each agent brings unique domain expertise and uses **shared context**, **profile data**, and **long-term memory** to construct a fully personalized, structured, and safe wellness plan.

---

## 🎯 **2. Problem Motivation**

Wellness apps often fail because they:

1. Provide **generic recommendations**
2. Ignore user **history, preferences, or environment**
3. Lack **continuity**, forgetting the user after each session
4. Cannot adjust based on **weather, schedule, activity level**, or **dietary preferences**

# MiniMax Wellness Orchestrator solves these issues by:

* Maintaining a **persistent user profile**
* Using **domain-specific specialist agents**
* Leveraging **tool calls** for memory, profile, planning, and optional real-world data
* Generating **fully personalized** wellness plans for real users (e.g., “Alice”, “Sarah”)
* Evaluating and adapting recommendations based on goals, constraints, and safety

<img width="2816" height="1536" alt="Gemini_Generated_Image_xd38zqxd38zqxd38 (4)" src="https://github.com/user-attachments/assets/4e839cd6-a211-41eb-933e-0762a81fb244" />

---

## 🏗️ **3. System Architecture**

### **3.1 Core Components**

#### **Chief Wellness Officer (CWO)**

<img width="2816" height="1536" alt="Gemini_Generated_Image_xd38zqxd38zqxd38 (1)" src="https://github.com/user-attachments/assets/0a6caec1-20aa-4281-975d-25ee49073536" />

The central orchestrator responsible for:

* Reading user goals
* Retrieving user profile & memory
* Delegating tasks to specialist agents
* Consolidating & delivering the final plan
* Ensuring safety, realism, and consistency


#### **Specialist Agents**

1. **Nutrition Specialist**

   * Calculates calories & macros
   * Builds daily meal plan templates
   * Applies dietary constraints (Halal, allergies, etc.)
   * Issues safety warnings (e.g., dangerously low BMI)

2. **Exercise Coach**

   * Builds workouts based on goals
   * Understands indoor/outdoor preferences
   * Uses weather (optional MCP)
   * Adjusts difficulty based on fitness level

3. **Mindfulness Specialist**

   * Breathwork (4-7-8 method)
   * Grounding exercises
   * Micro-practices for stress reduction
   * Long-form guided relaxation routines

<img width="2816" height="1536" alt="Gemini_Generated_Image_xd38zqxd38zqxd38 (2)" src="https://github.com/user-attachments/assets/19105a72-55fa-45bd-b516-e7bab1f6c71d" />


#### **Tooling Layer**

* **User Profile Store (SQLite)**
* **Memory Manager**
* **Nutrition Tools**
* **Exercise Tools**
* **Mindfulness Tools**

#### **Optional MCP Integrations**

* Google Calendar MCP
* Weather API MCP
  These allow contextual awareness like:
* Scheduling workouts when the calendar is free
* Providing indoor workouts during rain

---

## 🔄 **4. Agentic Workflow**

## Demo & Example User Journeys

This section walks through three real terminal sessions captured during development. Each shows how the Chief Wellness Officer (CWO) orchestrates specialists, updates memory/profile, asks clarifying questions, respects safety limits, and produces actionable, human-readable plans.

## Session A — Bob: Full 7-Day Plan (Goal: Reduce weight; constraints: sedentary, vegetarian, indoor, focus)

### User input: Hi, I'm Bob. Can you make me a full 7-day plan for my health, with meals, workouts, and mindfulness?

User then clarifies: plan to reduce weight, no activity, veg, indoor, focus


<img width="1073" height="773" alt="Screenshot 2025-11-29 at 1 24 51 AM" src="https://github.com/user-attachments/assets/69909bf4-7960-4753-a053-debcfd4d4d36" />

<img width="1073" height="779" alt="Screenshot 2025-11-29 at 1 25 10 AM" src="https://github.com/user-attachments/assets/bc655ad8-1dad-4682-9343-0651844f990f" />

<img width="1073" height="699" alt="Screenshot 2025-11-29 at 1 25 30 AM" src="https://github.com/user-attachments/assets/f7a5ccac-9a4f-40fb-ae93-ea531b606906" />




Key behaviors shown:

1. CWO retrieved profile & memories, then asked 5 short clarifying questions (goal, activity, diet, workout preference, mindfulness focus).
2. Profile was updated (name = Bob; goals and preferences stored).
3. System flagged a safety concern (weight 30kg at 158cm) and issued a strong recommendation to consult a healthcare professional before any weight-focused plans.
4. Specialists were invoked in parallel: nutrition_specialist, exercise_coach, mindfulness_orchestrator.
5. CWO merged specialist outputs into an integrated plan emphasizing nourishment and safety rather than aggressive weight loss.





## Session B — David: Safe Beginner Plan for Low Energy (Goal: increase energy; age update)

### User input: I'm David, I’m 45 and not very active. I feel low on energy. Can you help me start safely?


<img width="1073" height="764" alt="Screenshot 2025-11-29 at 1 25 49 AM" src="https://github.com/user-attachments/assets/7c3bbe2b-d231-4315-840f-12bf7ece912a" />

<img width="1073" height="771" alt="Screenshot 2025-11-29 at 1 26 06 AM" src="https://github.com/user-attachments/assets/d2e8440a-8aba-402b-b07e-9840bda6ba70" />

<img width="1073" height="771" alt="Screenshot 2025-11-29 at 1 26 19 AM" src="https://github.com/user-attachments/assets/3bd85540-c5bf-4f57-9eb1-94b913eec703" />


<img width="1073" height="771" alt="Screenshot 2025-11-29 at 1 26 31 AM" src="https://github.com/user-attachments/assets/95ebc8d5-28f7-4055-8aba-74c981627f79" />


<img width="1073" height="735" alt="Screenshot 2025-11-29 at 1 26 56 AM" src="https://github.com/user-attachments/assets/65c286f8-f495-42d8-b954-fee92ae9991d" />



Key behaviors shown:

1. CWO accepts new identity (profile updated to David, age 45).
2. Re-affirmed the urgent health advisory because same low weight remains in profile.
3. Asked a few targeted clarifying questions (activity specifics, dietary confirmation, timing/time commitment).
4. When the user reports “no constraints” and “low energy,” CWO runs specialists and returns a gentle, safe starter plan:
5. 20-minute indoor sessions, 3 days/week (brisk walking, gentle cardio, gentle circuit).
6. Mindfulness: 4-7-8 breathing and body scan suggested.
7. Nutrition: general, non-prescriptive guidance (nutrient-dense vegetarian foods, small frequent meals).


## User input (short): Yes, start the 4-7-8 breathing exercise → After guided rounds user replies: bad

<img width="1073" height="769" alt="Screenshot 2025-11-29 at 1 27 13 AM" src="https://github.com/user-attachments/assets/474049a0-49fa-4fc2-8ad4-133a858da718" />


<img width="1073" height="626" alt="Screenshot 2025-11-29 at 1 27 32 AM" src="https://github.com/user-attachments/assets/e0b9e39c-13d5-45e2-bfd6-e8b1148d8992" />




Key behaviors shown:

1. Mindfulness specialist produced a calm, guided 4-7-8 script (several cycles).
2. User reported feeling bad after the breathing exercise.
3. Agent switches to safety mode immediately:
4. Acknowledgement and empathy: “I’m sorry you’re feeling bad…”
5. Strong recommendation to consult a doctor and registered dietitian immediately.
6. Agent refused to continue with prescriptive plans until a professional assessment is completed.

Tools used for this flow: mindfulness_orchestrator, get_user_profile, update_user_profile, remember_user_insight.



---

## ⚙️ **5. Implementation Overview**

### **Tech Stack**

* Python
* FastAPI (optional API mode)
* Google ADK
* Gemini models (Flash/Pro)
* SQLite for profile & memory
* Optional MCPs:
  * Google Calendar
  * Weather API
 <img width="2816" height="1536" alt="Gemini_Generated_Image_xd38zqxd38zqxd38 (3)" src="https://github.com/user-attachments/assets/05aa855e-74fe-4890-b567-9142081f3b3b" />

    

### **Key Files**

* `cwo_agent.py` – main orchestrator
* `exercise_agent.py`, `exercise_tools.py`
* `nutrition_agent.py`, `nutrition_tools.py`
* `mindfulness_agent.py`, `mindfulness_tools.py`
* `user_profile_store.py`
* `user_memory_manager.py`

---

## 🧪 **6. Evaluation & Results**

### **Latency Observations**

| Operation                        | Time      |
| -------------------------------- | --------- |
| Profile retrieval                | ~0.5–1s   |
| Multi-agent orchestration        | 6–20s     |
| Mindfulness long-form generation | up to 70s |

### **Qualitative Evaluation**

| Criteria                 | Score (1–5) |
| ------------------------ | ----------- |
| Personalization          | 5           |
| Safety                   | 5           |
| Clarity of Plans         | 4           |
| Realism                  | 4           |
| Context Use              | 5           |
| Multi-Agent Coordination | 5           |


<img width="2816" height="1536" alt="Gemini_Generated_Image_xd38zqxd38zqxd38 (5)" src="https://github.com/user-attachments/assets/54692be5-a7b9-42a8-bc8a-957b9caa52b6" />


### **Safety Behaviors Observed**

* Low BMI → nutrition warning
* No unsupported medical claims
* Exercise difficulty adapted to fitness level
* Stress routines validated and explained

---


## 🚀 **7. Future Enhancements**

* Parallelized agent calls
* Wearable device integration (Fitbit, Apple Health)
* Mood detection via text sentiment
* Weekly progress tracking
* Mobile-friendly UI
* Recipe generation with macros
* Auto-scheduling using real calendars

---

## 🧩 **8. Quickstart (Direct Mode)**

```bash
python main.py --mode direct
```

Tools automatically:

* Load user profile
* Retrieve memories
* Run specialist agents
* Produce final plan
