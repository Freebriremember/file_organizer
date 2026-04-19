import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime


def sanitize_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    return name.strip('._') or "file"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 1
    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def format_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d_%H-%M-%S")


def get_sort_folder(file_path: Path, mode: str) -> str:
    if mode == "extension":
        ext = file_path.suffix.lower().lstrip(".")
        return ext if ext else "no_extension"

    if mode == "date":
        dt = datetime.fromtimestamp(file_path.stat().st_mtime)
        return dt.strftime("%Y-%m")

    if mode == "first_letter":
        first = file_path.stem[:1].lower()
        if first.isalpha():
            return first
        if first.isdigit():
            return "0-9"
        return "other"

    return "unsorted"


def build_new_name(file_path: Path, pattern: str, index: int) -> str:
    stat = file_path.stat()
    values = {
        "original": file_path.stem,
        "ext": file_path.suffix.lower().lstrip("."),
        "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
        "datetime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d_%H-%M-%S"),
        "size": str(stat.st_size),
        "index": f"{index:04d}",
    }

    new_stem = pattern.format(**values)
    new_stem = sanitize_filename(new_stem)

    return f"{new_stem}{file_path.suffix.lower()}"


def should_process(file_path: Path, extensions: set[str] | None) -> bool:
    if not file_path.is_file():
        return False

    if extensions is None:
        return True

    return file_path.suffix.lower().lstrip(".") in extensions


def collect_files(source_dir: Path, recursive: bool, extensions: set[str] | None):
    collected = []

    if recursive:
        for root, _, files in os.walk(source_dir):
            root_path = Path(root)
            for filename in files:
                file_path = root_path / filename
                if should_process(file_path, extensions):
                    collected.append(file_path)
    else:
        for file_path in source_dir.iterdir():
            if should_process(file_path, extensions):
                collected.append(file_path)

    return collected


def sort_files(files: list[Path], order: str) -> list[Path]:
    if order == "name":
        return sorted(files, key=lambda p: p.name.lower())

    if order == "mtime":
        return sorted(files, key=lambda p: p.stat().st_mtime)

    if order == "ctime":
        return sorted(files, key=lambda p: p.stat().st_ctime)

    if order == "size":
        return sorted(files, key=lambda p: p.stat().st_size)

    return files


def process_files(
    source_dir: Path,
    output_dir: Path,
    recursive: bool,
    extensions: set[str] | None,
    sort_by_folder: str,
    rename_pattern: str | None,
    order: str,
    move_files: bool,
    dry_run: bool,
):
    files = collect_files(source_dir, recursive, extensions)
    files = sort_files(files, order)

    if not files:
        print("No matching files found.")
        return

    print(f"Found {len(files)} file(s).")

    for index, file_path in enumerate(files, start=1):
        try:
            target_dir = output_dir

            if sort_by_folder != "none":
                folder_name = get_sort_folder(file_path, sort_by_folder)
                target_dir = output_dir / folder_name

            if rename_pattern:
                new_name = build_new_name(file_path, rename_pattern, index)
            else:
                new_name = sanitize_filename(file_path.name)

            destination = target_dir / new_name
            destination = unique_path(destination)

            action = "MOVE" if move_files else "COPY"
            print(f"{action}: {file_path} -> {destination}")

            if dry_run:
                continue

            target_dir.mkdir(parents=True, exist_ok=True)

            if move_files:
                shutil.move(str(file_path), str(destination))
            else:
                shutil.copy2(str(file_path), str(destination))

        except Exception as e:
            print(f"ERROR: {file_path} -> {e}")


def parse_extensions(ext_string: str | None):
    if not ext_string:
        return None

    extensions = set()
    for ext in ext_string.split(","):
        cleaned = ext.strip().lower().lstrip(".")
        if cleaned:
            extensions.add(cleaned)

    return extensions or None


def main():
    parser = argparse.ArgumentParser(
        description="Process, rename, and sort files in directories using os and shutil."
    )

    parser.add_argument(
        "source",
        help="Source directory containing files to process."
    )

    parser.add_argument(
        "output",
        help="Output directory where processed files will be placed."
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process files recursively in all subdirectories."
    )

    parser.add_argument(
        "--extensions",
        type=str,
        default=None,
        help="Comma-separated list of extensions to process, e.g. jpg,png,pdf"
    )

    parser.add_argument(
        "--sort-folder",
        choices=["none", "extension", "date", "first_letter"],
        default="extension",
        help="Create subfolders by extension, date, first letter, or none."
    )

    parser.add_argument(
        "--rename-pattern",
        type=str,
        default="{date}_{index}_{original}",
        help=(
            "Rename pattern using placeholders: "
            "{original}, {ext}, {date}, {datetime}, {size}, {index}"
        )
    )

    parser.add_argument(
        "--order",
        choices=["none", "name", "mtime", "ctime", "size"],
        default="name",
        help="Order files before processing."
    )

    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying them."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without actually changing files."
    )

    args = parser.parse_args()

    source_dir = Path(args.source).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist or is not a directory: {source_dir}")

    extensions = parse_extensions(args.extensions)

    process_files(
        source_dir=source_dir,
        output_dir=output_dir,
        recursive=args.recursive,
        extensions=extensions,
        sort_by_folder=args.sort_folder,
        rename_pattern=args.rename_pattern,
        order=args.order,
        move_files=args.move,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
