# Security Policy

## Scope and authorized use

This repository contains educational notes and code for controlled security labs, including Hack The Box. The material is not intended for unauthorized access, persistence, disruption, data extraction, or testing against third-party systems.

Only run the code against targets you own or are explicitly authorized to assess.

## Reporting a vulnerability in this repository

If you discover a security issue in the repository itself (for example, an accidentally committed credential or unsafe behavior), please do not publish the sensitive details in a public issue.

Contact the repository maintainer privately through the contact method listed on the GitHub profile. Include:

- A concise description of the issue
- The affected file or commit
- Reproduction steps that do not expose third-party data
- Suggested mitigation, if known

## Secret handling

Never commit passwords, access tokens, private keys, session cookies, cloud credentials, VPN configuration, or sensitive personal/network information.

If a secret is exposed, revoke or rotate it immediately. Removing it from the latest commit is not sufficient: assume it may remain in Git history, forks, caches, or logs.

## Safe defaults

Scripts should use configurable targets, explicit scope, connection timeouts, and certificate verification by default. Destructive operations must be clearly identified and require deliberate operator action.
