# Upstream review — September 21, 2026

## Applicability

An unauthenticated read of [the main commit API](https://api.github.com/repos/actions/attest/commits/main) returned `c5895f04a64254068ee4ce85086baae80a363b9c`, the exact tested revision. Commit date: September 17, 18:00:26 UTC. This is a point-in-time check; recheck before submission. No additional build is needed merely to establish that this identical revision remains the default-branch head.

## Prior-report search

GitHub public issue/PR search, without restricting to open items:

| Query | Results | Assessment |
|---|---|---|
| `repo:actions/attest "untracked"` | One: PR 445 | Different artifact-location bug |
| `repo:actions/attest "184.index.js"` | One: PR 469 | Introduction of the chunk, not a stale-output report |
| `repo:actions/attest "ignore-space-at-eol"` | None | Limited negative search evidence |
| `repo:actions/attest "clean build"` | None | Limited negative search evidence |

[PR 445](https://github.com/actions/attest/pull/445) moved downloaded artifacts outside the checkout workspace so checkout cleanup would not remove them. That is different from comparing untracked compiler outputs.

[PR 469](https://github.com/actions/attest/pull/469) updated `@sigstore/oci`. Its [file listing](https://api.github.com/repos/actions/attest/pulls/469/files?per_page=100) records `dist/184.index.js` as added and `dist/index.js` as modified. The returned review comment concerns the dependency name in the PR title. This establishes historical introduction, not when the file ceased to be generated or whether it was ever exploitable.

These searches do not establish novelty and cannot exclude private, unindexed, or differently worded reports. No broad repository-history or advisory audit has been completed.

## Reporting route and scope

The repository's displayed [security policy](https://github.com/actions/attest/security/policy) directs security issues to GitHub's security bug bounty. The repository-root raw `SECURITY.md` URL returned 404, but the displayed policy is available; absence of that one file URL is not absence of a policy.

Our evidence currently supports build-verification correctness defects, not a demonstrated security vulnerability, malicious release, or privilege escalation. The draft should not assert bounty eligibility, assign a vulnerability severity, or accuse any maintainer or dependency of wrongdoing. If reporting as security-sensitive, use the published private route; otherwise an ordinary maintainer issue/PR is a possible route for a narrowly scoped correctness fix. External submission requires the user's choice and authorization; nothing has been sent.
