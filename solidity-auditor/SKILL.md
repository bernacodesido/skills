---
name: solidity-auditor
description: >
  Use when the user asks to audit Solidity smart contracts.
  A skill for performing detailed security audits of Solidity smart contracts, following a comprehensive checklist of common vulnerability types and using the Immunefi severity classification system. This skill can operate in two modes: file mode (analyzing specified files) and diff mode (analyzing changes since a specified commit). The output is a structured report of any vulnerabilities found, or a statement confirming that no vulnerabilities were found.
license: MIT
compatibility: Works with Claude.ai, Claude Code, and the Claude API.
metadata: 
  author: Bernardo Codesido and Aureliano Calvo
  version: 1.0.0
---

# Auto Audit Skill for Solidity Smart Contracts

## Overview
This skill performs a detailed security audit of Solidity smart contracts. It follows a comprehensive checklist of common vulnerability types, including reentrancy, arithmetic issues, randomness weaknesses, encoding problems, signature issues, gas and loop vulnerabilities, flash loan and price manipulation risks, address assumptions, token interaction pitfalls, approval and transfer issues, access control weaknesses, external call risks, payment pattern problems, and risky Solidity constructs. The skill can operate in two modes: file mode (analyzing specified files) and diff mode (analyzing changes since a specified commit). The output is a structured report of any vulnerabilities found, classified by severity according to the Immunefi v2.3 system, or a statement confirming that no vulnerabilities were found.

---

## Core Capabilities

You are an expert in Solidity smart contract security who provides detailed and precise analyses. This analysis is part of a bigger audit — if no vulnerabilities are found, then none are found. Do not invent findings when the code is genuinely safe.

## Arguments

$ARGUMENTS

Parse the arguments as follows:
- One or more file paths to audit (required).
- An optional `--from <commit>` flag indicating a base commit for diff mode.

If no file paths were provided, ask the user for them before proceeding. If `--from` is not present, run in **file mode**. If `--from <commit>` is present, run in **diff mode**.

---

## Step 1 — Read the code

**File mode:** Use the Read tool to read each specified file. Then inspect import statements and use the Read tool to read each imported file as well. Repeat recursively until you have read the full dependency tree. Abstract contracts that are not themselves deployed can be read for context but should not be reported as standalone findings.

**Diff mode:** For each specified file:
1. Run `git diff <commit> -- <file>` (via Bash) to see what changed.
2. Run `git show <commit>:<file>` (via Bash) to read the file as it was at `<commit>`.
3. Use the Read tool to read the current version of the file.
4. Read imported dependencies as needed with the Read tool.

In diff mode, only report vulnerabilities **introduced or made exploitable by the changes**. Do not report issues that already existed at `<commit>`.

---

## Step 2 — Reason through the checklist

Work through every item below for each contract. Think carefully before concluding a vulnerability exists — only report issues you are certain of.

**Reentrancy**
- Standard reentrancy (ETH and token transfers before state updates)
- ERC-721 reentrancy (`onERC721Received` callback)
- Inter-function reentrancy (two functions sharing state, one called from the other)
- Inter-contract reentrancy (shared state across contracts)
- Inter-system reentrancy (cross-protocol callbacks)
- Read-only reentrancy (view functions returning stale state during a callback)

**Arithmetic**
- Integer overflow and underflow (especially in pre-0.8 code or unchecked blocks)
- Rounding errors and forced precision loss (e.g. minimum balance checks, division before multiplication)

**Randomness and time**
- Weak pseudo-randomness (block.timestamp, blockhash, or other on-chain sources used as entropy)
- Time manipulation (block.timestamp drift — miners can shift by a few minutes)

**Encoding and dispatch**
- Hash collision with `abi.encodePacked` on variable-length types
- Selector clashing (two functions with identical 4-byte selectors)

**Signatures**
- Signature replay (no nonce, no chain ID, or reusable across contexts)
- Signature malleability (s-value not restricted to the lower half)
- `ecrecover` returning the zero address on invalid signatures without a zero-address check

**Gas and loops**
- Unbounded loops that allow gas exhaustion or DoS
- Block stuffing attacks
- Unbounded gas consumption from external calls

**Flash loans and price**
- Flash loan attacks (including flash mints, e.g. Dai-style)
- Price manipulation via spot prices from AMMs used as oracles
- Inflating internal accounting by sending tokens directly to the contract

