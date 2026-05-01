import json
import polars as pl
from pathlib import Path
from ClinCore.config import StudyConfig

def validate_datasets(config: StudyConfig, study_dir: Path):
    out_dir = study_dir / "output"
    sdtm_dir = out_dir / "sdtm"
    adam_dir = out_dir / "adam"
    
    report = []

    for rule in config.validation:
        ds_path_sdtm = sdtm_dir / f"{rule.dataset.lower()}.csv"
        ds_path_adam = adam_dir / f"{rule.dataset.lower()}.csv"
        
        path = None
        if ds_path_sdtm.exists():
            path = ds_path_sdtm
        elif ds_path_adam.exists():
            path = ds_path_adam
            
        if not path:
            report.append({
                "dataset": rule.dataset,
                "column": rule.column,
                "rule": rule.rule_type,
                "status": "fail",
                "reason": "dataset not found"
            })
            continue

        df = pl.read_csv(path)
        
        if rule.rule_type == "required_column":
            if rule.column not in df.columns:
                report.append({
                    "dataset": rule.dataset,
                    "column": rule.column,
                    "rule": rule.rule_type,
                    "status": "fail",
                    "reason": "column missing"
                })
        elif rule.rule_type == "not_null":
            if rule.column in df.columns:
                null_count = df[rule.column].is_null().sum()
                if null_count > 0:
                    report.append({
                        "dataset": rule.dataset,
                        "column": rule.column,
                        "rule": rule.rule_type,
                        "status": "fail",
                        "reason": f"{null_count} null values found"
                    })

    with open(out_dir / "validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
