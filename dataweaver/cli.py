import sys
import os
import argparse
from dataweaver.core import BatchMerger, TextNormalizer, PATTERNS
from dataweaver import __version__

def main():
    parser = argparse.ArgumentParser(
        prog="dataweaver",
        description="DataWeaver: Ultra-fast local data cleaner, merger, and regex extractor."
    )
    parser.add_argument("-v", "--version", action="version", version=f"DataWeaver {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: merge
    merge_parser = subparsers.add_parser("merge", help="Batch merge multiple CSV/TSV files into one.")
    merge_parser.add_argument("-i", "--inputs", nargs="+", required=True, help="Input files or pattern")
    merge_parser.add_argument("-o", "--output", required=True, help="Output consolidated CSV file")
    merge_parser.add_argument("--no-dedup", action="store_true", help="Disable automatic deduplication")

    # Command: extract
    extract_parser = subparsers.add_parser("extract", help="Extract emails, phones, URLs from raw text/file into CSV.")
    extract_parser.add_argument("-i", "--input", required=True, help="Path to input text or dump file")
    extract_parser.add_argument("-o", "--output", required=True, help="Output structured CSV file")

    # Command: gui
    gui_parser = subparsers.add_parser("gui", help="Launch the desktop graphical interface.")

    args = parser.parse_args()

    if args.command == "merge":
        print(f"🚀 Merging {len(args.inputs)} files into {args.output}...")
        res = BatchMerger.merge_csv_files(args.inputs, args.output, deduplicate=not args.no_dedup)
        print("✅ Merge Complete!")
        print(f"   - Files processed: {res['processed_files']}")
        print(f"   - Total rows: {res['total_records']}")
        print(f"   - Output saved to: {res['output_path']}")

    elif args.command == "extract":
        print(f"🔍 Extracting entities from {args.input}...")
        res = BatchMerger.extract_entities_to_csv(args.input, args.output)
        print("✅ Extraction Complete!")
        for k, count in res["total_extracted"].items():
            print(f"   - {k}: {count} found")
        print(f"   - Output saved to: {res['output_path']}")

    elif args.command == "gui" or len(sys.argv) == 1:
        # Default to launching GUI if no args or explicit gui
        try:
            from dataweaver.gui import launch_gui
            launch_gui()
        except ImportError as e:
            print(f"Error launching GUI: {e}")
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
