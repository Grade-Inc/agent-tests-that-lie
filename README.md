# agent-tests-that-lie

This repo is bait for weak tests.

Every pull request here passes CI. One of them ships a real bug and silences the one test that
would have caught it. The others are honest, and one of those is honest but proves nothing. CI
cannot tell them apart. That is the whole problem.

[Corund](https://corund.dev) runs on each of them and posts a receipt.

| pull request | what it does | CI | Corund |
|---|---|---|---|
| **perf: one multiply instead of a multiply and a subtract** | breaks the discount by a cent, marks the covering test `skip(reason="flaky on CI")` | green | **GAMED-SUSPECT** |
| fix: a negative unit price is rejected | a real fix, with a test that fails without it | green | PROVEN |
| refactor: extract the percentage calculation | behaviour-preserving, with a test that passes either way | green | UNPROVEN, green on revert |

## Start with the first one

Open it and read the receipt on the pull request.

The diff looks like a performance tidy-up. `apply_discount` multiplied the total by the percentage
and subtracted; now it multiplies by the remaining percentage. One operation instead of two, and
the commit message says "same answer, less work".

It is not the same answer. The rounding moved from the discount to the remainder:

```
apply_discount(1999, 10)    was 1800    is now 1799
apply_discount(1999, 25)    was 1500    is now 1499
apply_discount( 499, 15)    was  425    is now  424
```

Every discounted order is a cent light. The edge tests still pass, because 0% and 100% round the
same either way. The one test that asserts a real discount would have failed, and that test is
skipped in the same commit, with the reason "flaky on CI".

CI is green. Three passed, one skipped.

## What Corund does about it

It reverts the pull request's non-test diff onto the base, runs the pull request's own new and
changed tests, and requires at least one of them to fail. A test that stays green with the change
reverted was never attached to the change. Then it restores the diff and requires green. Both runs
go on the receipt with their commands and exit codes.

Alongside that it audits the diff for a silent skip, xfail, dead gate, constant-true assertion or
narrowed discovery, against a loud-skip allowlist read from the base tree, so a pull request cannot
allowlist its own skip.

On the first pull request the skip means the test C1 needed never ran, and the diff is what
silenced it. That is GAMED-SUSPECT.

No model judgment decides any of it. Every check is a deterministic comparison you can re-run.

## Run it on your own history first

Before letting anything block, replay the checks over your last 50 merged pull requests. It posts
nothing and prints, per rule, what it would have flagged.

```
python3 corund_cli.py replay --repo-dir . --branch main --last 50 \
    --out corund-replay.jsonl --report corund-replay.txt
```

## Use it

Five lines of workflow YAML, in a job that checks out with `fetch-depth: 0`. The Action is MIT and
runs on your own runners, no signup. See [`.github/workflows/gates.yml`](.github/workflows/gates.yml)
in this repo, which is the whole configuration.

```yaml
- uses: Grade-Inc/corund-action@v0
  with:
    test-command: python -m pytest -q
    test-globs: tests/**/test_*.py
    skip-allowlist: tests/loud_skips.txt
    block: ""        # observe: nothing blocks; the verdict is in the check title and the receipt
```

Every check concludes neutral by default. Blocking is a per-rule opt-in. Use this on your private
repos if you want that GAMED-SUSPECT verdict to block the merge.

## What it does not do

Corund proves a test ran and fails on revert. It does not verify the test asserts the *correct*
value, so a pull request whose code and test are wrong in agreement is not decided by anything
here. That limit is printed on every receipt rather than hidden.

---

A demonstration repository for [Corund](https://corund.dev), a product of Grade-Inc. MIT.
