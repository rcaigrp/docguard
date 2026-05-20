from parsers import extract_references

def detect_drift(code_elements, doc_sections):
    """Identify potential drift between code and documentation."""
    findings = []
    
    # 1. Undocumented functions (code elements without docstrings)
    for filepath, elements in code_elements.items():
        for name, info in elements.items():
            if not info['docstring']:
                findings.append({
                    'type': 'undocumented',
                    'element': name,
                    'file': filepath,
                    'message': f"{info['type']} '{name}' has no docstring."
                })
    
    # 2. Outdated references (doc references to functions not in code)
    all_code_names = set()
    for elements in code_elements.values():
        all_code_names.update(elements.keys())
        
    for filepath, sections in doc_sections.items():
        for section_title, content in sections.items():
            refs = extract_references(content)
            for ref in refs:
                if ref not in all_code_names:
                    findings.append({
                        'type': 'outdated_reference',
                        'reference': ref,
                        'file': filepath,
                        'section': section_title,
                        'message': f"Reference '{ref}' not found in code."
                    })
                    
    return findings
