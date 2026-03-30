

import pandas as pd
import os
import json
from datetime import date, datetime

# Define mapping from Excel files to JS files
file_map = {
    'Material_Codes.xlsx': 'Material_Codes.js',
    'PM_Tracking.xlsx': 'PM_Tracking.js',
    'Sub-C Contracts.xlsx': 'SUB-C_CONTRACTS.js',
    'SUB-C Materials.xlsx': 'SUB-C_Materials.js',
    'Sub-C_List.xlsx': 'Sub-C_List.js',
}

excel_dir = os.path.join(os.path.dirname(__file__), 'Data excel')
js_dir = os.path.dirname(__file__)

for excel_file, js_file in file_map.items():
    excel_path = os.path.join(excel_dir, excel_file)
    js_path = os.path.join(js_dir, js_file)
    if not os.path.exists(excel_path):
        print(f"File not found: {excel_path}")
        continue
    df = pd.read_excel(excel_path)
    # Convert DataFrame to list of dicts for readability
    data = df.to_dict(orient='records')
    # Write to JS file as a variable export, pretty-printed
    var_name = os.path.splitext(js_file)[0]
    def default_serializer(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(f"// Auto-generated from {excel_file}\n")
        f.write(f"export const {var_name} = ")
        json.dump(data, f, ensure_ascii=False, indent=2, default=default_serializer)
        f.write(';\n')
    print(f"Wrote {len(data)} records to {js_file}")
print("Done.")
