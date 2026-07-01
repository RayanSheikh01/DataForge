"""Command-line entrypoint: dataforge run / export."""

import argparse


def main():
    """
    dataforge run <task.yaml>     # load config, build pipeline, run, print stats
    dataforge export <task.yaml>  # build HF dataset from existing data.jsonl
    """
    parser = argparse.ArgumentParser(description="DataForge CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the pipeline")
    run_parser.add_argument("config_path", type=str, help="Path to the task.yaml config file")

    export_parser = subparsers.add_parser("export", help="Export dataset")
    export_parser.add_argument("config_path", type=str, help="Path to the task.yaml config file")

    args = parser.parse_args()

    if args.command == "run":
        from dataforge.config import load_config
        from dataforge.pipeline import build_pipeline

        config = load_config(args.config_path)
        pipeline = build_pipeline(config)
        stats = pipeline.run()
        print(f"RunStats: accepted={stats.accepted}, discarded={stats.discarded}, duplicates={stats.duplicates}")

    elif args.command == "export":
        from dataforge.config import load_config
        from dataforge.writer import export_dataset

        config = load_config(args.config_path)
        
        export_dataset(out_dir=config.output.dir, push_to_hub=config.output.push_to_hub, repo_id=getattr(config.output, "repo_id", None))


if __name__ == "__main__":
    main()
