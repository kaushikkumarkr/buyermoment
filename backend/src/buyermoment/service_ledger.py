from __future__ import annotations

import json
from typing import Any

from .ledger import ExperimentLedger
from .service_models import (
    Client,
    ClientReport,
    DesignPartnerFeedbackV2,
    EvidenceChunk,
    EvidenceSource,
    ExperimentPortfolio,
    HumanApproval,
    AnalysisRun,
    MeasurementAudit,
)


class ServiceLedger(ExperimentLedger):
    """Portable client-scoped store layered on the existing experiment ledger."""

    def _initialize(self) -> None:
        super()._initialize()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    client_id TEXT PRIMARY KEY,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS evidence_sources (
                    source_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS evidence_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS portfolios (
                    client_id TEXT PRIMARY KEY,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS approvals (
                    approval_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS feedback_v2 (
                    feedback_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reports (
                    report_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS analysis_runs (
                    run_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS measurement_audits (
                    client_id TEXT PRIMARY KEY,
                    payload_json TEXT NOT NULL
                );
                """
            )

    def _save(self, table: str, key: str, client_id: str, payload: dict[str, Any], key_name: str) -> None:
        with self._connect() as connection:
            connection.execute(
                f"INSERT OR REPLACE INTO {table}({key_name}, client_id, payload_json) VALUES (?, ?, ?)",
                (key, client_id, json.dumps(payload, sort_keys=True)),
            )

    def save_client(self, client: Client) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO clients(client_id, payload_json) VALUES (?, ?)",
                (client.id, json.dumps(client.model_dump(mode="json"), sort_keys=True)),
            )

    def get_client(self, client_id: str) -> Client | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload_json FROM clients WHERE client_id = ?", (client_id,)).fetchone()
        return Client.model_validate_json(row["payload_json"]) if row else None

    def list_clients(self) -> list[Client]:
        with self._connect() as connection:
            rows = connection.execute("SELECT payload_json FROM clients ORDER BY client_id").fetchall()
        return [Client.model_validate_json(row["payload_json"]) for row in rows]

    def save_source(self, source: EvidenceSource, chunks: list[EvidenceChunk]) -> None:
        self._save("evidence_sources", source.id, source.client_id, source.model_dump(mode="json"), "source_id")
        with self._connect() as connection:
            for chunk in chunks:
                connection.execute(
                    "INSERT OR REPLACE INTO evidence_chunks(chunk_id, client_id, source_id, payload_json) VALUES (?, ?, ?, ?)",
                    (chunk.id, chunk.client_id, chunk.source_id, json.dumps(chunk.model_dump(mode="json"), sort_keys=True)),
                )

    def list_sources(self, client_id: str) -> list[EvidenceSource]:
        with self._connect() as connection:
            rows = connection.execute("SELECT payload_json FROM evidence_sources WHERE client_id = ? ORDER BY source_id", (client_id,)).fetchall()
        return [EvidenceSource.model_validate_json(row["payload_json"]) for row in rows]

    def list_chunks(self, client_id: str) -> list[EvidenceChunk]:
        with self._connect() as connection:
            rows = connection.execute("SELECT payload_json FROM evidence_chunks WHERE client_id = ? ORDER BY chunk_id", (client_id,)).fetchall()
        return [EvidenceChunk.model_validate_json(row["payload_json"]) for row in rows]

    def save_portfolio(self, portfolio: ExperimentPortfolio) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO portfolios(client_id, payload_json) VALUES (?, ?)",
                (portfolio.client_id, json.dumps(portfolio.model_dump(mode="json"), sort_keys=True)),
            )

    def get_portfolio(self, client_id: str) -> ExperimentPortfolio | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload_json FROM portfolios WHERE client_id = ?", (client_id,)).fetchone()
        return ExperimentPortfolio.model_validate_json(row["payload_json"]) if row else None

    def save_approval(self, approval: HumanApproval) -> None:
        self._save("approvals", approval.id, approval.client_id, approval.model_dump(mode="json"), "approval_id")

    def save_feedback(self, feedback: DesignPartnerFeedbackV2) -> None:
        self._save("feedback_v2", feedback.id, feedback.client_id, feedback.model_dump(mode="json"), "feedback_id")

    def save_report(self, report: ClientReport) -> None:
        self._save("reports", report.id, report.client_id, report.model_dump(mode="json"), "report_id")

    def save_analysis_run(self, run: AnalysisRun) -> None:
        self._save("analysis_runs", run.run_id, run.client_id, run.model_dump(mode="json"), "run_id")

    def list_analysis_runs(self, client_id: str) -> list[AnalysisRun]:
        with self._connect() as connection:
            rows = connection.execute("SELECT payload_json FROM analysis_runs WHERE client_id = ? ORDER BY run_id DESC", (client_id,)).fetchall()
        return [AnalysisRun.model_validate_json(row["payload_json"]) for row in rows]

    def save_measurement_audit(self, audit: MeasurementAudit) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO measurement_audits(client_id, payload_json) VALUES (?, ?)",
                (audit.client_id, json.dumps(audit.model_dump(mode="json"), sort_keys=True)),
            )

    def get_measurement_audit(self, client_id: str) -> MeasurementAudit | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload_json FROM measurement_audits WHERE client_id = ?", (client_id,)).fetchone()
        return MeasurementAudit.model_validate_json(row["payload_json"]) if row else None
