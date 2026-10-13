"""Generate the stable update manifest from verified public release assets.

This standalone channel tool uses only the Python standard library. It never reads
credentials or private databases, and performs no network requests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REPOSITORY = "applehitmyhead-svg/MateriaRadar-Updates"


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def build_manifest(release_dir: Path, *, tag: str | None = None) -> dict:
    directory = release_dir.resolve()
    reports = list(directory.glob("MateriaRadar-*-windows-x64-full-seed-smoke.json"))
    if len(reports) != 1:
        raise ValueError("A unique Windows full-seed verification report is required")
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    build = report.get("build", {})
    version = build.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Invalid version")
    verification = report.get("verification", {})
    if (not verification.get("ok") or verification.get("version") != version
            or not build.get("seed_id") or not re.fullmatch(r"[0-9a-f]{32}", build.get("build_id", ""))
            or any(not re.fullmatch(r"[0-9a-f]{64}", build.get(key, ""))
                   for key in ("source_sha256", "configuration_sha256"))):
        raise ValueError("A verified full-data build is required")
    tag = tag or "v"+version
    if not re.fullmatch("v"+re.escape(version)+r"(?:-build\.[A-Za-z0-9.-]+)?", tag):
        raise ValueError("Release tag must match the product version")
    base = f"https://github.com/{REPOSITORY}/releases/download/{tag}"
    names = {
        "windows-x64": f"MateriaRadar-{version}-windows-x64-setup.exe",
        "portable-windows-x64": f"MateriaRadar-{version}-windows-x64-full-seed.zip",
        "database": f"MateriaRadar-{version}-database.db.xz",
        "database-manifest": f"MateriaRadar-{version}-database-manifest.json",
        "verification": reports[0].name,
    }
    assets = {}
    checksums = (directory/f"MateriaRadar-{version}-SHA256SUMS.txt").read_text(encoding="utf-8")
    expected = dict((name, sha) for sha, name in (line.split("  ", 1) for line in checksums.splitlines()))
    for key, name in names.items():
        path = directory/name
        if not path.is_file() or path.is_symlink():
            raise ValueError("Missing release asset: "+name)
        sha = digest(path)
        if expected.get(name) != sha:
            raise ValueError("Release checksum differs: "+name)
        assets[key] = {"name": name, "size": path.stat().st_size, "sha256": sha, "url": base+"/"+name}
    if assets["windows-x64"]["sha256"] != verification.get("installer_sha256"):
        raise ValueError("Installer differs from the verified build")
    if assets["portable-windows-x64"]["sha256"] != verification.get("portable_sha256"):
        raise ValueError("Portable package differs from the verified build")
    return {"manifest_version": 1, "channel": "stable", "product": "MateriaRadar",
            "version": version, "release_tag": tag, "build": build, "assets": assets,
            "database_snapshot": verification["snapshot_id"],
            "historical_records": verification["observations"],
            "latest_successful_fetch": verification["latest_successful_fetch"],
            "excel_workbooks": len(verification["price_workbooks"]["files"])}


def main():
    parser = argparse.ArgumentParser(description="Prepare the anonymous public update channel.")
    parser.add_argument("--release-dir", type=Path, required=True)
    parser.add_argument("--tag")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = build_manifest(args.release_dir, tag=args.tag)
    output = args.output or args.release_dir/"latest.json"
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Prepared {manifest['version']} public update manifest: {output}")


if __name__ == "__main__":
    main()
