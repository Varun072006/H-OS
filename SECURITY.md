# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in HumanOS, please report it responsibly.

### DO

- Email security concerns to: **security@humanos.dev** (placeholder)
- Include a detailed description of the vulnerability
- Provide steps to reproduce if possible
- Allow reasonable time for a fix before public disclosure

### DO NOT

- Open a public GitHub issue for security vulnerabilities
- Exploit the vulnerability beyond what is necessary to demonstrate it
- Access or modify other users' data

## Response Timeline

| Action | Target Time |
|--------|-------------|
| Initial acknowledgment | 24 hours |
| Severity assessment | 48 hours |
| Fix development | 7 days (critical), 30 days (high), 90 days (medium/low) |
| Public disclosure | After fix is released |

## Scope

The following are in scope for security reports:

- Authentication and authorization bypasses
- Data exposure or leakage (especially privacy-related)
- Remote code execution
- Injection vulnerabilities
- Cryptographic weaknesses
- Model theft or unauthorized model access
- Privacy boundary violations (raw frame persistence)

## Security Practices

See the [Security Considerations](README.md#15--security-considerations) section in the README for our security architecture and practices.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest release | ✅ |
| Previous minor | ✅ (security fixes only) |
| Older versions | ❌ |
