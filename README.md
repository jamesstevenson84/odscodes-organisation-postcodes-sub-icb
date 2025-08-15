# Brighton Sub-ICB Organisations Finder

This project helps find healthcare Organisations that are part of Brighton's local healthcare system, specifically focusing on Sub-ICB (Integrated Care Board) locations.

## How It Works

### The Search Process

1. **What We're Looking For**
   
   We wanted to find official healthcare Organisations called "Sub-ICB Locations" in the Brighton area. These are local healthcare administrative bodies that help manage NHS services.

2. **Where We Look**
   
   We search across postal codes in Brighton and the surrounding Sussex area (like BN1, BN2, BN3, etc.) to find all healthcare Organisations.

3. **How We Filter**
   
   From all the healthcare Organisations we find (there were thousands!), we keep only the ones that are:
   - Currently active (not closed or historical)
   - Specifically designated as "Sub-ICB Location" in their official role

4. **What We Found**
   
   We discovered three important healthcare administrative bodies:
   - NHS SUSSEX ICB - 70F (located in Worthing, BN11 1DJ)
   - NHS SUSSEX ICB - 09D (located in Brighton, BN3 4AH)
   - NHS SUSSEX ICB - 97R (located in Lewes, BN7 2PB)

   Based on its location in Brighton (BN3), the "NHS SUSSEX ICB - 09D" is likely the main Brighton Sub-ICB organization.

5. **The Output**
   
   We've created a simple list (CSV file) that shows:
   - The official code for each organization (ODS Code)
   - The organization's name
   - Where it's located (postcode)
   - The organization's filtered role type
   - All the organization's roles (as a comma-separated list)

## Why This Matters

This information helps understand how healthcare is organized locally in Brighton. These Sub-ICB Organisations are responsible for planning and coordinating healthcare services in their specific areas, working under the larger Sussex Integrated Care Board.

The identification of these specific Organisations could be useful for anyone needing to contact the right healthcare administrative body in the Brighton area.

## Technical Details

The script uses the NHS ODS (Organisation Data Service) API to search for Organisations by postcode and filters them based on their role designation. It processes data from 58 postcodes in the Brighton and Sussex area.

### How the Script Works

1. **Search Process**: Searches for Organisations using the provided postcode list with the correct API parameter (`searchQueryGeneral`)
2. **Filtering**: Filters results for only Organisations with "Active" status and "SUB ICB LOCATION" role
3. **Data Extraction**: Extracts key fields (ODS Code, Name, Postcode) and role information
4. **Deduplication**: Removes duplicates based on ODS Code as the key
5. **Output**: Saves everything to a CSV file with detailed role information

### Step-by-Step Process

1. It loops over all postcodes in the list (BN1, BN2, etc.)
2. For each postcode, it sends a POST request to the ODS API with `searchQueryGeneral` parameter
3. It filters the results to only include Organisations with "Active" status and appropriate role
4. It stores the ODS Code, Name, and Postcode in the results list
5. It removes duplicate entries using the ODS Code as a key
6. Finally, it writes all unique results to the `brighton_sub_icb_orgs.csv` file

The script found 3 unique Sub-ICB Organisations across all the postcodes, out of thousands of healthcare Organisations in the area.

### Requirements
- Python 3.x
- Requests library (`pip install requests`)

### Local Setup & Running
To set up and run the script locally:

1. Ensure you have Python 3 installed (macOS usually comes with Python 3).
2. Open a terminal and navigate to your project directory:
   ```sh
   cd /Users/jamesstevenson/Documents/python
   ```
3. (Recommended) Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
4. If you have a `requirements.txt` file, install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run the script:
   ```sh
   python3 brighton-sub-icb-orgs.py
   ```

### Running the Script
```bash
python brighton-sub-icb-orgs.py
```

When you run the script, you'll be prompted with:
1. Whether you want to filter by role name (Y/N)
2. If yes, which role name to search for

This allows you to:
- Search for any type of healthcare organization role
- Filter using partial text matches (doesn't need to be an exact match)
- Get all active organizations without role filtering

The output will be saved as `brighton_sub_icb_orgs.csv`.
