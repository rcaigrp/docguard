def find_drift(code_elements, doc_sections):
    drifts = []
    # 1. Check for undocumented code elements
    for elem in code_elements:
        if not elem.get('docstring'):
            drifts.append({
                'type': 'UNDOCUMENTED',
                'element': elem['name'],
                'message': f"No docstring for {elem['name']} in {elem.get('file', 'unknown')}"
            })
            
    # 2. Check for outdated documentation references
    code_names = {e['name'].lower() for e in code_elements}
    for sec in doc_sections:
        # If it's a reference, check if it exists in code
        if sec.get('type') == 'REFERENCE':
            if sec['name'].lower() not in code_names:
                drifts.append({
                    'type': 'OUTDATED',
                    'element': sec['name'],
                    'message': f"Docs reference '{sec['name']}' not found in code"
                })
    return drifts
