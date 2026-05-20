from parsers import get_code_elements, get_doc_refs

def scan(directory):
    code_elements = get_code_elements(directory)
    doc_refs = get_doc_refs(directory)
    
    findings = []
    code_names = [e['name'] for e in code_elements]
    
    for elem in code_elements:
        if elem['name'] not in doc_refs:
            findings.append({
                'status': 'UNDOCUMENTED',
                'element': elem['name'],
                'file': elem['file']
            })
            
    for ref in doc_refs:
        if ref not in code_names:
            if ref not in ['python', 'code', 'import', 'markdown', 'readme']:
                findings.append({
                    'status': 'OUTDATED',
                    'element': ref,
                    'file': 'docs'
                })
                
    return findings
