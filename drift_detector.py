def detect_drift(code_elements, doc_sections):
    drifts = []
    code_names = {c['name'].lower(): c for c in code_elements}
    doc_names = {d['name'].lower(): d for d in doc_sections}
    
    for name, element in code_names.items():
        if name not in doc_names:
            drifts.append({
                'type': 'UNDOC',
                'element': element['name'],
                'issue': f'No documentation found for {element["type"]} {element["name"]}'
            })
            
    for name, doc in doc_names.items():
        if name not in code_names:
            drifts.append({
                'type': 'OUTDATED',
                'element': doc['name'],
                'issue': f'Documentation for {doc["name"]} has no corresponding code'
            })
            
    return drifts
