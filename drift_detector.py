import re

def detect_drift(code_elements, doc_elements):
    findings = []
    for element in code_elements:
        if not element.get('docstring'):
            findings.append({
                'type': 'warning',
                'element': f"{element['type']} {element['name']}",
                'issue': 'No documentation string found.'
            })
    
    doc_text = ' '.join(doc_elements.get('headings', [])) + ' ' + ' '.join(doc_elements.get('code_snippets', []))
    
    for element in code_elements:
        pattern = re.compile(r'\b' + re.escape(element['name']) + r'\b', re.IGNORECASE)
        if not pattern.search(doc_text):
            findings.append({
                'type': 'info',
                'element': f"{element['type']} {element['name']}",
                'issue': 'Not mentioned in documentation.'
            })
    return findings
