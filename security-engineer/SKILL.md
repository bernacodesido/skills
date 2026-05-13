---
name: security-engineer
description: >
  Vulnerability finding, CVE detection, dependency auditing, security configuration assessment, supply attack detection, OWASP Top 10 testing, XSS/SQLi detection, API security assessment, and authentication testing
license: MIT
compatibility: Works with Claude.ai, Claude Code, and the Claude API.
metadata:
  author: Bernardo Codesido
  version: 1.0.0
---

# 🔎 Vulnerability Scanning & Assessment

## Overview

This skill enables Claude to assist with comprehensive vulnerability scanning and security assessment operations. It covers CVE detection, dependency auditing, configuration review, CVSS scoring, supply chain attacks detection, OWASP Top 10 testing, XSS/SQLi detection, API security assessment, and authentication testing, along with automated vulnerability reporting.

---

## Core Capabilities

### 1. Dependency Vulnerability Auditing

Claude can analyze project dependencies for known vulnerabilities:

**When the user asks to audit dependencies:**

1. Identify the project's package manager (pip, npm, go, maven, cargo, etc.)
2. Parse dependency files (requirements.txt, package.json, go.mod, pom.xml, Cargo.toml)
3. Extract exact versions for all direct and transitive dependencies
4. Checks if dependencies versions are pinned or if there are version ranges
5. Query the OSV (Open Source Vulnerabilities) database and NVD for known CVEs
6. Map each vulnerability to its CVSS score and severity level
7. Check if patched versions are available
8. Generate a prioritized remediation report
9. Suggest minimum version upgrades to resolve vulnerabilities

**Supported dependency files:**
| Language | Files |
|----------|-------|
| Python | `requirements.txt`, `Pipfile.lock`, `pyproject.toml`, `setup.py` |
| JavaScript | `package.json`, `package-lock.json`, `yarn.lock` |
| Go | `go.mod`, `go.sum` |
| Java | `pom.xml`, `build.gradle` |
| Rust | `Cargo.toml`, `Cargo.lock` |
| Ruby | `Gemfile`, `Gemfile.lock` |
| PHP | `composer.json`, `composer.lock` |

### 2. Configuration Security Auditing

Claude can review server and application configurations for security issues:

**When the user asks to audit configurations:**

1. Parse the configuration file format (nginx, Apache, SSH, Docker, Kubernetes)
2. Check against CIS Benchmarks and security best practices
3. Identify dangerous defaults left unchanged
4. Flag overly permissive settings (wide-open CORS, directory listing, debug mode)
5. Check for missing security-hardening directives
6. Compare against known-good baseline configurations
7. Generate findings with severity, description, and remediation steps

**Supported configurations:**

- **Web Servers**: Nginx, Apache, IIS, Caddy
- **SSH**: OpenSSH `sshd_config`
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis
- **Container**: Dockerfile, docker-compose.yml, Kubernetes manifests
- **Cloud**: AWS Security Groups, IAM Policies, S3 Bucket policies

### 3. CVSS Scoring & Risk Assessment

Claude can calculate and explain CVSS scores:

**When the user asks about CVSS:**

1. Calculate CVSS v3.1 Base Score from attack vector metrics
2. Explain each metric's contribution to the score
3. Determine severity rating (None, Low, Medium, High, Critical)
4. Apply Temporal and Environmental adjustments if data is available
5. Generate risk matrices for multiple vulnerabilities
6. Prioritize remediation based on exploitability and impact

### 4. OWASP Top 10 Assessment

**When the user asks to test for OWASP Top 10:**

| #   | Vulnerability             | Testing Approach                                                                  |
| --- | ------------------------- | --------------------------------------------------------------------------------- |
| A01 | Broken Access Control     | Test IDOR, path traversal, forced browsing, missing function-level access control |
| A02 | Cryptographic Failures    | Audit TLS config, check for sensitive data in transit/at rest, weak algorithms    |
| A03 | Injection                 | Test SQL, NoSQL, OS command, LDAP, XPath injection vectors                        |
| A04 | Insecure Design           | Review architecture for missing security controls                                 |
| A05 | Security Misconfiguration | Check default configs, unnecessary features, error handling                       |
| A06 | Vulnerable Components     | Audit third-party libraries and frameworks                                        |
| A07 | Auth & ID Failures        | Test session management, credential storage, MFA, brute force                     |
| A08 | Software & Data Integrity | Check for unsigned updates, insecure deserialization, CI/CD security              |
| A09 | Logging & Monitoring      | Verify logging coverage, monitoring gaps, incident detection                      |
| A10 | SSRF                      | Test for server-side request forgery in URL parameters                            |

