import requests
import csv
import time
import json

# API URL for ODS data search
API_URL = "https://www.odsdatasearchandexport.nhs.uk/api/search/organisationGeneralSearch"

# List of postcodes provided by the user - fix spaces to match the API format
postcodes = [
    "BN1", "BN2", "BN3", "BN4", "BN5", "BN6", "BN7", "BN8", "BN9",
    "BN10 7", "BN10 8", "BN10 9", "BN11 2", "BN14 0", "BN14 7", "BN14 8", "BN14 9",
    "BN15 0", "BN15 5", "BN15 8", "BN15 9", "BN21 4", "BN25 2", "BN26 5", "BN26 6",
    "BN41 1", "BN41 2", "BN41 9", "BN42 4", "BN43 5", "BN43 6", "BN43 9",
    "BN44 3", "BN44 4", "BN45 7", "BN50 8", "BN50 9", "BN51 9", "BN52 9",
    "BN88 1", "BN88 3", "BN88 4", "BN95 1", "BN99 6", "BN99 8", "BN99 9",
    "PO22 7", "RH11 9", "RH13 8", "RH15 0", "RH15 5", "RH15 8", "RH15 9",
    "RH16 4", "RH17 5", "RH17 6", "RH17 7", "TN22 5"
]

results = []

# Define constants for field names to avoid duplication
ODS_CODE = "ODS Code"
NAME = "Name"
POSTCODE = "Postcode"

print(f"Searching for SUB ICB LOCATION organizations in {len(postcodes)} postcodes...")

# For tracking our findings
sub_icb_count = 0

# Process each postcode
for pc in postcodes:
    print(f"Searching postcode: {pc}")
    
    # Create payload for API request - using searchQueryGeneral as shown in example
    payload = {
        "searchQueryGeneral": pc,
        "offset": 0,
        "batchSize": 2000
    }
    
    try:
        # Send the POST request to the API
        resp = requests.post(API_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()
        
        # Print raw response for debugging (first postcode only)
        if pc == postcodes[0]:
            print(f"Example API response for {pc}: {json.dumps(data)[:500]}...")
        
        # Process organizations based on the response structure
        if "orgArray" in data:
            orgs_found = len(data["orgArray"])
            print(f"Found {orgs_found} organizations for {pc}")
            
            # Process each organization
            for org in data["orgArray"]:
                # Only include active organizations with SUB ICB LOCATION role
                is_active = org.get("status") == "Active"
                role_names = org.get("roleName", [])
                
                # Check if "SUB ICB LOCATION" or "ICB" is in the roleName list (case-insensitive)
                is_sub_icb = any(role and "SUB ICB LOCATION" in role.upper() for role in role_names)
                is_icb = any(role and role.upper() == "ICB" for role in role_names)
                
                if is_active and (is_sub_icb or is_icb):
                    # Add this organization to our results
                    sub_icb_count += 1
                    role_type = "ICB" if is_icb else "SUB ICB LOCATION"
                    print(f"  Found {role_type}: {org.get('name')} (ODS: {org.get('id')})")
                    results.append({
                        ODS_CODE: org.get("id", ""),
                        NAME: org.get("name", ""),
                        POSTCODE: org.get("postcode", ""),
                        "Role": role_type
                    })
        else:
            print(f"No organizations found for {pc}")
            
        # Be kind to the API
        time.sleep(0.2)
    except requests.RequestException as e:
        print(f"Error fetching {pc}: {e}")

# Remove duplicates based on ODS Code
unique_results = {item[ODS_CODE]: item for item in results}.values()

# Save to CSV
with open("brighton_sub_icb_orgs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[ODS_CODE, NAME, POSTCODE, "Role"])
    writer.writeheader()
    writer.writerows(unique_results)

print(f"Found {sub_icb_count} total SUB ICB LOCATION organizations")
print(f"Saved {len(unique_results)} unique organisations with SUB ICB LOCATION role to brighton_sub_icb_orgs.csv")
