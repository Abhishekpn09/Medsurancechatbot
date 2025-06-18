import pyodbc
import county_lookup

cnx = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-6MNJPHEQ;'
    'DATABASE=Medsurance;'
    'Trusted_Connection=yes;'
    'Encrypt=no;'
)

def get_all_plan_types():
    try:
        cursor = cnx.cursor()
        query = "SELECT DISTINCT plan_type FROM Plans"
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"[ERROR] get_all_plan_types: {e}")
        return []

def get_all_locations():
    return list(county_lookup.county_lookup.keys())

def get_plans_by_type_and_location(plan_type, location):
    try:
        county_code = county_lookup.county_lookup.get(location)
        if not county_code:
            return []

        cursor = cnx.cursor()
        query = """
            SELECT plan_id, plan_name
            FROM Plans
            WHERE plan_type = ? AND county_code = ?
        """
        cursor.execute(query, (plan_type, county_code))
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"[ERROR] get_plans_by_type_and_location: {e}")
        return []

def get_plan_by_id(plan_id):
    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM Plans WHERE plan_id = ?"
        cursor.execute(query, (plan_id,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None
    except Exception as e:
        print(f"[ERROR] get_plan_by_id: {e}")
        return None

def get_premium_by_plan(plan_id, age_group, family_type):
    try:
        cursor = cnx.cursor()
        query = """
            SELECT premium, ehb_percent
            FROM PlanPremiums
            WHERE plan_id = ? AND age_group = ? AND family_type = ?
        """
        cursor.execute(query, (plan_id, age_group, family_type))
        result = cursor.fetchone()
        if result:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, result))
        return None
    except Exception as e:
        print(f"[ERROR] get_premium_by_plan: {e}")
        return None

def get_csr_by_plan(plan_id, csr_variant):
    try:
        cursor = cnx.cursor()
        query = """
            SELECT service_type, cost_type, value, unit, applies_after_deductible, unit_time
            FROM PlanCSR
            WHERE plan_id = ? AND csr_variant = ?
        """
        cursor.execute(query, (plan_id, csr_variant))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"[ERROR] get_csr_by_plan: {e}")
        return []

def get_plans_for_criteria(plan_type, county_name, age_group, family_type):
    try:
        county_code = county_lookup.county_lookup.get(county_name)
        if not county_code:
            return []

        cursor = cnx.cursor()
        query = """
            SELECT p.plan_id, p.plan_name, pp.premium, pp.ehb_percent
            FROM Plans p
            JOIN PlanPremiums pp ON p.plan_id = pp.plan_id
            WHERE p.plan_type = ?
              AND p.county_code = ?
              AND pp.age_group = ?
              AND pp.family_type = ?
        """
        cursor.execute(query, (plan_type, county_code, age_group, family_type))
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        print(f"[ERROR] get_plans_for_criteria: {e}")
        return []
