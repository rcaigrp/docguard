import re
from typing import List, Dict

def detect_drift(code_elements: List[Dict], doc_sections: List[Dict]) -> List[Dict]:
    """
    Identifies potential documentation drift by comparing code elements with documentation sections.
    Uses simple heuristics to identify undocumented functions and outdated references.
    """
    findings = []
    code_names = {elem['name'] for elem in code_elements}

    # Check for undocumented code elements
    for elem in code_elements:
        name = elem['name']
        covered = False
        for section in doc_sections:
            title = section.get('title', '').lower()
            content = section.get('content', '').lower()
            if name.lower() in title or name.lower() in content:
                covered = True
                break
        if not covered:
            findings.append({
                'type': 'undocumented',
                'element': name,
                'path': elem.get('path', ''),
                'message': f"'{name}' is not documented."
            })

    # Check for outdated references in documentation
    for section in doc_sections:
        content = section.get('content', '').lower()
        # Extract potential code references (e.g., `func_name` or `ClassName`)
        refs = re.findall(r'`(\w+)`', content)
        for ref in refs:
            if ref not in code_names:
                findings.append({
                    'type': 'outdated_reference',
                    'element': ref,
                    'path': section.get('path', ''),
                    'message': f"Reference to '{ref}' not found in code structure."
                })

    return findings
