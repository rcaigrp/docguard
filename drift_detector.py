def find_drift(code_elements, docs):
    findings = []
    doc_headers = []
    for doc in docs:
        doc_headers.extend(doc.get("headers", []))
        doc_headers.extend([ref[0] for ref in doc.get("refs", [])])
        
    for elem in code_elements:
        if not elem.get("doc"):
            findings.append({
                "type": "UNDOCUMENTED",
                "element": elem["name"],
                "issue": f"Function/Class '{elem['name']}' has no docstring."
            })
        elif elem["name"] not in doc_headers:
            findings.append({
                "type": "OUTDATED",
                "element": elem["name"],
                "issue": f"Documentation reference missing for '{elem['name']}'."
            })
    return findings
