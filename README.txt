Project Overview: Medsurance Chatbot
Medsurance is an AI-powered conversational assistant designed to simplify the often overwhelming process of exploring health insurance plans in the U.S. Through natural language interaction, users can search for plans, get premium estimates, view plan details, and track their application — all using a friendly chatbot interface.

🗂️ Project Structure (Explained)
The project is modular and organized into folders, each with a clear purpose:

backend/ – This is the heart of your chatbot logic. It contains a FastAPI server that acts as the webhook for Dialogflow. It processes user queries, interacts with the database, and formats responses.

db/ – Contains a SQL file (DE.sql) that defines your database schema and includes sample data. This needs to be imported into SQL Server to support chatbot queries.

dialogflow_assets/ – This folder includes training data (intents, phrases, entities) that can be imported directly into Dialogflow, enabling the chatbot to understand user inputs.

frontend/ (optional) – Can be used to develop a visual web interface, though the chatbot functions independently of it.

notebooks/ – Jupyter notebooks used at the beginning of the project for data cleaning and transforming datasets downloaded from healthcare.gov.

⚙️ Setting Up the Environment
🔹 Install Required Packages
To ensure all Python dependencies are available:

bash
Copy
Edit
pip install -r backend/requirements.txt
Or install them manually:

fastapi – for building APIs

uvicorn – for running the FastAPI app

mysql-connector – to connect Python to SQL Server (or MySQL)

🚀 Running the Backend (FastAPI)
This is how your chatbot backend gets started:

Open your terminal or command prompt

Navigate to the backend directory:

bash
Copy
Edit
cd backend
Run the API server using:

bash
Copy
Edit
uvicorn main:app --reload
Once started, it will be available at:
📍 http://127.0.0.1:8000/

🗃️ Setting Up the Database
To store and retrieve plan data, your chatbot relies on SQL Server. Here's how to set it up:

Open MySQL Workbench or SQL Server Management Studio

Load the SQL dump file located at:

pgsql
Copy
Edit
db/DE.sql
This will create the necessary tables:

Plans

PlanPremiums

PlanCSR

PlanLocations

Locations

Make sure the database connection settings in db_helper.py match your local SQL setup.

🌍 Connecting to Dialogflow
Dialogflow (ES or CX) is used to define how your bot understands user input.

Since Dialogflow requires a public URL, you’ll need to expose your FastAPI server using ngrok.

🔹 Steps to Run ngrok
Download from https://ngrok.com/download

Extract and place ngrok.exe somewhere accessible

Run this command in terminal:

bash
Copy
Edit
ngrok http 8000
You’ll get a temporary https:// URL. Use this as the webhook URL in Dialogflow.

📝 Note: ngrok sessions expire — when they do, re-run the command and update the webhook URL in Dialogflow.

🧠 Dialogflow AI Setup
Dialogflow handles user inputs via:

Intents
Intent Name	What It Does
plan.search	Search plans by type and county
provide.agegroup	User specifies age group
provide.familytype	User specifies family situation (e.g., individual + kids)
plan.details	Gets metadata for a plan ID
plan.premium	Returns premium and EHB %
plan.csr	Displays CSR (cost-sharing reduction) details
AddPlanToOrder	Adds a plan to the user’s "cart"
RemovePlanFromOrder	Removes a plan from the cart
View-SelectedPlans	Lists all selected plans
ConfirmPlanSelection	Confirms final submission of plans
TrackPlanApplication	Tracks plan using application ID

Entities
These help Dialogflow match user phrases:

plan-type: PPO, HMO, etc.

location: U.S. counties (e.g., Autauga, Baldwin)

age_group: e.g., "30-34"

family_type: e.g., "Individual+2 children"

plan-id: 14-character alphanumeric string

application_id: Tracking number for application

✅ Final Checklist
Before testing the full experience:

✅ FastAPI server is running

✅ SQL database is correctly loaded

✅ Webhook is connected to Dialogflow via ngrok

✅ Entities and intents are imported into Dialogflow
