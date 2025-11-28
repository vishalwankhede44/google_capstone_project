# Run Commands

This file contains common commands to run the project components from the project root (`/Users/vishalwankhede/GoogleAiAgents/capstone project`). Replace placeholder values where needed.

---

## 1) Run `deploy-remote` (list available deployments)

Use this to list deployments. Run from the project root so imports resolve.

Without Poetry (recommended):

```bash
cd "/Users/vishalwankhede/GoogleAiAgents/capstone project"
PYTHONPATH=. python -m deployment.remote --list --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

With Poetry (if you have Poetry installed):

```bash
cd "/Users/vishalwankhede/GoogleAiAgents/capstone project"
poetry run deploy-remote --list --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

---

## 2) Create a remote deployment

```bash
cd "/Users/vishalwankhede/GoogleAiAgents/capstone project"
PYTHONPATH=. python -m deployment.remote --create --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

If you need to pass additional flags, append them to the command (for example `--resource_id`, `--session_id`, `--send`, `--message`).

---

## 3) Cleanup (remove deployment)

The project defines a cleanup entrypoint for tearing down deployments. Run similarly:

```bash
# Without Poetry
PYTHONPATH=. python -m deployment.cleanup --resource_id=RESOURCE_ID --project_id=gen-lang-client-0449050593 --location=us-central1

# With Poetry
poetry run cleanup --resource_id=RESOURCE_ID --project_id=gen-lang-client-0449050593 --location=us-central1
```

(Replace `RESOURCE_ID` with the deployment id returned when you created the deployment.)

---

## 4) Run ADK web UI for agents

Run ADK from the project root. ADK expects an agent directory (e.g., `wellness`) containing a `root_agent` export or `root_agent.yaml`.

```bash
cd "/Users/vishalwankhede/GoogleAiAgents/capstone project"
adk web wellness
```

Note: If you previously ran `adk web` from inside the agent folder, run it instead from the parent directory so the loader can locate your agents.

---

## 5) Create a virtualenv and install dependencies (recommended)

Run these once to prepare a clean environment:

```bash
cd "/Users/vishalwankhede/GoogleAiAgents/capstone project"
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Install packages needed by deployment scripts
pip install absl-py vertexai google-cloud-aiplatform python-dotenv pydantic cloudpickle requests google-adk
```

After this, run the `PYTHONPATH=. python -m ...` commands shown above.

---

## 6) Load environment variables from `.env`

If you keep config in `wellness/.env`, load it into the shell before running commands that depend on it:

```bash
cd "/Users/vishalwankhede/GoogleAiAgents/capstone project"
set -a; source wellness/.env; set +a
PYTHONPATH=. python -m deployment.remote --list
```

---

## 7) Troubleshooting

- `ModuleNotFoundError: No module named 'absl'` → install `absl-py` into your current environment.
- `403 ... storage.buckets.get` → verify the bucket exists and your active GCP credentials (service account or user) have permissions on the bucket.
- If imports fail, ensure you run from the project root or set `PYTHONPATH=.`.

---

If you want this file in a different location or want me to add more specific example flags/arguments, tell me which commands to include and I'll update the file.

---

## Detailed `deployment/remote.py` Actions

The `deployment/remote.py` script implements multiple mutually-exclusive actions. Use only one of the boolean flags at a time. Below are examples for each supported action.

- Create a new remote deployment (wraps the local `wellness` agent and deploys it):

```bash
PYTHONPATH=. python -m deployment.remote --create --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

- List all remote deployments:

```bash
PYTHONPATH=. python -m deployment.remote --list --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

- Delete an existing deployment (use the `resource_id` printed when you created the deployment):

```bash
PYTHONPATH=. python -m deployment.remote --delete --resource_id=projects/PROJECT/locations/LOCATION/agentEngines/RESOURCE_ID --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

- Create a new session for a user on a deployment:

```bash
PYTHONPATH=. python -m deployment.remote --create_session --resource_id=projects/PROJECT/locations/LOCATION/agentEngines/RESOURCE_ID --user_id=test_user --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

- List sessions for a user on a deployment:

```bash
PYTHONPATH=. python -m deployment.remote --list_sessions --resource_id=projects/PROJECT/locations/LOCATION/agentEngines/RESOURCE_ID --user_id=test_user --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

- Get details for a specific session:

```bash
PYTHONPATH=. python -m deployment.remote --get_session --resource_id=projects/PROJECT/locations/LOCATION/agentEngines/RESOURCE_ID --session_id=SESSION_ID --user_id=test_user --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

- Send a message to a session (streams and prints responses):

```bash
PYTHONPATH=. python -m deployment.remote --send --resource_id=projects/PROJECT/locations/LOCATION/agentEngines/RESOURCE_ID --session_id=SESSION_ID --user_id=test_user --message "Hello, can you give me a 3-day workout plan?" --project_id=gen-lang-client-0449050593 --location=us-central1 --bucket=gs://wellness-bucket-281125
```

Notes:
- Replace `projects/PROJECT/locations/LOCATION/agentEngines/RESOURCE_ID` and `SESSION_ID` with real values returned by the create/list commands.
- The script reads `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_CLOUD_STAGING_BUCKET` from environment variables if `--project_id`, `--location`, or `--bucket` are not supplied.

---

## Concrete examples (use your deployment)

You provided this resource id: `4897994448253747200` and the full resource name returned by the API is:
`projects/137466749380/locations/us-central1/reasoningEngines/4897994448253747200`

Note: the resource's project id (`137466749380`) differs from the `gen-lang-client-0449050593` project id used elsewhere in examples. Use the project id that the API returned when calling actions on this resource.

Use these exact commands (run from the project root). Replace `SESSION_ID` when required.

- Create a session (prints the new Session ID):

```bash
PYTHONPATH=. python -m deployment.remote \
	--create_session \
	--resource_id=projects/137466749380/locations/us-central1/reasoningEngines/4897994448253747200 \
	--user_id=test_user \
	--project_id=137466749380 \
	--location=us-central1 \
	--bucket=gs://wellness-bucket-281125
```

- List sessions for the user `test_user`:

```bash
PYTHONPATH=. python -m deployment.remote \
	--list_sessions \
	--resource_id=projects/137466749380/locations/us-central1/reasoningEngines/4897994448253747200 \
	--user_id=test_user \
	--project_id=137466749380 \
	--location=us-central1 \
	--bucket=gs://wellness-bucket-281125
```

- Get session details (replace `SESSION_ID`):

```bash
PYTHONPATH=. python -m deployment.remote \
	--get_session \
	--resource_id=projects/137466749380/locations/us-central1/reasoningEngines/4897994448253747200 \
	--session_id=SESSION_ID \
	--user_id=test_user \
	--project_id=137466749380 \
	--location=us-central1 \
	--bucket=gs://wellness-bucket-281125
```

- Send a message to a session (replace `SESSION_ID`):

```bash
PYTHONPATH=. python -m deployment.remote \
	--send \
	--resource_id=projects/137466749380/locations/us-central1/reasoningEngines/4897994448253747200 \
	--session_id=SESSION_ID \
	--user_id=test_user \
	--message "Hello — give me a 3-day beginner workout plan." \
	--project_id=137466749380 \
	--location=us-central1 \
	--bucket=gs://wellness-bucket-281125
```

- Delete the deployment (use with care):

```bash
PYTHONPATH=. python -m deployment.remote \
	--delete \
	--resource_id=projects/137466749380/locations/us-central1/reasoningEngines/4897994448253747200 \
	--project_id=137466749380 \
	--location=us-central1 \
	--bucket=gs://wellness-bucket-281125
```