### 5. Injection Testing

**When the user asks to test for injections:**

1. Map all input points (forms, headers, cookies, URL parameters, JSON body)
2. Test each input with injection payloads appropriate to the context
3. Detect blind injection through timing or boolean differences
4. Test for second-order injection (stored payloads triggered later)
5. Test for NoSQL injection in MongoDB/Elasticsearch applications
6. Check for template injection (SSTI) in Jinja2, Twig, Freemarker
7. Test for command injection through shell metacharacters
8. Document PoC steps for confirmed findings

### 6. API Security Testing

**When the user asks to test API security:**

1. Parse OpenAPI/Swagger specifications
2. Test all endpoints for authentication requirements
3. Check for broken object-level authorization (BOLA)
4. Test rate limiting and throttling
5. Check for mass assignment vulnerabilities
6. Validate input/output schemas
7. Test for excessive data exposure
8. Check for security-relevant headers (CORS, CSP, etc.)
9. Test GraphQL-specific issues (introspection, batching attacks)

### 7. Authentication & Session Testing

**When the user asks to test authentication:**

1. Test password policies and brute-force protections
2. Analyze session token entropy and predictability
3. Test session fixation and session hijacking
4. Check for insecure "remember me" implementations
5. Test OAuth/OIDC flows for misconfigurations
6. Verify MFA implementation and bypass attempts
7. Test password reset flow security
8. Check for credential stuffing protections

### 8. XSS Detection & Exploitation

**When the user asks about XSS:**

1. Map all reflection points (reflected, stored, DOM-based)
2. Test basic payloads with various encoding bypasses
3. Identify WAF/filter rules and develop bypasses
4. Test for DOM-based XSS through JavaScript analysis
5. Craft context-specific payloads (HTML, attribute, JavaScript, URL)
6. Demonstrate impact (session theft, keylogging, phishing)
7. Generate remediation recommendations

### 9. Vulnerability Report Generation

Generate professional vulnerability assessment reports:

**When the user asks for a report:**

1. Compile all findings with severity classification
2. Include executive summary for management audience
3. Provide technical details for each finding
4. Include proof-of-concept steps where applicable
5. List remediation recommendations prioritized by risk
6. Generate compliance mapping (PCI-DSS, SOC2, ISO 27001)
7. Export in multiple formats (JSON, HTML, Markdown, PDF-ready)

### 10. Supply Chain Attack Detection

**When the user asks about supply chain attacks:**

1. Analyze software bill of materials (SBOM) for dependencies
2. Check for known vulnerable versions in the supply chain
3. Monitor for typosquatting and malicious packages in public registries
4. Analyze CI/CD pipelines for security weaknesses
5. Check for unauthorized access to source code repositories
6. Monitor for anomalous activity in build and deployment processes
7. Generate alerts for suspicious changes in dependencies or configurations


### 11. OSSF Score Analysis

**When the user asks about OSSF Scorecard:**
1. Search for Binary-Artifacts
2. Analyze CI/CD workflows for unsecure patterns
3. Validate if there is a dependency update tool
4. Check for the presence of a LICENSE file
5. Check for the presence of a SECURITY.md file
6. Validate that dependencies are pinned to specific versions through SHA digests or version numbers.
7. Ensure static analysis tools are integrated

---

## Usage Instructions

### Example Prompts

```
> Audit the Python dependencies in this project for known CVEs
> Review this nginx configuration for security issues
> Calculate the CVSS v3.1 score for a remote code execution via unauthenticated API
> Generate a vulnerability assessment report from these scan results
> Check if any of these software versions have known exploits
> Test this web application for OWASP Top 10 vulnerabilities
> Check this API for authentication bypass issues
> Generate XSS payloads that bypass this WAF
> Test these input fields for SQL injection
> Review the authentication flow of this application
> Assess the CORS configuration of this API
> Analyze this project with OSSF Scorecard
```

---

## Integration Guide

### Chaining with Other Skills

- **← Recon & OSINT (01)**: Receive discovered hosts and services for scanning
- **→ Exploit Development (03)**: Pass confirmed vulnerabilities for PoC development
- **→ Blue Team Defense (15)**: Generate remediation and hardening recommendations
- **→ CSOC Automation (11)**: Auto-generate tickets for discovered vulnerabilities

---

## References

- [NVD — National Vulnerability Database](https://nvd.nist.gov/)
- [OSV — Open Source Vulnerabilities](https://osv.dev/)
- [CVSS v3.1 Specification](https://www.first.org/cvss/v3.1/specification-document)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)