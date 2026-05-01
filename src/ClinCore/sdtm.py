import polars as pl
from pathlib import Path
from ClinCore.config import DatasetConfig
from ClinCore.metadata import record_lineage

def process_sdtm(name: str, config: DatasetConfig, study_dir: Path, out_dir: Path):
    if not config.source_file:
        return

    source_path = study_dir / config.source_file
    df = pl.read_csv(source_path, separator=config.delimiter, null_values=["", "NA", "null"])

    rename_map = {}
    for mapping in config.mappings:
        if mapping.source in df.columns:
            rename_map[mapping.source] = mapping.target
            record_lineage(name, mapping.target, mapping.source, "mapped")

    df = df.rename(rename_map)

    for drv in config.derivations:
        try:
            expr_str = drv.expression
            df = df.with_columns(eval(expr_str).alias(drv.target))
            record_lineage(name, drv.target, "derived", drv.expression)
        except Exception as e:
            print(f"Error evaluating derivation for {name}.{drv.target}: {e}")

    out_file = out_dir / f"{name.lower()}.csv"
    df.write_csv(out_file)
    print(f"Saved SDTM dataset: {out_file}")
