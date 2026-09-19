#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from owner_publication import EVENT_CLASSES,OWNER_PUBLICATION_PATH
from relaylib import load_yaml,print_result
from takeoverlib import digest_mapping


def validate(root:Path):
    e=[];w=[];path=root/OWNER_PUBLICATION_PATH
    if not path.exists():return e,w
    data=load_yaml(path)
    if data.get("schema_version")!="relay-v2.5-owner-publication":e.append("OWNER_PUBLICATION schema_version must be relay-v2.5-owner-publication")
    publication=data.get("publication") or {};source=data.get("source") or {};baseline=data.get("baseline") or {}
    sequence=publication.get("sequence");pid=str(publication.get("id") or "")
    if not isinstance(sequence,int) or sequence<1:e.append("OWNER_PUBLICATION publication.sequence must be positive integer")
    if isinstance(sequence,int) and pid!=f"PUB-{sequence:04d}":e.append("OWNER_PUBLICATION publication.id must match publication.sequence")
    if publication.get("event_class") not in EVENT_CLASSES:e.append(f"OWNER_PUBLICATION event_class invalid: {publication.get('event_class')}")
    if not isinstance(publication.get("changed_dimensions"),list):e.append("OWNER_PUBLICATION changed_dimensions must be list")
    for key in ("owner_view_digest","report_projection_digest","normalized_report_digest"):
        if not str(publication.get(key) or "").startswith("sha256:"):e.append(f"OWNER_PUBLICATION publication.{key} must be sha256 digest")
    if not isinstance(source.get("report_sources"),dict):e.append("OWNER_PUBLICATION source.report_sources must be mapping")
    report=baseline.get("report")
    if not isinstance(report,dict):e.append("OWNER_PUBLICATION baseline.report must be mapping")
    else:
        expected=digest_mapping(report)
        if baseline.get("digest")!=expected:e.append("OWNER_PUBLICATION baseline.digest does not match baseline.report")
        if publication.get("normalized_report_digest")!=expected:e.append("OWNER_PUBLICATION normalized_report_digest does not match baseline.report")
        for key in ("task","implementation","evidence","quality","delivery_or_custody","execution","stop","roadmap","next_work","issues","owner_decisions"):
            if key not in report:e.append(f"OWNER_PUBLICATION baseline.report missing {key}")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))


if __name__=="__main__":
    main()
