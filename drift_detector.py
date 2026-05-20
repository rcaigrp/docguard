def detect_drift(code, docs):
    doc_names = [d['name'] for d in docs]
    return [{"type": "Undocumented", "element": c['name'], "file": c['file']} for c in code if c['name'] not in doc_names]
