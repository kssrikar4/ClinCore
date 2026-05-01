import json
import xml.etree.ElementTree as ET
from pathlib import Path
from ClinCore.config import StudyConfig

_lineage_store = {}

def init_lineage():
    global _lineage_store
    _lineage_store.clear()

def record_lineage(dataset: str, variable: str, origin: str, details: str):
    global _lineage_store
    if dataset not in _lineage_store:
        _lineage_store[dataset] = {}
    _lineage_store[dataset][variable] = {
        "origin": origin,
        "details": details
    }

def finalize_lineage(out_dir: Path, config: StudyConfig):
    global _lineage_store
    
    lineage_file = out_dir / "lineage.json"
    with open(lineage_file, "w") as f:
        json.dump(_lineage_store, f, indent=2)

    root = ET.Element("StudyMetadata", studyId=config.study_id)
    desc = ET.SubElement(root, "Description")
    desc.text = config.description

    datasets_el = ET.SubElement(root, "Datasets")
    for ds_name, variables in _lineage_store.items():
        ds_el = ET.SubElement(datasets_el, "Dataset", name=ds_name)
        vars_el = ET.SubElement(ds_el, "Variables")
        for var_name, info in variables.items():
            var_el = ET.SubElement(vars_el, "Variable", name=var_name)
            ET.SubElement(var_el, "Origin").text = info["origin"]
            ET.SubElement(var_el, "Details").text = info["details"]

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(out_dir / "study_metadata.xml", encoding="utf-8", xml_declaration=True)
