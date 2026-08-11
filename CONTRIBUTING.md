# Contributing

Thank you for helping improve AI DevOps Guardrails. Contributions should make the guidance clearer, safer, easier to verify, or easier to adopt without expanding operational risk.

## Start with the smallest useful change

Prefer a focused pull request that solves one problem. Reuse the existing instruction, skill, example, and documentation structure before adding a new abstraction or adapter.

Open an issue before implementation when a proposal would:

- add or materially change an agent adapter, plugin, workflow, script, or automation path;
- request new GitHub permissions, credentials, cloud access, network access, or third-party actions;
- change the safety model, approval boundary, supported-tool claims, or release process;
- affect many files or introduce a new dependency;
- include behaviour that could write to repositories, infrastructure, or production systems.

Small documentation corrections, link fixes, fictional examples, and focused test improvements may proceed directly when their scope and validation are clear.

## Safety requirements

- Use fictional, synthetic, or fully redacted examples.
- Never include live credentials, tokens, customer data, internal hostnames, account identifiers, repository secrets, or production resource names.
- Do not present an AI review as a substitute for human approval, branch protection, security review, change management, or production verification.
- Keep write, shell, cloud, deployment, destructive, and production-impacting actions behind explicit approval.
- Describe blast radius, rollback, validation, and residual risk when a change affects operational guidance.
- Report sensitive weaknesses privately using [`SECURITY.md`](SECURITY.md).

## Local validation

Run the credential-free repository checks from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_check_text_hygiene.py' -v
python3 scripts/check-text-hygiene.py
python3 -m unittest discover -s tests -p 'test_check_markdown_links.py' -v
python3 scripts/check-markdown-links.py

git ls-files -z '*.yml' '*.yaml' |
  ruby -e 'require "yaml"; STDIN.read.split("\0").reject(&:empty?).each { |path| YAML.parse_file(path); puts "validated #{path}" }'

python3 -m compileall -q scripts
```

These checks exercise the text and link validators, validate repository text hygiene, validate YAML syntax, and compile Python helpers. External links are not crawled. The checks do not prove that an agent, policy, workflow, infrastructure change, or production system is safe.

## Pull request expectations

A useful pull request should explain:

- the problem and why the change is needed;
- the files and supported workflows affected;
- whether the change is documentation-only or changes behaviour;
- any permissions, identity, secret, supply-chain, infrastructure, or production implications;
- the validation performed and its limitations;
- rollback or removal steps when applicable;
- the related issue using `Closes #<issue>` when the change fully resolves it.

Keep the pull request ready for review only when the described validation has been completed and the diff contains no unrelated changes.
