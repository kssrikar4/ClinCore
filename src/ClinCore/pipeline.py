from pathlib import Path
from ClinCore.config import StudyConfig
from ClinCore.sdtm import process_sdtm
from ClinCore.adam import process_adam
from ClinCore.metadata import init_lineage, finalize_lineage
from ClinCore.validation import validate_datasets
from ClinCore.reporting import generate_reports
from rich.progress import Progress, SpinnerColumn, TextColumn

def run_pipeline(config: StudyConfig, study_dir: Path):
    out_dir = study_dir / "output"
    sdtm_dir = out_dir / "sdtm"
    adam_dir = out_dir / "adam"
    sdtm_dir.mkdir(parents=True, exist_ok=True)
    adam_dir.mkdir(parents=True, exist_ok=True)

    init_lineage()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Processing datasets...", total=len(config.datasets))
        
        for ds_name, ds_config in config.datasets.items():
            progress.update(task, description=f"Processing {ds_name}...")
            if ds_config.type == "sdtm":
                process_sdtm(ds_name, ds_config, study_dir, sdtm_dir)
            elif ds_config.type == "adam":
                process_adam(ds_name, ds_config, study_dir, adam_dir)
            progress.advance(task)

    validate_datasets(config, study_dir)
    generate_reports(config, study_dir)
    finalize_lineage(out_dir, config)
