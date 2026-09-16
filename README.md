# agent-tests-that-lie

This repo is bait for weak tests.

Four pull requests. All four pass CI. One ships a real bug and silences the one test that covers
it. One is a real fix. One is a refactor whose test would pass with or without it. One changes no
behaviour at all. CI reports the same thing for all four: green.

[Corund](https://corund.dev) runs red-on-revert on each of them and posts a receipt.

## Red-on-revert

Corund reverts the pull request's non-test diff onto the base, runs the pull request's own new and
changed tests, and requires at least one of them to execute and **fail by assertion** on that
reverted tree. Then it restores the diff and requires green. Both runs go on the receipt, with
their commands and exit codes.

A test that stays green with the change reverted was never attached to the change.

Corund never accuses. Where it cannot prove, it withholds and names the reason.

| pull request | what it does | CI | Corund |
|---|---|---|---|
| [#1 fix: a negative unit price is rejected](../../pull/1) | a real fix, with a test that fails without it | green | **PROVEN** |
| [#2 refactor: extract the percentage calculation](../../pull/2) | behaviour-preserving; the test passes either way | green | **UNPROVEN-green-on-revert** |
| [#3 perf: one multiply instead of a multiply and a subtract](../../pull/3) | breaks the discount by a cent, marks the covering test `skip(reason="flaky on CI")` | green | **UNPROVEN-collection** |
| [#4 refactor: name the discount amount before subtracting it](../../pull/4) | no behaviour change, no test change | green | **NOT-RUN** |

Four pull requests, four different things Corund can say. Exactly one of them is `PROVEN`.

## Start with #3

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
same either way. The one test that asserts a real discount would have failed — and that test is
skipped in the same commit, with the reason "flaky on CI".

CI is green. Three passed, one skipped.

Corund does not call this sabotage. It cannot see intent, so it does not guess at it. What it does
is refuse to call the pull request proven, and name the test that made proof impossible:

```
tests/test_cart.py::test_apply_discount_takes_the_percentage_off_the_whole_total:
    skipped WITH the change — never executed, not a witness

UNPROVEN-collection: no test failed by assertion on the reverted tree;
1 test(s) carry this reason:
    tests/test_cart.py::test_apply_discount_takes_the_percentage_off_the_whole_total
```

That is the receipt, verbatim. Green CI says the pull request is fine. The receipt says the only
test that could have judged it never ran. A reviewer reads one line and knows where to look.

## The other three

**#1 is the control.** A real fix with a test that genuinely fails without it. On the reverted tree
that test fails by assertion; with the change restored it passes. `PROVEN`, and the receipt names
the witness. Without this one you could not tell a working check from a check that is simply always
unhappy.

**#2 is the honest near-miss.** The refactor preserves behaviour, so its test passes on both trees.
That is not a bug and nobody did anything wrong — but the test proves nothing about this diff, and
the receipt says so: `UNPROVEN-green-on-revert`. This is the most common verdict on real
repositories, and it is a statement about the test, not an accusation about the author.

**#4 changes no tests at all**, so there is nothing to compare and Corund says `NOT-RUN` rather
than inventing a verdict. A check that reports a result it did not compute is the failure mode this
whole repository is about.

## Run it on your own history first

Before letting anything block, replay the check over your last 50 merged pull requests. It posts
nothing, and prints what it would have said.

```
python3 corund_cli.py replay --repo-dir . --branch main --last 50 \
    --out corund-replay.jsonl --report corund-replay.txt
```

## Use it

A few lines of workflow YAML, in a job that checks out with `fetch-depth: 0`. The Action is MIT and
runs on your own runners, no signup. See [`.github/workflows/gates.yml`](.github/workflows/gates.yml)
in this repo, which is the whole configuration.

```yaml
- uses: Grade-Inc/corund-action@v0.1.3
  with:
    runner: pytest
    test-command: python -m pytest -q
    test-globs: tests/**/test_*.py
    block: ""        # observe: nothing blocks; the verdict is in the check title and the receipt
```

Every check-run conclusion is neutral by default. Blocking is opt-in: set `block: c1` when you want
a failed check to stop the merge.

## What it does not do

Corund proves a test ran and fails on revert. It does not verify the test asserts the *correct*
value, so a pull request whose code and test are wrong in agreement is not decided by anything
here.

It checks that the tests a pull request adds or changes catch that pull request's change. It does
not flag a pull request that only turns off an existing test — on #3 above, the receipt names the
skipped test because that test was the one it needed, not because it audits skips.

Both limits are printed on every receipt rather than hidden.

---

A demonstration repository for [Corund](https://corund.dev), a product of Grade-Inc. MIT.
