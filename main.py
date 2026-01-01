import os
import time
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.hubapi.com"

# --- Required: 200ms delay between EVERY API call ---
LAST_CALL_TS = 0.0
def rate_limited_request(method: str, path: str, token: str, json_body=None):
    global LAST_CALL_TS
    now = time.time()
    wait = 0.2 - (now - LAST_CALL_TS)
    if wait > 0:
        time.sleep(wait)

    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.request(method, url, headers=headers, json=json_body, timeout=30)
    LAST_CALL_TS = time.time()

    if not resp.ok:
        raise RuntimeError(
            f"HubSpot API error {resp.status_code} on {method} {path}: {resp.text}"
        )

    # Some endpoints return 204 No Content
    if resp.status_code == 204 or not resp.text:
        return None
    return resp.json()


def pick_employee_or_member_label(labels_response: dict):
    """
    HubSpot v4 labels endpoint returns something like:
    {
      "results":[
        {"category":"HUBSPOT_DEFINED","typeId":279,"label":null},
        {"category":"USER_DEFINED","typeId":550,"label":"Employee", ...},
        ...
      ]
    }
    We try to find a label containing "employee" or "member".
    """
    results = (labels_response or {}).get("results", [])
    for r in results:
        label = (r.get("label") or "").strip().lower()
        if "employee" in label or "member" in label:
            return {"associationCategory": r.get("category"), "associationTypeId": r.get("typeId")}
    return None


def main():
    load_dotenv()

    token = os.getenv("HUBSPOT_KEY")
    firstname = os.getenv("FIRSTNAME")
    lastname = os.getenv("LASTNAME")

    if not token:
        raise SystemExit("Missing HUBSPOT_KEY in .env")
    if not firstname or not lastname:
        raise SystemExit("Missing FIRSTNAME and/or LASTNAME in .env")

    # --- Step 2: Create a Contact ---
    # Replace these with your real first/last name for the challenge.
    contact_payload = {
        "properties": {
            "email": "candidate.test@coding-challenge-company.com",
            "firstname": firstname,
            "lastname": lastname,
        }
    }

    contact = rate_limited_request(
        "POST",
        "/crm/v3/objects/contacts",
        token,
        json_body=contact_payload,
    )
    contact_id = contact["id"]
    print(f"✅ Created contact: {contact_id}")

    # --- Step 3: Create a Company ---
    company_payload = {
        "properties": {
            "name": "Coding Challenge Company GmbH",
            "domain": "coding-challenge-company.com",
        }
    }

    company = rate_limited_request(
        "POST",
        "/crm/v3/objects/companies",
        token,
        json_body=company_payload,
    )
    company_id = company["id"]
    print(f"✅ Created company: {company_id}")

    # --- Step 4: Create an Association (employee/member) ---
    # First: discover labels available between contact<->company
    labels = rate_limited_request(
        "GET",
        "/crm/v4/associations/contact/company/labels",
        token,
        json_body=None,
    )

    label_def = pick_employee_or_member_label(labels)

    if label_def:
        # Associate WITH a label
        assoc_body = [label_def]
        rate_limited_request(
            "PUT",
            f"/crm/v4/objects/contact/{contact_id}/associations/company/{company_id}",
            token,
            json_body=assoc_body,
        )
        print(f"✅ Associated using label: {label_def}")
    else:
        # Fallback: default unlabeled association
        rate_limited_request(
            "PUT",
            f"/crm/v4/objects/contact/{contact_id}/associations/default/company/{company_id}",
            token,
            json_body=None,
        )
        print("✅ Associated using default (unlabeled) contact↔company association")

    print("\nDone.")


if __name__ == "__main__":
    main()

