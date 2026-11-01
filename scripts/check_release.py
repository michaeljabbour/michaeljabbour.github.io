"""Refuse publication of a local preview or an artifact from other source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

from catalogue_admission import current_admission, load_publication, validate_catalogue

ROOT = Path(__file__).resolve().parents[1]


def validate_artifact(root, *, for_publication=False):
    catalogue = json.loads((root / "content/portfolio.json").read_text())
    mapping = json.loads((root / "content/migration/mapping.json").read_text())
    if for_publication:
        if os.environ.get("PORTFOLIO_PREVIEW") == "1":
            raise ValueError("A preview override cannot authorize publication")
        admission = validate_catalogue(catalogue, mapping, load_publication(root))
    else:
        admission = current_admission(root, catalogue, mapping)
    artifact_path = root / "dist/publication.json"
    artifact = json.loads(artifact_path.read_text())
    if set(artifact) != {"schema_version", "source_commit", "preview_only", "publication_ready", "capability_ids", "additional_sources"} or artifact["schema_version"] != "portfolio-artifact/v1":
        raise ValueError("Invalid artifact publication receipt")
    for key in ["preview_only", "publication_ready", "capability_ids"]:
        if type(artifact[key]) is not type(admission[key]) or artifact[key] != admission[key]:
            raise ValueError("Artifact publication state differs from admitted source")
    if artifact["additional_sources"] != admission["additions"]:
        raise ValueError("Artifact release pins differ from admitted source")
    head = subprocess.check_output(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if artifact["source_commit"] != head:
        raise ValueError("Artifact does not belong to the current source commit")
    if json.loads((root / "dist/portfolio.json").read_text()) != catalogue:
        raise ValueError("Served catalogue differs from admitted source")
    if for_publication:
        if artifact["preview_only"] or artifact["publication_ready"] is not True:
            raise ValueError("Local preview artifacts cannot be published")
        dirty = subprocess.check_output(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(root), "status", "--porcelain=v1"], text=True)
        if dirty:
            raise ValueError("Publication requires committed source")
    return {"source_sha": head, "publication_ready": artifact["publication_ready"], "preview_only": artifact["preview_only"], "publication_manifest_sha256": hashlib.sha256(artifact_path.read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--for-publication", action="store_true")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    result = validate_artifact(ROOT, for_publication=args.for_publication)
    if args.github_output:
        if not args.for_publication or not result["publication_ready"]:
            raise ValueError("Only a publication guard may emit ready outputs")
        with args.github_output.open("a") as output:
            output.write("publication_ready=true\nsource_sha=" + result["source_sha"] + "\npublication_manifest_sha256=" + result["publication_manifest_sha256"] + "\n")
    print(json.dumps(result, indent=2))
