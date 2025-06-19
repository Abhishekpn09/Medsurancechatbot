
The Medsurance Chatbot is organized into modular components that handle data preprocessing, backend logic, Dialogflow integration, and optional frontend capabilities.

pgsql
Copy
Edit
Medsurancechatbot/
│
├── backend/                → FastAPI server handling all Dialogflow webhook requests
├── db/                     → SQL Server database schema and dump
├── frontend/               → (Optional) Static site or client UI
├── dialogflow_assets/      → Intents, entities, training phrases
├── notebooks/              → Jupyter notebooks for data cleaning & ETL

⚙️ Installation & Setup
1️ Python & Dependencies
Install required packages via pip:

bash
Copy
Edit
pip install -r backend/requirements.txt
Or individually:

bash
Copy
Edit
pip install mysql-connector
pip install "fastapi[all]"

2️ Running the Backend Server
To start the FastAPI server:

bash
Copy
Edit
cd backend
uvicorn main:app --reload
This will start the server at http://127.0.0.1:8000/

3️ Setting Up the Database
Import the SQL schema:

Open MySQL Workbench

Use db/DE.sql to create tables and populate sample data

Tables include:

Plans

PlanPremiums

PlanCSR

PlanLocations

Locations

Update database connection info in db_helper.py if needed.

4️ Exposing Webhook with ngrok
If using Dialogflow, you'll need to expose your local backend:

Download ngrok

Unzip and open a terminal in its directory

Run:

bash
Copy
Edit
ngrok http 8000
Copy the https:// URL and paste it into your Dialogflow webhook URL.

Note: ngrok sessions expire. Restart it as needed and update your webhook URL.

 Components Overview
main.py – Webhook logic for handling Dialogflow intents

db_helper.py – Centralized SQL query logic for plans, CSR, premium, etc.

county_lookup.py – Maps user-friendly county names to internal codes

generic_helper.py – Formats responses like currency and lists

Medsurance (1).ipynb & (2).ipynb – Clean and transform raw data from healthcare.gov

DE.sql – SQL dump to set up tables, relationships, and test records

Checklist Before Deployment
 FastAPI server running

 SQL Server database populated

 Dialogflow intents match backend logic

 ngrok running (for public webhook access)

 county codes synced via county_lookup.py

Directory structure
===================
backend: Contains Python FastAPI backend code
db: contains the dump of the database. you need to import this into your MySQL db by using MySQL workbench tool
dialogflow_assets: this has training phrases etc. for our intents
frontend: website code

Install these modules
======================

pip install mysql-connector
pip install "fastapi[all]"

OR just run pip install -r backend/requirements.txt to install both in one shot

To start fastapi backend server
================================
1. Go to backend directory in your command prompt
2. Run this command: uvicorn main:app --reload

ngrok for https tunneling
================================
1. To install ngrok, go to https://ngrok.com/download and install ngrok version that is suitable for your OS
2. Extract the zip file and place ngrok.exe in a folder.
3. Open windows command prompt, go to that folder and run this command: ngrok http 80000

NOTE: ngrok can timeout. you need to restart the session if you see session expired message.
