def detect_drift(code_elements, doc_sections):
    findings = []
    doc_titles = []
    for sections in doc_sections.values():
        for s in sections:
            doc_titles.append(s["title"])
            
    for elem in code_elements:
        if elem["name"] not in doc_titles:
            findings.append({
                "element": elem["name"],
                "status": "UNDOC",
                "file": elem["file"]
            })
        else:
            findings.append({
                "element": elem["name"],
                "status": "OK",
                "file": elem["file"]
            })
    return findings
