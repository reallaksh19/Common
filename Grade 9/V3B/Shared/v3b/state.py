"""Single transactional owner for immutable packets and optimistic acceptance."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .contracts import canonical, digest, require


class RunStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        require((self.root / "run.sqlite3").is_file(), "RUN_NOT_INITIALIZED")
        self.connection = sqlite3.connect(self.root / "run.sqlite3", timeout=30)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys=ON")

    @classmethod
    def create(cls, root: Path, metadata: dict) -> "RunStore":
        root.mkdir(parents=True, exist_ok=True)
        require(not (root / "run.sqlite3").exists(), "RUN_ALREADY_EXISTS")
        db = sqlite3.connect(root / "run.sqlite3")
        db.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE bundles(id TEXT PRIMARY KEY, revision INTEGER NOT NULL,
                                 epoch INTEGER NOT NULL, cursor INTEGER NOT NULL);
            CREATE TABLE packets(digest TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE accepted(bundle TEXT NOT NULL REFERENCES bundles(id),
                stage TEXT NOT NULL, digest TEXT NOT NULL REFERENCES packets(digest),
                actor TEXT NOT NULL, PRIMARY KEY(bundle, stage));
            CREATE TABLE events(sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                bundle TEXT, kind TEXT NOT NULL, body TEXT NOT NULL);
        """)
        with db:
            for key, value in metadata.items():
                db.execute("INSERT INTO metadata VALUES (?,?)", (key, canonical(value).decode()))
            for bundle in metadata["bundles"]:
                db.execute("INSERT INTO bundles VALUES (?,0,1,0)", (bundle["bundle_id"],))
        db.close()
        return cls(root)

    def close(self) -> None:
        self.connection.close()

    def metadata(self) -> dict:
        return {x["key"]: json.loads(x["value"]) for x in self.connection.execute("SELECT * FROM metadata")}

    def bundle(self, bundle_id: str) -> dict:
        row = self.connection.execute("SELECT * FROM bundles WHERE id=?", (bundle_id,)).fetchone()
        require(row is not None, "BUNDLE_UNKNOWN", bundle_id)
        return dict(row)

    def packets(self, bundle_id: str) -> dict:
        rows = self.connection.execute("""SELECT a.stage,a.actor,p.body,p.digest
            FROM accepted a JOIN packets p ON a.digest=p.digest WHERE a.bundle=?""", (bundle_id,))
        return {x["stage"]: {"actor": x["actor"], "digest": x["digest"],
                             "payload": json.loads(x["body"])} for x in rows}

    def accept(self, bundle_id: str, stage: str, actor: str, payload: dict,
               expected_revision: int, expected_epoch: int) -> dict:
        body, fingerprint = canonical(payload).decode(), digest(payload)
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            current = self.bundle(bundle_id)
            require(current["epoch"] == expected_epoch, "STALE_CUSTODY_EPOCH")
            previous = self.connection.execute(
                "SELECT digest,actor FROM accepted WHERE bundle=? AND stage=?", (bundle_id, stage)).fetchone()
            if previous is not None:
                require(previous["digest"] == fingerprint and previous["actor"] == actor,
                        "CANONICAL_ACCEPTANCE_ALREADY_EXISTS", stage)
                self.connection.rollback()
                return {"digest": fingerprint, "idempotent": True, **current}
            require(current["revision"] == expected_revision, "STALE_INPUT_REVISION")
            self.connection.execute("INSERT OR IGNORE INTO packets VALUES (?,?)", (fingerprint, body))
            self.connection.execute("INSERT INTO accepted VALUES (?,?,?,?)", (bundle_id, stage, fingerprint, actor))
            self.connection.execute("UPDATE bundles SET revision=revision+1,cursor=cursor+1 WHERE id=?", (bundle_id,))
            event = {"stage": stage, "actor": actor, "digest": fingerprint,
                     "input_revision": expected_revision, "epoch": expected_epoch}
            self.connection.execute("INSERT INTO events(bundle,kind,body) VALUES (?,?,?)",
                                    (bundle_id, "ACCEPTED", canonical(event).decode()))
            self.connection.commit()
            return {"digest": fingerprint, "idempotent": False, **self.bundle(bundle_id)}
        except BaseException:
            self.connection.rollback()
            raise

    def reject(self, bundle_id: str, stage: str, actor: str, payload: dict, code: str) -> None:
        body = {"stage": stage, "actor": actor, "payload": payload, "reason_code": code}
        with self.connection:
            self.connection.execute("INSERT INTO events(bundle,kind,body) VALUES (?,?,?)",
                                    (bundle_id, "REJECTED", canonical(body).decode()))

    def invalidate(self, bundle_id: str, stages: list[str], reason: str,
                   expected_revision: int) -> dict:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            current = self.bundle(bundle_id)
            require(current["revision"] == expected_revision, "STALE_INPUT_REVISION")
            accepted = self.packets(bundle_id)
            removed = {x: accepted[x]["digest"] for x in stages if x in accepted}
            require(bool(removed), "NOTHING_TO_INVALIDATE")
            self.connection.executemany("DELETE FROM accepted WHERE bundle=? AND stage=?",
                                        [(bundle_id, x) for x in removed])
            remaining = len(accepted) - len(removed)
            self.connection.execute("UPDATE bundles SET revision=revision+1,epoch=epoch+1,cursor=? WHERE id=?",
                                    (remaining, bundle_id))
            event = {"reason": reason, "superseded": removed}
            self.connection.execute("INSERT INTO events(bundle,kind,body) VALUES (?,?,?)",
                                    (bundle_id, "INVALIDATED", canonical(event).decode()))
            self.connection.commit()
            return self.bundle(bundle_id)
        except BaseException:
            self.connection.rollback()
            raise

    def events(self) -> list[dict]:
        return [{**dict(x), "body": json.loads(x["body"])}
                for x in self.connection.execute("SELECT * FROM events ORDER BY sequence")]
