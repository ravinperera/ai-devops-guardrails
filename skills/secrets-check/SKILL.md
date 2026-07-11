# Secrets Check

Use this skill when reviewing code, configuration, logs, examples, pull requests or documentation for secret exposure.

## Goal

Prevent credentials and sensitive values from entering repositories, logs, examples or AI prompts.

## Check for

- API keys, tokens, passwords, private keys and certificates
- `.env`, `.npmrc`, `.pypirc`, kubeconfig and cloud credential files
- AWS access key IDs and secret access keys
- GitHub tokens and fine-grained PATs
- database URLs with usernames/passwords
- Slack, Stripe, SendGrid, Twilio or other service tokens
- private endpoints, internal hostnames or client-specific identifiers
- logs that include headers, cookies, tokens or authorization values
- examples that look fake but match real secret formats

## Required output

```text
Secrets risk: None observed / Low / Medium / High / Critical
Locations reviewed: files or paths
Potential exposures:
- [severity] file/path and reason
Required actions:
- rotate/revoke if real
- remove from history if committed
- move to secret manager
- add ignore/pre-commit scanning
Safe replacement examples:
- example
Recommendation: proceed / proceed after fixes / do not proceed
```

## Safe replacement guidance

Use placeholders that cannot be mistaken for real credentials:

```text
EXAMPLE_AWS_ACCESS_KEY_ID
EXAMPLE_DATABASE_PASSWORD
example-token-do-not-use
<replace-with-secret-manager-reference>
```

Never print full detected secrets back to the user. Show only a redacted form such as `abcd...wxyz` if needed.
