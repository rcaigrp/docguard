def detect_drift(code_elements, docs, dry_run=False):
    """Identify potential drift between code and documentation."""
    findings = []
    
    # Check for undocumented functions/classes
    for elem in code_elements:
        if not elem.get('docstring'):
            findings.append({'type': 'undocumented', 'name': elem['name']})
            
    # Check for outdated references (docs exist but code doesn't)
    code_names = {elem['name'] for elem in code_elements}
    for doc_name in docs:
        if doc_name not in code_names:
            findings.append({'type': 'outdated_reference', 'name': doc_name})
            
    return findings
