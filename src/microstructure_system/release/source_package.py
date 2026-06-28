from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from microstructure_system.release.manifest import _is_excluded_path


def source_release_filename() -> str:
    """Return the generated source release filename."""
    return "market_microstructure_execution_cost_system_source_release.zip"


def build_source_release_package(project_root: Path) -> Path:
    """Build the clean source release zip for public sharing."""
    package_path = project_root / "dist" / source_release_filename()
    package_path.parent.mkdir(parents=True, exist_ok=True)
    if package_path.exists():
        package_path.unlink()
    include_roots = {".github", "src", "tests", "config", "docs", "reports"}
    include_files = {
        ".gitattributes",
        ".gitignore",
        "README.md",
        "pyproject.toml",
        "run_project.py",
        "uv.lock",
    }
    with ZipFile(package_path, "w", ZIP_DEFLATED) as archive:
        for file in sorted(project_root.rglob("*")):
            if not file.is_file():
                continue
            relative_path = file.relative_to(project_root)
            if _is_excluded_path(relative_path):
                continue
            if relative_path.parts[0] in include_roots or relative_path.name in include_files:
                archive.write(file, relative_path)
    return package_path
