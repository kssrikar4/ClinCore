import argparse
import sys
from pathlib import Path
from rich.console import Console

from ClinCore.config import load_config
from ClinCore.fetcher import fetch_data
from ClinCore.pipeline import run_pipeline
from ClinCore.validation import validate_datasets
from ClinCore.reporting import generate_reports

console = Console()

def main():
    parser = argparse.ArgumentParser(prog="ClinCore", description="CDISC-ready study engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Scaffold a new study directory")
    init_parser.add_argument("--dir", default="new_study", help="Directory name")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch raw data")
    fetch_parser.add_argument("--study", required=True, help="Study directory name")

    run_parser = subparsers.add_parser("run", help="Execute pipeline")
    run_parser.add_argument("--config", required=True, help="Path to study.yaml")

    validate_parser = subparsers.add_parser("validate", help="Run validation checks")
    validate_parser.add_argument("--config", required=True, help="Path to study.yaml")

    report_parser = subparsers.add_parser("report", help="Generate TLFs")
    report_parser.add_argument("--config", required=True, help="Path to study.yaml")

    args = parser.parse_args()

    try:
        if args.command == "init":
            console.print(f"[bold blue]Initializing study in {args.dir}...[/bold blue]")
            from ClinCore.config import init_study
            init_study(args.dir)
            console.print("[bold green]Successfully initialized study.[/bold green]")
        elif args.command == "fetch":
            console.print(f"[bold blue]Fetching data for {args.study}...[/bold blue]")
            fetch_data(args.study)
            console.print("[bold green]Data fetch complete.[/bold green]")
        elif args.command == "run":
            console.print(f"[bold blue]Running pipeline for {args.config}...[/bold blue]")
            cfg = load_config(args.config)
            run_pipeline(cfg, Path(args.config).parent)
            console.print("[bold green]Pipeline execution complete.[/bold green]")
        elif args.command == "validate":
            console.print(f"[bold blue]Validating datasets for {args.config}...[/bold blue]")
            cfg = load_config(args.config)
            validate_datasets(cfg, Path(args.config).parent)
            console.print("[bold green]Validation complete.[/bold green]")
        elif args.command == "report":
            console.print(f"[bold blue]Generating reports for {args.config}...[/bold blue]")
            cfg = load_config(args.config)
            generate_reports(cfg, Path(args.config).parent)
            console.print("[bold green]Reports generated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