**Address assumptions**
- Unexpected addresses (e.g. a receiver pointing to another contract in the system)
- Addresses empty at deployment but populated later (contract deployment at a known address)
- Accepting arbitrary bytes from untrusted callers (malicious calldata)

**Token interactions**
- Tokens with blocklists (USDC, USDT)
- Pausable tokens
- Fee-on-transfer tokens (balance received < amount sent)
- Rebasing or airdrop tokens (balances modified outside transfers)
- Upgradable tokens (behaviour can change after audit)
- Flash-mintable tokens
- Tokens with multiple addresses
- Tokens with very low or very high decimals
- Tokens with non-string metadata (name/symbol)
- Weird ERC-20 tokens: ERC-777 hooks, missing return values, etc.

**Approvals and transfers**
- Approval race conditions (not using `increaseAllowance`/`decreaseAllowance`)
- Revert on approval to zero address
- Revert on zero-value transfers
- Revert on transfer to the zero address
- Revert on large approvals or transfers
- No revert on failure (silent transfer failure)
- `transferFrom` where `src == msg.sender` bypasses allowance checks
- Unusual or non-standard `permit` implementations
- Code injection via token name in interfaces that render it

**Access control and visibility**
- Missing or incorrect function visibility (`public` when it should be `internal`/`private`)
- Missing or incorrect access control modifiers
- Lack of calldata validation on privileged functions

**External calls**
- Gas griefing via external calls (sending just enough gas to fail)
- Unchecked return values (`call`, `send`, `transfer` return values ignored)
- Reverting external calls that an attacker can force to fail (griefing)
- Contracts that cannot receive Ether when the function expects it

**Payment patterns**
- Push payment misuse (prefer pull over push)
- Use of `send` or `transfer` instead of `call` (2300 gas stipend may be insufficient)

**Solidity constructs**
- Deprecated or risky constructs (`tx.origin` for auth, `selfdestruct`, `delegatecall` to untrusted addresses)
- Block re-org risks on chains susceptible to reorganisations

**Scope notes:**
- Include vulnerabilities inherited from parent contracts — they are part of the deployed bytecode.
- Do not flag abstract contracts as standalone findings — they are not deployed.

---

## Step 3 — Classify severity (Immunefi v2.3)

Assign severity using these criteria:

**Critical**
- Manipulation of governance voting result deviating from the voted outcome
- Direct theft of any user funds (at-rest or in-motion), other than unclaimed yield
- Direct theft of any user NFTs (at-rest or in-motion), other than unclaimed royalties
- Permanent freezing of funds
- Permanent freezing of NFTs
- Unauthorized minting of NFTs
- Predictable or manipulable RNG resulting in abuse of principal or NFT
- Unintended alteration of what the NFT represents (token URI, payload, artistic content)
- Protocol insolvency

**High**
- Theft of unclaimed yield
- Theft of unclaimed royalties
- Permanent freezing of unclaimed yield
- Permanent freezing of unclaimed royalties
- Temporary freezing of funds
- Temporary freezing of NFTs

**Medium**
- Smart contract unable to operate due to lack of token funds
- Block stuffing
- Griefing (no profit motive for attacker, but damage to users or the protocol)
- Theft of gas
- Unbounded gas consumption

**Low**
- Contract fails to deliver promised returns but does not lose value

**Explicitly out of scope:**
- Incorrect data supplied by third-party oracles (oracle manipulation / flash loan attacks are in scope)
- Basic economic and governance attacks (e.g. 51% attack)
- Lack of liquidity impacts
- Sybil attacks
- Centralization risks

---

## Step 4 — Output the report

Begin with a one-paragraph summary of what was analyzed (contracts, mode, scope).

Then, for each vulnerability found, output a section using this exact format:

---

### [SEVERITY] Title

**File(s):** `path/to/file.sol`

**Description:**
Detailed explanation of the vulnerability, naming the specific function(s) where the issue exists. If the issue is inherited from a parent contract, name that contract and its file.

**Exploit scenario:**
Concrete, step-by-step description of how an attacker would exploit this vulnerability, including any preconditions.

**Recommendation:**
Specific, actionable steps to fix the issue, including code patterns or references to safer alternatives where relevant.

---

If no vulnerabilities are found after working through the full checklist, output:

> No security vulnerabilities were found in the analyzed contract(s).
