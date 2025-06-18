from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import time

app = FastAPI()
user_sessions = {}

@app.get("/")
async def root():
    return {"message": "API is running."}

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    query_result = payload.get("queryResult", {})
    intent = query_result.get("intent", {}).get("displayName", None)
    parameters = query_result.get("parameters", {})
    session_id = payload.get("session", "default_session")

    if session_id not in user_sessions:
        user_sessions[session_id] = {
            'last_intent': None,
            'last_query': None,
            'last_active': time.time(),
            'selected_plans': [],
            'plan_type': None,
            'location': None,
            'age_group': None,
            'last_viewed_plan_id': None
        }

    user_sessions[session_id]['last_active'] = time.time()

    intent_handler_dict = {
        'plan.search': lambda p: search_plan(p, session_id),
        'provide.agegroup': lambda p: provide_agegroup(p, session_id),
        'provide.familytype': lambda p: provide_familytype(p, session_id),
        'plan.details': lambda p: get_plan_details(p, session_id),
        'plan.premium': lambda p: get_plan_premium(p),
        'plan.csr': lambda p: get_csr_details(p),
        'AddPlanToOrder': lambda p: add_plan_to_order(p, session_id),
        'RemovePlanFromOrder': lambda p: remove_plan_from_order(p, session_id),
        'View-SelectedPlans': lambda p: view_selected_plans(p, session_id),
        'ConfirmPlanSelection': lambda p: confirm_plan_selection(p, session_id),
        'TrackPlanApplication': lambda p: track_plan_application(p)
    }

    if intent in intent_handler_dict:
        user_sessions[session_id]['last_intent'] = intent
        return intent_handler_dict[intent](parameters)

    return JSONResponse(content={"fulfillmentText": "Sorry, I didn't understand your request."})

def search_plan(parameters, session_id):
    plan_type = parameters.get("plan-type", "").strip()
    location = parameters.get("location", "").strip()

    if ":" in plan_type:
        plan_type = plan_type.split(":")[0].strip()

    valid_plan_types = db_helper.get_all_plan_types()
    valid_locations = db_helper.get_all_locations()

    if plan_type not in valid_plan_types:
        return JSONResponse(content={"fulfillmentText": f"Plan type '{plan_type}' is not available."})
    if location not in valid_locations:
        return JSONResponse(content={"fulfillmentText": f"Location '{location}' is not available."})

    user_sessions[session_id]['plan_type'] = plan_type
    user_sessions[session_id]['location'] = location

    return JSONResponse(content={"fulfillmentText": "Got it! Please provide your age group."})

def provide_agegroup(parameters, session_id):
    age_group = parameters.get("age_group")
    user_sessions[session_id]['age_group'] = age_group
    return JSONResponse(content={"fulfillmentText": "Great! Now please provide your family type."})

def provide_familytype(parameters, session_id):
    family_type = parameters.get("family_type")
    session = user_sessions[session_id]
    plan_type = session.get("plan_type")
    location = session.get("location")
    age_group = session.get("age_group")

    if not all([plan_type, location, age_group, family_type]):
        return JSONResponse(content={"fulfillmentText": "Missing required info to search plans."})

    plans = db_helper.get_plans_for_criteria(plan_type, location, age_group, family_type)

    if not plans:
        return JSONResponse(content={"fulfillmentText": "No plans found matching your criteria."})

    plan = plans[0]
    return JSONResponse(content={
        "fulfillmentText": f"Plan: {plan['plan_name']} (ID: {plan['plan_id']}), "
                           f"Premium: ${plan['premium']}, EHB: {plan['ehb_percent']}%"
    })

