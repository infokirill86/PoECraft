# Diagnostics and Failure Reporting

## Required diagnostic fields

M34-A breach diagnostics include:

- fixture id;
- seed;
- run id;
- sample tier;
- branch key;
- pool digest;
- scaled deviation;
- scaled tolerance;
- diagnostic category.

## Negative-control proof

M34-A includes an explicitly marked negative-control test:

- `test_m34a_negative_control_proves_breach_reporting_can_fail`

The negative-control creates an intentionally invalid observed-count distribution and asserts that the breach path raises a hard failure.

It also checks that the failure message includes the required diagnostic fields.

## Why this matters

Without a negative-control, a convergence test can look serious while never proving that it would fail on bad behavior.

The negative-control is not a gameplay claim and is not a new mechanic. It is a test of the test harness.
