## Summary

<!-- What problem does this solve, and what changed? -->

## Change type

- [ ] Documentation or examples only
- [ ] Tests or validation only
- [ ] Guardrail or skill behaviour
- [ ] Adapter, automation, workflow, or script
- [ ] Other: <!-- describe -->

## Affected surface

<!-- List the instructions, skills, examples, scripts, or supported tools affected. -->

## Safety review

- Risk level: <!-- Low / Medium / High -->
- Blast radius: <!-- Files, users, tools, environments, or systems affected -->
- Permissions or identity impact: <!-- None, or describe -->
- Secrets or sensitive-data impact: <!-- None, or describe -->
- Supply-chain or dependency impact: <!-- None, or describe -->
- Infrastructure or production impact: <!-- None, or describe -->
- Rollback or removal: <!-- Revert, delete, disable, or other recovery path -->

- [ ] Examples use fictional, synthetic, or fully redacted values.
- [ ] No credentials, customer data, internal hostnames, or production identifiers are included.
- [ ] The change does not treat AI output as approval or proof of production safety.
- [ ] Any write, shell, cloud, deployment, destructive, or production-impacting action remains behind explicit approval.

## Validation performed

<!-- Record checks actually executed, results, and evidence. Do not list planned checks as completed. -->

```text
python3 -m unittest discover -s tests -p 'test_check_text_hygiene.py' -v
python3 scripts/check-text-hygiene.py
python3 -m unittest discover -s tests -p 'test_check_markdown_links.py' -v
python3 scripts/check-markdown-links.py

git ls-files -z '*.yml' '*.yaml' |
  ruby -e 'require "yaml"; STDIN.read.split("\0").reject(&:empty?).each { |path| YAML.parse_file(path); puts "validated #{path}" }'

python3 -m compileall -q scripts
```

## Validation limitations

<!-- What was not tested or cannot be proven by repository-level checks? -->

## Issue

<!-- Use Closes #<issue> when this pull request fully resolves an issue. -->
