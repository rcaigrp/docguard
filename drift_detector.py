def detect_drift(code_elements, doc_sections):
    findings = []
    doc_names = [d['name'] for d in doc_sections]
    code_names = [c['name'] for c in code_elements]
    
    for c in code_elements:
        if c['name'] not in doc_names:
            findings.append({
                'type': 'undocumented',
                'element': c['name'],
                'issue': f"Function {c['name']} is not documented."
            })
            
    for d in doc_sections:
        if d['name'] not in code_names:
            findings.append({
                'type': 'outdated',
                'element': d['name'],
                'issue': f"Documentation {d['name']} has no matching code."
            })
            
    return findings
