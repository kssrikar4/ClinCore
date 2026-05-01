import yaml
import shutil
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class ColumnMap(BaseModel):
    source: str
    target: str

class Derivation(BaseModel):
    target: str
    expression: str

class DatasetConfig(BaseModel):
    type: str
    source_file: Optional[str] = None
    delimiter: str = ","
    mappings: List[ColumnMap] = []
    derivations: List[Derivation] = []

class ValidationRule(BaseModel):
    dataset: str
    rule_type: str
    column: str
    condition: Optional[str] = None

class ReportConfig(BaseModel):
    id: str
    type: str
    dataset: str
    columns: List[str]

class StudyConfig(BaseModel):
    study_id: str
    description: str
    datasets: Dict[str, DatasetConfig]
    validation: List[ValidationRule] = []
    reports: List[ReportConfig] = []

def load_config(path: str | Path) -> StudyConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return StudyConfig(**data)

def init_study(dir_name: str):
    p = Path(dir_name)
    p.mkdir(parents=True, exist_ok=True)
    (p / "raw_data").mkdir(exist_ok=True)
    (p / "output").mkdir(exist_ok=True)
    (p / "output" / "sdtm").mkdir(exist_ok=True)
    (p / "output" / "adam").mkdir(exist_ok=True)
    
    default_config = {
        "study_id": "DEMO-001",
        "description": "Demo Study",
        "datasets": {
            "TS": {
                "type": "sdtm",
                "source_file": "raw_data/trials.csv",
                "mappings": [
                    {"source": "NCT Number", "target": "STUDYID"},
                    {"source": "Study Title", "target": "TITLE"},
                    {"source": "Study Status", "target": "STATUS"}
                ],
                "derivations": [
                    {"target": "DOMAIN", "expression": "pl.lit('TS')"}
                ]
            },
            "ADTS": {
                "type": "adam",
                "source_file": "TS",
                "mappings": [],
                "derivations": [
                    {"target": "PARAMCD", "expression": "pl.lit('TRIAL_SUMMARY')"},
                    {"target": "AVALC", "expression": "pl.col('STATUS')"}
                ]
            }
        },
        "validation": [
            {"dataset": "TS", "rule_type": "not_null", "column": "STUDYID"}
        ],
        "reports": [
            {
                "id": "T-01",
                "type": "table",
                "dataset": "ADTS",
                "columns": ["STUDYID", "TITLE", "STATUS", "PARAMCD", "AVALC"]
            }
        ]
    }
    with open(p / "study.yaml", "w", encoding="utf-8") as f:
        yaml.dump(default_config, f, sort_keys=False)
