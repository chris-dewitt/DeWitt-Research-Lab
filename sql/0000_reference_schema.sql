-- DRL reference persistence model. PostgreSQL 16+ target; production DDL evolves through reviewed migrations.
CREATE SCHEMA IF NOT EXISTS drl;

CREATE TABLE drl.subjects (
  subject_id text PRIMARY KEY,
  subject_type text NOT NULL CHECK (subject_type IN ('anonymous','user','service','device')),
  created_at timestamptz NOT NULL,
  disabled_at timestamptz,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE drl.sessions (
  session_id text PRIMARY KEY,
  subject_id text NOT NULL REFERENCES drl.subjects(subject_id),
  mode text NOT NULL CHECK (mode IN ('public-anonymous','public-authenticated','private-cloud','private-local','offline')),
  consent_snapshot_id text,
  created_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  ended_at timestamptz,
  privacy_profile text NOT NULL,
  CHECK (expires_at > created_at)
);

CREATE TABLE drl.consent_snapshots (
  consent_snapshot_id text PRIMARY KEY,
  subject_id text REFERENCES drl.subjects(subject_id),
  policy_version text NOT NULL,
  created_at timestamptz NOT NULL,
  expires_at timestamptz,
  analytics boolean NOT NULL,
  content_capture boolean NOT NULL,
  history boolean NOT NULL,
  research_donation boolean NOT NULL,
  allowed_research_uses jsonb NOT NULL DEFAULT '[]'::jsonb,
  snapshot_digest text NOT NULL UNIQUE
);
ALTER TABLE drl.sessions ADD CONSTRAINT sessions_consent_fk FOREIGN KEY (consent_snapshot_id) REFERENCES drl.consent_snapshots(consent_snapshot_id);

CREATE TABLE drl.task_runs (
  run_id text PRIMARY KEY,
  task_id text NOT NULL,
  session_id text NOT NULL REFERENCES drl.sessions(session_id),
  correlation_id text NOT NULL,
  trace_id text NOT NULL UNIQUE,
  idempotency_key text NOT NULL,
  state text NOT NULL,
  objective_redacted text,
  requested_skill text,
  code_revision text NOT NULL,
  config_digest text NOT NULL,
  model_route jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamptz NOT NULL,
  deadline timestamptz NOT NULL,
  started_at timestamptz,
  finished_at timestamptz,
  terminal_error jsonb,
  UNIQUE (session_id, idempotency_key)
);

CREATE TABLE drl.trace_events (
  trace_id text NOT NULL REFERENCES drl.task_runs(trace_id) ON DELETE CASCADE,
  sequence bigint NOT NULL,
  event_id text NOT NULL UNIQUE,
  parent_event_id text,
  step_id text,
  event_type text NOT NULL,
  system text NOT NULL,
  safe_summary text NOT NULL,
  payload jsonb NOT NULL,
  classification text NOT NULL,
  payload_digest text NOT NULL,
  occurred_at timestamptz NOT NULL,
  PRIMARY KEY (trace_id, sequence)
);

CREATE TABLE drl.artifacts (
  artifact_id text PRIMARY KEY,
  kind text NOT NULL,
  uri text NOT NULL,
  digest text NOT NULL,
  classification text NOT NULL,
  media_type text,
  source_system text NOT NULL,
  rights_id text,
  created_at timestamptz NOT NULL,
  expires_at timestamptz,
  UNIQUE (digest, uri)
);

CREATE TABLE drl.run_artifacts (
  run_id text NOT NULL REFERENCES drl.task_runs(run_id) ON DELETE CASCADE,
  artifact_id text NOT NULL REFERENCES drl.artifacts(artifact_id),
  role text NOT NULL,
  PRIMARY KEY (run_id, artifact_id, role)
);

CREATE TABLE drl.policy_decisions (
  decision_id text PRIMARY KEY,
  run_id text NOT NULL REFERENCES drl.task_runs(run_id) ON DELETE CASCADE,
  tool_call_id text NOT NULL,
  policy_version text NOT NULL,
  decision text NOT NULL CHECK (decision IN ('allow','deny','require-approval')),
  risk_tier text NOT NULL,
  reason_code text NOT NULL,
  request_digest text,
  required_scopes jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamptz NOT NULL,
  expires_at timestamptz
);

CREATE TABLE drl.approvals (
  approval_id text PRIMARY KEY,
  approval_request_id text NOT NULL,
  run_id text NOT NULL REFERENCES drl.task_runs(run_id) ON DELETE CASCADE,
  request_digest text NOT NULL,
  decision text NOT NULL CHECK (decision IN ('approved','denied','cancelled')),
  scopes jsonb NOT NULL,
  decided_by text NOT NULL,
  decision_version bigint NOT NULL,
  device_id text,
  created_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL
);

CREATE TABLE drl.evidence_items (
  evidence_id text PRIMARY KEY,
  source_uri text NOT NULL,
  source_system text NOT NULL,
  source_version text NOT NULL,
  published_at timestamptz,
  effective_at timestamptz,
  as_of_eligible_at timestamptz,
  retrieved_at timestamptz NOT NULL,
  content_digest text NOT NULL,
  locator jsonb NOT NULL,
  classification text NOT NULL,
  rights_id text NOT NULL
);

CREATE TABLE drl.claims (
  claim_id text PRIMARY KEY,
  run_id text REFERENCES drl.task_runs(run_id) ON DELETE CASCADE,
  claim_type text NOT NULL,
  claim_text text NOT NULL,
  confidence numeric,
  confidence_basis text,
  as_of timestamptz NOT NULL
);

CREATE TABLE drl.claim_evidence (
  claim_id text NOT NULL REFERENCES drl.claims(claim_id) ON DELETE CASCADE,
  evidence_id text NOT NULL REFERENCES drl.evidence_items(evidence_id),
  relation text NOT NULL CHECK (relation IN ('supports','contradicts')),
  PRIMARY KEY (claim_id, evidence_id, relation)
);

CREATE INDEX task_runs_session_created_idx ON drl.task_runs(session_id, created_at DESC);
CREATE INDEX trace_events_type_time_idx ON drl.trace_events(event_type, occurred_at DESC);
CREATE INDEX evidence_asof_idx ON drl.evidence_items(as_of_eligible_at, source_system);
CREATE INDEX claims_run_idx ON drl.claims(run_id);

-- Production work still requires RLS/tenant policies, retention partitions/jobs, encryption design,
-- migration ownership, backup/restore testing, performance indexes, and PII/content minimization.
