# Repository Validation

The repository uses a lightweight GitHub Actions workflow to catch basic documentation and configuration mistakes without requiring cloud credentials or access to production systems.

## Checks performed

The workflow runs on pull requests and pushes to `main`.

### Markdown and YAML text hygiene

`scripts/check-text-hygiene.py` examines tracked Markdown and YAML files and verifies that they:

- are valid UTF-8 text;
- do not contain NUL bytes;
- end with a final newline; and
- do not contain trailing spaces or tabs.

The script uses only the Python standard library and `git ls-files`, so contributors do not need to install a package manager dependency.

### YAML syntax

Ruby's YAML parser reads every tracked `.yml` and `.yaml` file. This catches malformed workflow or configuration syntax before merge.

The check validates syntax only. It does not prove that a workflow, policy, or tool-specific configuration is semantically correct.

### Python helper syntax

`python3 -m compileall -q scripts` compiles repository helper scripts to catch Python syntax errors.

## Run the checks locally

From the repository root:

```bash
python3 scripts/check-text-hygiene.py

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
