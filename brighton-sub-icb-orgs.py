import requests
import csv
import time
import json
import sys

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

# Define constant for the SUB ICB LOCATION role
SUB_ICB_ROLE = "SUB ICB LOCATION"

# Ask user if they want to filter by roleName
filter_by_role = input("Do you want to filter by role name? (Y/N): ").strip().upper() == "Y"

if filter_by_role:
    print(f"Common role names include: '{SUB_ICB_ROLE}', 'GP PRACTICE', 'PHARMACY', 'HOSPITAL', etc.")
    role_filter = input("Enter the role name to search for: ").strip()
    print(f"Filtering for active organizations with role: {role_filter}")
else:
    role_filter = None
    print("No role filter applied - will return all active organizations (inactive organizations will be excluded)")

results = []

# Define constants for field names to avoid duplication
ODS_CODE = "ODS Code"
NAME = "Name"
POSTCODE = "Postcode"
ROLE_NAMES = "Role Names"
ROLE_TYPE = "Role Type"

# Set message based on filtering option
if filter_by_role:
    print(f"Searching for active organizations with role '{role_filter}' in {len(postcodes)} postcodes...")
else:
    print(f"Searching for all active organizations in {len(postcodes)} postcodes...")

# For tracking our findings
found_count = 0

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
                # Check if the organization is active - we only include active organizations
                is_active = org.get("status") == "Active"
                
                # Skip any inactive organizations
                if not is_active:
                    continue
                
                should_include = True
                role_type = ""
                
                # If we need to filter by role name
                if filter_by_role:
                    role_names = org.get("roleName", [])
                    
                    # Special case for SUB ICB LOCATION and ICB roles
                    if role_filter.upper() == SUB_ICB_ROLE.upper():
                        # Check for SUB ICB LOCATION or ICB in the role names
                        is_sub_icb = any(role and SUB_ICB_ROLE.upper() in role.upper() for role in role_names)
                        is_icb = any(role and role.upper() == "ICB" for role in role_names)
                        should_include = is_sub_icb or is_icb
                        role_type = "ICB" if is_icb else SUB_ICB_ROLE
                    else:
                        # For any other role filter, check for partial matches in the role names
                        matched_roles = [role for role in role_names if role and role_filter.upper() in role.upper()]
                        should_include = len(matched_roles) > 0
                        # Use the first matching role as the role_type for display
                        role_type = matched_roles[0] if matched_roles else role_filter
                    
                # If all checks pass, include this organization
                if should_include:
                    found_count += 1
                    if not role_type:
                        role_type = "Active"
                        
                    # Get the full list of role names as a comma-separated string
                    role_names_list = org.get("roleName", [])
                    role_names_str = ", ".join(role_names_list) if role_names_list else ""
                    
                    print(f"  Found {role_type}: {org.get('name')} (ODS: {org.get('id')})")
                    results.append({
                        ODS_CODE: org.get("id", ""),
                        NAME: org.get("name", ""),
                        POSTCODE: org.get("postcode", ""),
                        ROLE_TYPE: role_type,
                        ROLE_NAMES: role_names_str
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
    writer = csv.DictWriter(f, fieldnames=[ODS_CODE, NAME, POSTCODE, ROLE_TYPE, ROLE_NAMES])
    writer.writeheader()
    writer.writerows(unique_results)

if filter_by_role:
    print(f"Found {found_count} total organizations with '{role_filter}' role")
    print(f"Saved {len(unique_results)} unique organizations with '{role_filter}' role to brighton_sub_icb_orgs.csv")
else:
    print(f"Found {found_count} total active organizations")
    print(f"Saved {len(unique_results)} unique active organizations to brighton_sub_icb_orgs.csv")
