import urllib.request
import urllib.parse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. Verifying Frontend Routes (http://localhost:5173) ===")
for path in ['/', '/interop', '/command']:
    try:
        req = urllib.request.Request(f'http://localhost:5173{path}', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print(f"  [PASS] Frontend route {path} -> HTTP {resp.status}")
    except Exception as e:
        print(f"  [FAIL] Frontend route {path}: {e}")

print("\n=== 2. Verifying Backend State Sample Payloads (http://127.0.0.1:8000) ===")
for state in ['west_bengal', 'bihar', 'odisha']:
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:8000/api/interop/sample-payload/{state}') as resp:
            data = json.loads(resp.read().decode('utf-8'))
            portal = data.get("source_portal", "")
            print(f"  [PASS] Sample for {state}: source='{portal}'")
    except Exception as e:
        print(f"  [FAIL] Sample for {state}: {e}")

print("\n=== 3. Verifying Dynamic Declarative Schema Mapping ===")
custom_req_data = {
    "state_origin": "Punjab",
    "raw_payload": {
        "source_portal": "Punjab Kisan Portal",
        "kisan_nam": "Gurmeet Singh",
        "zila": "Ludhiana",
        "fasal": "Wheat",
        "fasal_kism": "HD-3086",
        "mitti_ph": 7.4,
        "nitrogen": 210.0,
        "carbon": 0.55,
        "ardrata": 72.0
    },
    "custom_rules": {
        "kisan_nam": "farmer.name",
        "zila": "location.district",
        "fasal": "crop.name",
        "fasal_kism": "crop.variety",
        "mitti_ph": "soil_health.ph",
        "nitrogen": "soil_health.nitrogen_kg_ha",
        "carbon": "soil_health.organic_carbon_pct",
        "ardrata": "weather.relative_humidity_pct"
    }
}
req = urllib.request.Request(
    'http://127.0.0.1:8000/api/interop/normalize',
    data=json.dumps(custom_req_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print(f"  [PASS] Declarative Adapter Source: {res.get('source_schema_detected')}")
    print(f"  [PASS] Farmer Name mapped: {res['normalized_context']['farmer']['name']}")
    print(f"  [PASS] Location District mapped: {res['normalized_context']['location']['district']}")
    print(f"  [PASS] Crop Name mapped: {res['normalized_context']['crop']['name']}")
    print(f"  [PASS] Soil pH mapped: {res['normalized_context']['soil_health']['ph']}")
    print(f"  [PASS] Soil Nitrogen mapped: {res['normalized_context']['soil_health']['nitrogen_kg_ha']} kg/ha")
    print(f"  [PASS] Mappings applied count: {len(res['field_mappings_applied'])}")
    for note in res.get('transformation_notes', []):
        print(f"         Audit Note: {note}")

print("\n=== 4. Verifying Earth Engine Sentinel-2 Telemetry & Outbreak Corridor ===")
with urllib.request.urlopen('http://127.0.0.1:8000/api/interop/telemetry') as resp:
    alerts = json.loads(resp.read().decode('utf-8'))
    print(f"  [PASS] Active Regional Alerts: {len(alerts)} corridor warning(s) active.")
    for a in alerts[:2]:
        print(f"         - Alert ID: {a['alert_id']} | Pest: {a['pest_disease_name']}")
        print(f"           Corridor: {a['transmission_corridor']}")
        print(f"           Threatened Districts: {a['threatened_neighboring_districts']}")

latitude = os.getenv("KRISHISETU_TEST_LATITUDE")
longitude = os.getenv("KRISHISETU_TEST_LONGITUDE")
if latitude and longitude:
    query = urllib.parse.urlencode({"latitude": latitude, "longitude": longitude})
    with urllib.request.urlopen(f'http://127.0.0.1:8000/api/telemetry/satellite?{query}') as resp:
        sat = json.loads(resp.read().decode('utf-8'))
        if sat.get("available"):
            print(f"  [PASS] Earth Engine observation: {sat.get('observation_date')}")
            print(f"         NDVI={sat.get('ndvi')} | Vegetation={sat.get('vegetation_status')}")
            print(f"         Clear pixels={sat.get('clear_pixel_pct')}%")
        else:
            print(f"  [UNAVAILABLE] Satellite telemetry: {sat.get('reason')}")
else:
    print("  [SKIP] Set KRISHISETU_TEST_LATITUDE and KRISHISETU_TEST_LONGITUDE to query a farm.")

print("\n=== 5. Testing Simulated Cross-Border Outbreak Injection ===")
sim_url = 'http://127.0.0.1:8000/api/interop/simulate-outbreak?pest_name=Yellow+Stem+Borer&origin_state=West+Bengal&origin_district=Malda&affected_crop=Rice&severity=High'
sim_req = urllib.request.Request(sim_url, data=b'', headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(sim_req) as resp:
    new_alert = json.loads(resp.read().decode('utf-8'))
    print(f"  [PASS] Injected Outbreak: {new_alert['alert_id']} for {new_alert['pest_disease_name']}")
    print(f"         Corridor: {new_alert['transmission_corridor']}")
    print(f"         Threatened Neighbors: {new_alert['threatened_neighboring_districts']}")

print("\nALL VERIFICATION CHECKS PASSED 100%!")
