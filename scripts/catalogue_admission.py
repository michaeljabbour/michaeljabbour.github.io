"""Admit named additions without rewriting historical repository migrations."""
import json
import os
import re
from datetime import datetime, timezone

HISTORICAL_RENAMES = {'build-amplifier': ['amplifier-skill-build-amplifier', 'amplifier-capability-build-amplifier'],
 'build-tauri': ['amplifier-skill-build-tauri', 'amplifier-capability-build-tauri'],
 'build-with-torque': ['amplifier-skill-build-torque', 'amplifier-capability-build-with-torque'],
 'cognitive-simulation': ['amplifier-skill-cognitive-simulation',
                          'amplifier-capability-cognitive-simulation'],
 'constraint-builder': ['amplifier-skill-constraint-builder',
                        'amplifier-capability-constraint-builder'],
 'data-substrate': ['amplifier-tool-data', 'amplifier-capability-data'],
 'decisioncraft': ['amplifier-smart-tool-decisioncraft', 'amplifier-capability-decisioncraft'],
 'desktop-tasks': ['amplifier-skill-desktop-tasks', 'amplifier-capability-desktop-tasks'],
 'fast-decisions': ['amplifier-smart-tool-fast-decisions', 'amplifier-capability-fast-decisions'],
 'forge': ['amplifier-skill-forge', 'amplifier-capability-forge'],
 'good-teammate': ['amplifier-skill-good-teammate', 'amplifier-capability-good-teammate'],
 'image-provider': ['amplifier-tool-imagen-provider', 'amplifier-capability-imagen-provider'],
 'imagen-studio': ['amplifier-skill-imagen-studio', 'amplifier-capability-imagen-studio'],
 'intent-to-plan': ['amplifier-skill-intent-to-plan', 'amplifier-capability-intent-to-plan'],
 'knowledge': ['amplifier-smart-tool-knowledge', 'amplifier-capability-knowledge'],
 'long-read': ['amplifier-skill-long-read', 'amplifier-capability-long-read'],
 'market-fit': ['amplifier-skill-market-fit', 'amplifier-capability-market-fit'],
 'memory': ['amplifier-skill-memory', 'amplifier-capability-memory'],
 'migrate': ['amplifier-skill-migrate', 'amplifier-capability-migrate'],
 'pipeline': ['amplifier-skill-pipeline', 'amplifier-capability-pipeline'],
 'preceptor': ['amplifier-skill-preceptor', 'amplifier-capability-preceptor'],
 'project-handoff': ['amplifier-skill-project-handoff', 'amplifier-capability-project-handoff'],
 'research': ['amplifier-skill-research', 'amplifier-capability-research'],
 'right-shape': ['amplifier-skill-right-shape', 'amplifier-capability-right-shape'],
 'session-doctor': ['amplifier-skill-session-doctor', 'amplifier-capability-session-doctor'],
 'sizzle': ['amplifier-skill-sizzle', 'amplifier-capability-sizzle'],
 'taste-elegance': ['amplifier-skill-taste', 'amplifier-capability-taste-elegance'],
 'team-access': ['amplifier-tool-team-access', 'amplifier-capability-team-access'],
 'teaserkit': ['amplifier-smart-tool-teaserkit', 'amplifier-capability-teaserkit'],
 'transfer': ['amplifier-skill-transfer', 'amplifier-capability-transfer'],
 'unknowns': ['amplifier-skill-unknowns', 'amplifier-capability-unknowns'],
 'ux-ergonomics': ['amplifier-skill-ux-ergonomics', 'amplifier-capability-ux-ergonomics'],
 'worth-using': ['amplifier-skill-worth-using', 'amplifier-capability-worth-using']}
HISTORICAL_IDS = frozenset(HISTORICAL_RENAMES)
ADDITIONAL_IDS = frozenset({"articlecraft", "idea-talks", "stories"})


def validate_historical_migration(mapping):
    rows = mapping.get("repositories", [])
    ids = [row.get("id") for row in rows]
    if len(ids) != 33 or len(set(ids)) != 33 or set(ids) != HISTORICAL_IDS:
        raise ValueError("Historical migration must retain exactly the original 33 identities")
    for row in rows:
        if [row.get("old_repository"), row.get("new_repository")] != HISTORICAL_RENAMES[row["id"]]:
            raise ValueError("Historical migration pairs cannot be rewritten for new capabilities")
    return rows


def load_publication(root):
    path = root / "content/additions.json"
    if not path.exists():
        return {"schema_version": "portfolio-additions/v1", "publication_ready": True, "capabilities": []}
    return json.loads(path.read_text())


def validate_catalogue(catalogue, migration, publication, *, preview=False, ci=False):
    """Preview is explicit and local; it never grants publication readiness."""
    validate_historical_migration(migration)
    if set(publication) != {"schema_version", "publication_ready", "capabilities"} or publication.get("schema_version") != "portfolio-additions/v1" or type(publication.get("publication_ready")) is not bool:
        raise ValueError("Invalid additions publication manifest")
    if ci and preview:
        raise ValueError("GitHub Actions must not accept the local preview override")
    entries = publication["capabilities"]
    if not isinstance(entries, list):
        raise ValueError("Additional capabilities must be a list")
    entries_by_id = {}
    fields = {"id", "repository_url", "source_commit", "license", "repository_verified", "verified_at"}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != fields:
            raise ValueError("Invalid addition fields")
        ident = entry["id"]
        if ident not in ADDITIONAL_IDS or ident in entries_by_id:
            raise ValueError("Unknown or duplicate additional capability")
        if entry["repository_url"] != "https://github.com/michaeljabbour/amplifier-capability-" + ident or entry["license"] != "MIT":
            raise ValueError("Addition canonical identity or license differs")
        if type(entry["repository_verified"]) is not bool:
            raise ValueError("Repository verification must be an explicit boolean")
        pin = entry["source_commit"]
        if pin is not None and (not isinstance(pin, str) or not re.fullmatch(r"[0-9a-f]{40}", pin) or pin == "0" * 40):
            raise ValueError("Addition requires a complete non-placeholder source commit")
        if entry["verified_at"] is not None:
            try:
                reviewed = datetime.fromisoformat(entry["verified_at"].replace("Z", "+00:00"))
            except (ValueError, AttributeError, TypeError) as exc:
                raise ValueError("Repository verification needs an ISO timestamp") from exc
            if reviewed.tzinfo is None or reviewed > datetime.now(timezone.utc):
                raise ValueError("Repository verification timestamp must be timezone-aware and not future-dated")
        entries_by_id[ident] = entry
    projects = catalogue.get("projects", [])
    ids = [project.get("id") for project in projects]
    if len(ids) != len(set(ids)) or set(ids) != HISTORICAL_IDS | set(entries_by_id):
        raise ValueError("Catalogue must retain the historical 33 plus exactly its named admitted additions")
    verified = publication["publication_ready"] and all(
        entry["repository_verified"] and entry["source_commit"] and entry["verified_at"]
        for entry in entries
    )
    if not verified and not preview:
        raise ValueError("Additions are not cleared for public activation; explicit local preview only")
    return {"preview_only": bool(preview), "publication_ready": bool(verified and not preview), "additions": entries_by_id, "capability_ids": sorted(ids)}


def current_admission(root, catalogue, migration):
    return validate_catalogue(catalogue, migration, load_publication(root),
                              preview=os.environ.get("PORTFOLIO_PREVIEW") == "1",
                              ci=os.environ.get("GITHUB_ACTIONS") == "true")