def get_plan_details(parameters, session_id):
    plan_id = parameters.get("plan-id")
    plan = db_helper.get_plan_by_id(plan_id)

    if not plan:
        return JSONResponse(content={"fulfillmentText": f"No details found for plan ID {plan_id}."})

    user_sessions[session_id]['last_viewed_plan_id'] = plan_id

    response_text = (
        f"\U0001F4D8 Plan Name: {plan['plan_name']}\n"
        f"\U0001F3E2 Issuer: {plan['issuer_name']}\n"
        f"\U0001F48E Level: {plan['meta_level']}\n"
        f"\U0001F4CB Type: {plan['plan_type']}"
    )

    brochure_url = plan.get("benifits_summary_url")
    if brochure_url:
        response_text += f'\n\U0001F4C4 <a href="{brochure_url}" target="_blank">Click here to view the plan brochure</a>'

    return JSONResponse(content={"fulfillmentText": response_text})

def get_plan_premium(parameters):
    plan_id = parameters.get("plan-id")
    age_group = parameters.get("age_group")
    family_type = parameters.get("family_type")

    if not all([plan_id, age_group, family_type]):
        return JSONResponse(content={"fulfillmentText": "To show you a premium, I need more info. You can say: Please include a plan ID, age group, and family type."})

    premium_info = db_helper.get_premium_by_plan(plan_id, age_group, family_type)
    if premium_info:
        return JSONResponse(content={"fulfillmentText": (
            f"The premium for {family_type} in {age_group} is ${premium_info['premium']} "
            f"with an EHB percent of {premium_info['ehb_percent']}%."
        )})
    return JSONResponse(content={"fulfillmentText": "No premium info found for this plan configuration."})

def get_csr_details(parameters):
    plan_id = parameters.get("plan-id")
    csr_variant = parameters.get("plan-csr")

    csr_rows = db_helper.get_csr_by_plan(plan_id, csr_variant)
    if not csr_rows:
        return JSONResponse(content={"fulfillmentText": "No CSR details found for that plan and variant."})

    formatted = "\n".join([
        f"{row['service_type']} ({row['cost_type']}): {row['value']} {row['unit']} "
        f"{'- After Deductible' if row['applies_after_deductible'] else ''} {row['unit_time'] or ''}".strip()
        for row in csr_rows
    ])

    return JSONResponse(content={"fulfillmentText": f"CSR Details for {csr_variant}:\n{formatted}"})

def add_plan_to_order(parameters, session_id):
    plan_id = parameters.get("plan-id") or user_sessions[session_id].get('last_viewed_plan_id')
    if not plan_id:
        return JSONResponse(content={"fulfillmentText": "Please provide the plan ID to add."})

    plan = db_helper.get_plan_by_id(plan_id)
    plan_name = plan.get("plan_name", f"Plan {plan_id}") if plan else f"Plan {plan_id}"

    user_sessions[session_id]['selected_plans'].append({
        'plan_id': plan_id,
        'plan_name': plan_name
    })
    return JSONResponse(content={"fulfillmentText": f"{plan_name} added to your selection."})

def remove_plan_from_order(parameters, session_id):
    plan_id = parameters.get("plan-id")
    plans = user_sessions[session_id].get('selected_plans', [])
    updated = [p for p in plans if p['plan_id'] != plan_id]
    user_sessions[session_id]['selected_plans'] = updated
    return JSONResponse(content={"fulfillmentText": f"Plan {plan_id} removed."})

def view_selected_plans(parameters, session_id):
    plans = user_sessions[session_id].get('selected_plans', [])
    if not plans:
        return JSONResponse(content={"fulfillmentText": "You haven't selected any plans yet."})
    text = '\n'.join([f"- {p['plan_name']} (ID: {p['plan_id']})" for p in plans])
    return JSONResponse(content={"fulfillmentText": f"Your selected plans:\n{text}"})

def confirm_plan_selection(parameters, session_id):
    plans = user_sessions[session_id].get('selected_plans', [])
    if not plans:
        return JSONResponse(content={"fulfillmentText": "No plans selected to submit."})
    return JSONResponse(content={"fulfillmentText": "Plans submitted successfully."})

def track_plan_application(parameters):
    application_id = parameters.get("application_id", "N/A")
    return JSONResponse(content={"fulfillmentText": f"Application ID {application_id} is under review."})

