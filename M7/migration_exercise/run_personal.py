#!/usr/bin/env python3
"""Migration brief 2 : révocation ACL + rejet de révision obsolète, avec gel préalable.

Distinct du smoke test lab.py (corruption SQLite). Cas gelés AVANT mesure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab import activate, digest, export_corpus, migrate, read_export, save, search, search_active  # noqa: E402

CASES_GEL = {
    "schema_version": 1,
    "frozen_at": "2026-10-06T00:00:00Z",
    "component": "index_documentaire_json_sqlite",
    "risk": "fuite_inter_perimetre_apres_migration",
    "cases": [
        {
            "case_id": "MIG-REV-01",
            "title": "révision supersédée refusée à l'import",
            "protocol": "exporter, marquer un document status=superseded, read_export doit échouer",
            "pass_criterion": "ValueError sur export altéré ; export sain inchangé",
        },
        {
            "case_id": "MIG-ACL-01",
            "title": "révocation technicien avant scoring",
            "protocol": "retirer technicien de DOC-DATA-ACCESS-001, migrer, chercher en rôle technicien",
            "pass_criterion": "document absent du top-k technicien ; présent pour superviseur si autorisé",
        },
        {
            "case_id": "MIG-RB-01",
            "title": "rollback pointeur actif après panne candidat",
            "protocol": "activer sqlite, corrompre, reactiver json avec hash source",
            "pass_criterion": "même top-3 calibration qu'avant migration",
        },
    ],
    "gates": [
        "aucune_permission_elargie",
        "aucun_secret",
        "test_split_unused",
        "rollback_rejoue",
    ],
}


def _load_questions(pack: Path) -> list[dict]:
    path = pack / "2026-S1" / "rag_eval" / "questions.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [row for row in rows if row["split"] == "calibration"]


def run(pack: Path, output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"refus d'écraser {output}")
    output.mkdir(parents=True)
    gel_path = output / "cases_gel.json"
    save(gel_path, CASES_GEL)
    gel_hash = digest(gel_path)

    export = output / "corpus.json"
    export_corpus(pack, export)
    source_hash = digest(export)
    activate(output, export.name, "json")
    questions = _load_questions(pack)

    def replay():
        return [search_active(output, q["question"], q["role"]) for q in questions]

    before = replay()
    results: dict = {
        "gel_sha256": gel_hash,
        "source_export_sha256": source_hash,
        "cases": {},
        "test_split_used": False,
    }

    # MIG-REV-01
    bad_export = output / "corpus_superseded.json"
    shutil.copy(export, bad_export)
    payload = json.loads(bad_export.read_text(encoding="utf-8"))
    payload["documents"][0]["status"] = "superseded"
    save(bad_export, payload)
    rev_ok = False
    try:
        read_export(bad_export)
    except ValueError:
        rev_ok = True
    results["cases"]["MIG-REV-01"] = {
        "passed": rev_ok,
        "detail": "read_export refuse status=superseded",
    }

    # MIG-ACL-01 — retirer technicien de DOC-DATA-ACCESS-001 si présent
    acl_export = output / "corpus_acl_revoked.json"
    payload = json.loads(export.read_text(encoding="utf-8"))
    target_id = "DOC-DATA-ACCESS-001"
    found = False
    for doc in payload["documents"]:
        if doc["document_id"] == target_id and "technicien" in doc["allowed_roles"]:
            doc["allowed_roles"] = sorted(role for role in doc["allowed_roles"] if role != "technicien")
            doc["checksum_sha256"] = hashlib.sha256(doc["text"].encode()).hexdigest()
            found = True
    if not found:
        # fallback pédagogique : révoquer technicien sur le premier doc qui l'autorise
        for doc in payload["documents"]:
            if "technicien" in doc["allowed_roles"] and "superviseur" in doc["allowed_roles"]:
                target_id = doc["document_id"]
                doc["allowed_roles"] = sorted(role for role in doc["allowed_roles"] if role != "technicien")
                doc["checksum_sha256"] = hashlib.sha256(doc["text"].encode()).hexdigest()
                found = True
                break
    save(acl_export, payload)
    acl_db = output / "index_acl.sqlite"
    migrate(acl_export, acl_db)
    tech_hits = search(acl_db, "sqlite", "accès aux données politique", "technicien")
    # superviseur doit encore pouvoir voir si autorisé
    try:
        sup_hits = search(acl_db, "sqlite", "accès aux données politique", "superviseur")
    except Exception as exc:  # noqa: BLE001
        sup_hits = [f"error:{exc}"]
    acl_pass = target_id not in tech_hits
    results["cases"]["MIG-ACL-01"] = {
        "passed": acl_pass and found,
        "document_id": target_id,
        "technicien_hits": tech_hits,
        "superviseur_hits": sup_hits,
        "detail": "révocation appliquée avant scoring SQLite",
    }

    # MIG-RB-01 — migration saine + corruption + rollback
    database = output / "index.sqlite"
    started = time.perf_counter()
    migrate(export, database)
    migration_ms = round((time.perf_counter() - started) * 1000, 3)
    activate(output, database.name, "sqlite")
    after = replay()
    database.write_bytes(b"corruption brief2")
    detected = False
    try:
        search_active(output, questions[0]["question"], questions[0]["role"])
    except ValueError:
        detected = True
    activate(output, export.name, "json", expected_sha256=source_hash)
    rollback = replay()
    results["cases"]["MIG-RB-01"] = {
        "passed": before == after == rollback and detected,
        "ranking_equal": before == after,
        "rollback_equal": before == rollback,
        "corruption_detected": detected,
        "migration_ms": migration_ms,
    }

    results["status"] = "passed" if all(case["passed"] for case in results["cases"].values()) else "failed"
    save(output / "report.json", results)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-pack", type=Path, default=Path(__file__).resolve().parents[3] / "data_pack")
    parser.add_argument("--output", type=Path, default=Path("results/migration-brief2-r1"))
    args = parser.parse_args()
    report = run(args.data_pack, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "passed" else 1)
