---
type: public-source-investigation
created: 2026-09-18
updated: 2026-09-18
status: evidence-reviewed-with-offline-model
scope: public-disclosures-and-documentation-no-live-security-testing
---

# Case 001 — When verified software betrays trust

## The question that started the trail

How can a system authenticate a software release correctly and still deliver something its maintainers never intended?

The strongest lead is not broken cryptography. It is **untrusted material crossing into a process that has authority**. An identity check can be correct while the authenticated process is acting on poisoned inputs. This is a synthesis of established security ideas, not a newly discovered vulnerability.

Research date: September 18, 2026. Method: public maintainer reports, primary security disclosures, official specifications and release documentation, plus an offline educational model. No third-party systems were scanned, no attack was attempted, and no malware was downloaded or executed.

## Clue 1: short-lived credentials did not remove the release boundary

TanStack's May 11 incident report attributes 84 malicious package versions across 42 packages to a chain involving untrusted pull-request execution, shared build-cache state, and publishing authority in a later release job. It reports that the intended publication step was skipped after test failures, yet malicious publication still occurred. This is the maintainers' reconstruction; private logs and individual compromised-package attestations were not independently examined here. [TanStack postmortem, updated May 15](https://tanstack.com/blog/npm-supply-chain-compromise-postmortem).

The maintainers' follow-up explains why ordinary credential-theft defenses were insufficient in this case: publishing already used short-lived, workflow-bound credentials. They describe removing release caches and unsafe trigger patterns, alongside other hardening. Importantly, this report does not imply those repositories remain vulnerable today. [TanStack hardening follow-up](https://tanstack.com/blog/incident-followup).

Contrast Mastra's June 16 incident: its maintainer report describes social engineering of an employee, followed by token-based malicious publication despite MFA being required for maintainers, because token bypass was allowed. These are different entry paths, not proof of a single culprit or universal exploit. [Mastra maintainer incident report, published June 17](https://github.com/mastra-ai/mastra/issues/18061).

**Inference:** “we use MFA” and “we use short-lived credentials” answer narrower questions than “can an untrusted process cause a release?” Both controls remain valuable; neither replaces analysis of the entire path.

## Clue 2: two very recent disclosures expose the handoff itself

The search then reached two September 16 disclosures. Both identify previously reported, fixed issues—not discoveries made by this investigation.

| Public disclosure | What crossed the boundary | Important limits |
|---|---|---|
| [GHSL-2026-225, actions/attest](https://securitylab.github.com/advisories/GHSL-2026-225_actions_attest/) | A privileged workflow trusted a branch choice supplied inside an artifact. Checking its syntax and an accompanying revision did not establish authorization to choose that destination. | Fixed September 14. The advisory notes collaborator-only pull requests and default-branch protection; it does not establish unrestricted public exploitation or a compromised release. |
| [GHSL-2026-204, SPIFFE SPIRE repository](https://securitylab.github.com/advisories/GHSL-2026-204_spiffe_spire_repository/) | Artifact extraction could overwrite executable helper code before the privileged consumer validated the artifact data. | Fix reported merged September 4. The described privileges concern issue and pull-request changes; do not inflate that into proof of arbitrary production access. |

The actions/attest [fix PR #488](https://github.com/actions/attest/pull/488) is visibly merged. Its description moves branch context to the platform event and restricts the supported origin/actor combination. It also corrects the artifact extraction layout. This is a concrete example of checking **who may designate a target**, not merely whether the target string looks valid.

The SPIRE advisory's complete text was available in the primary-source search result, while a later direct open failed through the retrieval tool. Its fix was not independently executed or exhaustively reviewed here. Neither issue should be confused with a break in attestation cryptography or the SPIFFE identity protocol.

## The distinction worth keeping

There are at least four separate questions:

1. **Identity:** which user or workflow exercised the authority?
2. **Provenance:** which source and process produced these bytes?
3. **Authorization:** was this origin allowed to cause this specific operation on this specific destination?
4. **Behavior:** what will the bytes do when executed?

A valid answer to one does not automatically answer the others. npm explicitly states that provenance is not a guarantee that code is non-malicious. [npm provenance limitations](https://docs.npmjs.com/generating-provenance-statements/#provenance-limitations).

SLSA likewise distinguishes source integrity from build integrity, and its verification guidance requires checking expected builders, sources, parameters, signatures, and artifact digests—not merely the existence of an attestation. It also states limits on its threat coverage. [SLSA threat model](https://slsa.dev/spec/v1.2/threats-overview), [artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts).

My working shorthand is **trace the handoff, not just the badge**. This is a practical organizing principle, not a new security theory.

## What changed recently—and what has not automatically changed

Historical attacks must not be presented as descriptions of every current platform configuration.

- **May 22:** npm staged publishing became generally available. A workflow can be limited to uploading a staged release; a maintainer then approves it with 2FA. Availability is not evidence a particular project enabled stage-only publishing. [Announcement](https://github.blog/changelog/2026-05-22-staged-publishing-and-new-install-time-controls-for-npm/).
- **July 8:** npm 12 shipped with dependency lifecycle scripts blocked unless allowed by the root package policy, and Git/remote-URL dependencies disallowed by default. This is not a claim that all scripts are disabled or that older clients inherit these defaults. [Actual npm 12 release](https://github.com/npm/cli/releases/tag/v12.0.0).
- **September 10:** GitHub announced generally available, service-enforced `cache-mode` controls. Low-trust events have read-only defaults; explicit write settings can override them. Cache access is a distinct control, not synonymous with repository-content permissions. [Cache access announcement](https://github.blog/changelog/2026-09-10-control-github-actions-cache-access-with-cache-mode/).
- **September 17:** workflow execution protections became generally available. The new default restriction on `pull_request_target` for specified public repositories initially runs in evaluation mode; automatic enforcement is announced for **November 2**, not already universal on the date of this investigation. [Execution-protection announcement](https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/).

Current npm documentation also says adding trusted publishing does not itself remove traditional token-based publication. Those paths must be considered separately. [Trusted publishing documentation](https://docs.npmjs.com/trusted-publishers/).

This freshness check changed the investigation: a recommendation to “add cache permissions someday” would miss a control already shipped, while assuming the new workflow default is already enforced would overstate protection.

## A small experiment: two kinds of failure, not one

I built a deterministic, offline influence-graph model. It distinguishes an attacker's ability to influence **publishing authority** from the ability to influence **published bytes**. A legitimate publisher can distribute bad bytes without giving their author direct control of its credential.

| Assumed toy configuration | Influence can reach publishing authority | Influence can reach published bytes |
|---|---:|---:|
| Shared cache feeds a privileged release job | Yes | Yes |
| Only credential lifetime is shortened | Yes | Yes |
| Fresh runner restores the same shared cache | Yes | Yes |
| Install hooks disabled, compromised build tool still executed | Yes | Yes |
| Isolated publisher does not execute artifact code, but accepts its bytes | No | Yes |
| The sole modeled PR-to-cache path is removed | No | No |
| Cache path removed, different unreviewed dependency still executes | Yes | Yes |
| Publisher isolated and an effective artifact gate rejects influenced bytes | No | No |

All eight declared scenarios and four algorithm controls passed. A separate reviewer recomputed all sixteen scenario/target reachability results and shortest path lengths with a different algorithm and checked the saved source hash.

**What this does not show:** an exploit, a probability of compromise, a real repository vulnerability, or a working malware detector. The graph edges are assumptions. The last row assumes an effective gate; it does not demonstrate how to build one. “No path” means no path in that small graph, not “secure.”

The useful counterexample is the isolated publisher: **protecting credentials and protecting artifact integrity are distinct requirements**. A signature made by an uncompromised publisher does not repair malicious content that it was authorized to publish.

Files: [offline model](./trust_boundary_lab.py), [results and source hash](./trust_boundary_lab_results.json). The model has no network access, shell execution, credential reads, or third-party dependencies.

## The research direction this earns

A useful next project would be a **handoff review benchmark** for build automation: can an analyst or tool track origin, permitted destination, executable content, and authorization through multiple jobs?

This is not an untouched field. GitHub Security Lab has documented workflow/artifact boundary failures for years, and zizmor already provides audits for cache poisoning, dangerous triggers, permissions, and other workflow patterns. A new tool would need a demonstrated gap and comparison against these baselines—not a renamed implementation of them. [GitHub Security Lab's workflow guidance](https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/), [zizmor audit rules](https://docs.zizmor.sh/audits/).

The bounded next test would use local synthetic fixtures and already-fixed public examples:

1. Freeze vulnerable/fixed pairs and the exact platform assumptions, including the date-dependent cache defaults.
2. Keep bytes, metadata, execution, and authority as separate edge types; a well-formed string is not an authorization decision.
3. Compare existing checks with a cross-job review on held-out examples, including harmless workflows. Count false alarms and unresolved cases, not just detections.
4. Test whether the proposed explanation identifies the decisive boundary and whether the fixed version removes that path without breaking legitimate behavior.
5. Stop claiming improvement if existing tools already explain the cases equally well. Unknown action internals must remain unknown, not silently “safe.”

The wider curiosity lead is persistent state: caches, generated files, notebooks, and stored agent memory can carry low-trust input into a later, higher-authority context. That analogy motivates investigation; it does not establish that all these systems share an exploit or require the same defense.

## Bottom line

This pass produced a sourced case file, a current-controls check, and an independently reviewed offline model. It did **not** discover a zero-day, certify a system, or contact affected maintainers. The strongest next question is precise: **where does data from one trust level become an instruction or authorized decision at another?**
