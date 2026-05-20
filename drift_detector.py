def detect_drift(code_elements, doc_sections):
    drifts = []
    for element in code_elements:
        name = element['name']
        found = False
        for section_name in doc_sections.keys():
            if name.lower() in section_name.lower() or section_name.lower() in name.lower():
                found = True
                break
        if not found:
            drifts.append({
                'element': name,
                'type': element['type'],
                'status': 'undocumented',
                'path': element['path']
            })
    return drifts
