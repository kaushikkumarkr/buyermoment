from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .commercial import AdExperiment, CampaignOutcome, CommercialContextOutcome, PilotRequest
from .commercial_workflow import outcome_lineage


class ExperimentLedger:
    """Small portable SQLite ledger for immutable experiment/outcome lineage."""

    def __init__(self, path: Path = Path("data/phase7/experiment_ledger.sqlite3")) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS experiments (
                    experiment_id TEXT PRIMARY KEY,
                    buyer_moment_id TEXT NOT NULL,
                    business_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outcomes (
                    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT NOT NULL,
                    buyer_moment_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    imported_at TEXT NOT NULL,
                    UNIQUE(experiment_id, buyer_moment_id, date, payload_json)
                );
                CREATE TABLE IF NOT EXISTS context_outcomes (
                    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT NOT NULL,
                    buyer_moment_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS pilot_requests (
                    request_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                """
            )

    def save_experiment(self, experiment: AdExperiment) -> None:
        payload = json.dumps(experiment.model_dump(mode="json"), sort_keys=True)
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO experiments(experiment_id, buyer_moment_id, business_id, payload_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (experiment.experiment_id, experiment.buyer_moment_id, experiment.business_id, payload, experiment.created_at.isoformat()),
            )

    def save_outcome(self, outcome: CampaignOutcome) -> CommercialContextOutcome:
        with self._connect() as connection:
            row = connection.execute("SELECT payload_json FROM experiments WHERE experiment_id = ?", (outcome.experiment_id,)).fetchone()
            if row is None:
                raise ValueError(f"Experiment not found: {outcome.experiment_id}")
            experiment = AdExperiment.model_validate_json(row["payload_json"])
            lineage = outcome_lineage(experiment, outcome)
            payload = json.dumps(outcome.model_dump(mode="json"), sort_keys=True)
            connection.execute(
                "INSERT OR IGNORE INTO outcomes(experiment_id, buyer_moment_id, date, payload_json, imported_at) VALUES (?, ?, ?, ?, datetime('now'))",
                (outcome.experiment_id, outcome.buyer_moment_id, outcome.date, payload),
            )
            connection.execute(
                "INSERT INTO context_outcomes(experiment_id, buyer_moment_id, payload_json, created_at) VALUES (?, ?, ?, datetime('now'))",
                (lineage.experiment_id, lineage.buyer_moment_id, json.dumps(lineage.model_dump(mode="json"), sort_keys=True)),
            )
            return lineage

    def list_experiments(self) -> list[dict]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute("SELECT * FROM experiments ORDER BY created_at DESC")]

    def list_outcomes(self) -> list[dict]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute("SELECT * FROM outcomes ORDER BY date DESC")]

    def save_pilot_request(self, request: PilotRequest) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO pilot_requests(request_id, timestamp, payload_json) VALUES (?, ?, ?)",
                (request.request_id, request.timestamp.isoformat(), json.dumps(request.model_dump(mode="json"), sort_keys=True)),
            )
