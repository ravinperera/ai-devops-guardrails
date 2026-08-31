# Repository Validation

The repository uses a lightweight GitHub Actions workflow to catch basic documentation and configuration mistakes without requiring cloud credentials or access to production systems.

## Checks performed

The workflow runs on pull requests and pushes to `main`.

### Text-hygiene regression tests

`tests/test_check_text_hygiene.py` exercises the dependency-free text validator against valid UTF-8 content, trailing whitespace, missing final newlines, NUL bytes, invalid UTF-8, high-confidence credential shapes, and redacted examples. This protects the validator's expected failure behaviour as the repository evolves.

### Markdown, Python, and YAML text hygiene

`scripts/check-text-hygiene.py` examines tracked Markdown, Python, and YAML files and verifies that they:

- are valid UTF-8 text;
- do not contain NUL bytes;
- end with a final newline;
- do not contain trailing spaces or tabs; and
- do not contain a narrow set of obvious credential-shaped values such as AWS access-key IDs, GitHub personal access tokens, OpenAI-style API keys, or PEM private-key headers.

The credential patterns are intentionally conservative. Redacted placeholders remain valid, and the check is not a replacement for GitHub secret scanning, provider-side revocation, or scanning repository history after an exposure.

The script uses only the Python standard library and `git ls-files`, so contributors do not need to install a package manager dependency.

### Repository-local Markdown links

`scripts/check-markdown-links.py` verifies links between tracked Markdown files and other repository-local targets without making network requests. It rejects missing targets and paths that escape the repository, while ignoring external URLs, page anchors, and links shown inside fenced examples.

`tests/test_check_markdown_links.py` covers existing and missing targets, repository escapes, external URLs, anchors, fenced examples, and URL-encoded local paths.

The link check is intentionally local-only. It does not crawl external sites or prove that an external reference is current or trustworthy.

### YAML syntax

Ruby's YAML parser reads every tracked `.yml` and `.yaml` file. This catches malformed workflow or configuration syntax before merge.

The check validates syntax only. It does not prove that a workflow, policy, or tool-specific configuration is semantically correct.

### Python helper syntax

`python3 -m compileall -q scripts` compiles repository helper scripts to catch Python syntax errors.

## Run the checks locally

From the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_check_text_hygiene.py' -v
python3 scripts/check-text-hygiene.py
python3 -m unittest discover -s tests -p 'test_check_markdown_links.py' -v
python3 scripts/check-markdown-links.py

git ls-files -z '*.yml' '*.yaml' |
  ruby -e 'require "yaml"; STDIN.read.split("\0").reject(&:empty?).each { |path| YAML.parse_file(path); puts "validated #{path}" }'

python3 -m compileall -q scripts
```

## Checks intentionally not included

The validation workflow deliberately remains small and credential-free.

It does not currently:

- execute infrastructure plans or deployments;
- connect to AWS, Kubernetes, registries, secret stores, or production systems;
- prove that an AI agent will follow the instructions consistently;
- perform a complete Markdown style review;
- crawl external links, which can introduce flaky network-dependent failures;
- scan commit history for previously exposed secrets; or
- replace security review, branch protection, required approvals, or code-owner review.

These omissions are intentional. Stronger checks should be added only when they have a clear maintenance owner, stable inputs, and a documented response process for failures.

## Workflow safety properties

The workflow:

- has read-only repository permissions;
- uses no repository or environment secrets;
- has a five-minute timeout;
- cancels superseded runs for the same ref; and
- performs no write, deployment, or cloud-authentication action.

A future change that adds credentials, write permissions, third-party actions, artifact publication, or network-dependent validation should receive an explicit GitHub Actions and supply-chain review.
