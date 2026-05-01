# ClinCore
ClinCore is a CDISC-ready clinical data processing engine designed to bridge the gap between raw data extracts and regulatory-compliant datasets (SDTM/ADaM). Built for speed, auditability, and professional reporting.

## Quick Start (Demo Workflow)
For newcomers. This workflow uses automated data fetching to demonstrate the engine's capabilities.

### 1. Installation
```bash
# create and activate python venv
pip install -e .
```

### 2. Initialize and Fetch Sample Data
Create a study directory and pull hypertension trial data from ClinicalTrials.gov (AACT).
```bash
ClinCore init --dir demo_study
ClinCore fetch --study demo_study
```

### 3. Run the Pipeline
The `init` command automatically creates a `study.yaml` pre-configured for the fetched data.
```bash
ClinCore run --config demo_study/study.yaml
```

### 4. Review Results
Check `demo_study/output/` for:
- `sdtm/` & `adam/`: Processed datasets.
- `tlfs.pdf`: Professional summary tables.
- `lineage.json`: Complete audit trail.

## Production Workflow for your own Study
Follow this path when you have your own raw datasets (e.g., from an EDC system) and need to build a compliant pipeline.

### 1. Setup Your Workspace
Initialize a new study structure.
```bash
ClinCore init --dir clinical_trial_001
```

### 2. Import Your Raw Data
Place your raw data files (CSV, PSV, or TSV) into the `raw_data/` directory.
```bash
cp /path/to/my/raw_data.csv clinical_trial_001/raw_data/
```

### 3. Configure Transformations
Edit `clinical_trial_001/study.yaml` to define your mappings and derivations. ClinCore supports custom delimiters for non-standard raw extracts.

```yaml
datasets:
  DM:
    type: sdtm
    source_file: raw_data/my_raw_data.csv
    delimiter: ","  # Supports "|", "\t", etc.
    mappings:
      - source: Raw_Subject_ID
        target: USUBJID
    derivations:
      - target: DOMAIN
        expression: pl.lit("DM")
```

### 4. Execute and Validate
Run the pipeline and generate your TLF reports in one step.
```bash
ClinCore run --config clinical_trial_001/study.yaml
```

## Advanced Features
ClinCore uses Polars for ultra-fast ingestion. Support for custom delimiters ensures that even corrupted pipe-delimited extracts are parsed correctly without data loss.

### Professional Reporting
Generate FDA-ready PDF summaries. Configure reports in your `study.yaml`:
```yaml
reports:
  - id: T14.1
    type: table
    dataset: ADSL
    columns: [USUBJID, ARM, AGE, SEX]
```

### Audit-Ready Traceability
Every run generates a `lineage.json` file. This technical audit trail maps every variable in your final datasets back to its source, including the specific logic used for derivations.

## License
[Mozilla Public License Version 2.0](LICENSE) - Feel free to use and modify.
