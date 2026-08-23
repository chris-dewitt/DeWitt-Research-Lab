# Local Atticus run records

`atticus-demo` writes one JSON file here per run. The files are gitignored.

Each record is ids and scores only: task id, planner line, plan source, tool
names, evidence ids, EvalForge score, artifact keys, and the workflow digest.
It does **not** store the objective, prompts, evidence text, tool arguments,
trace messages, or limitations. That is the AGENTS.md default: do not log
prompt or tool content.

Progress during a run goes to stderr as `progress: <event> <detail>` lines so
a multi-minute CPU generation is not silent. `--json` still prints the full
result on stdout when you ask for it.

Override the directory with `ATTICUS_RUN_RECORD_DIR`.
