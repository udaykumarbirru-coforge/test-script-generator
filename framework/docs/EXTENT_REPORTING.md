# Centralized Extent Reporting

## Architecture

Reporting is implemented as framework infrastructure. Generated tests and Page Object business methods do not initialize reports, write report logs, call screenshots, or flush reports.

Execution flow:

`pytest / Execution Agent -> execution_hooks -> ExecutionAgentReportingBridge -> ExtentReportManager`

Action flow:

`generated test -> page/business method -> PlaywrightActions -> centralized reporter -> screenshot + step evidence`

Direct generated `page.goto(...)` navigation is transparently intercepted by `DriverManager`, so existing generated tests do not need to change.

> Note: AventStack's official ExtentReports implementations are Java/.NET. This Python framework therefore provides a native Extent-style HTML reporting implementation with centralized lifecycle, test/step logging, media attachments, environment metadata, statistics, and failure analysis. It does not introduce a Java/.NET runtime dependency into the Python framework.

## Files

- `framework/reporting/extent_reporter.py` - execution/test/step report model, screenshot capture, HTML/JSON output, failure evidence.
- `framework/reporting/context.py` - execution-scoped reporter context and recursion protection.
- `framework/reporting/models.py` - test and step data contracts.
- `framework/core/execution_agent.py` - execution folder creation, reporter initialization and final flush.
- `framework/core/execution_hooks.py` - pytest lifecycle integration and automatic test failure capture.
- `framework/core/driver_manager.py` - transparent capture of direct page navigation.
- `framework/core/actions.py` - centralized framework action interception. No page object reporting code is required.
- `framework/config/reporting.json` - reporting policy.

## Default output

Each run creates:

```text
reports/executions/<execution-id>/
├── extent-report.html
├── execution-report.json
├── execution-result.json
└── screenshots/
    └── <test-name>/
        ├── 0001_<action>_pass.png
        ├── 0002_<action>_pass.png
        └── ...
```

`execution-result.json` publishes the final report path, JSON evidence path, screenshot directory, status, and execution statistics for an Execution Agent or CI wrapper.

## Captured step fields

Each framework action records timestamp, normalized action name, logical locator name when inferable, locator description, sanitized input value, expected result, actual result, PASS/FAIL/WARNING status, duration, screenshot path, metadata, and—on failure—exception type/message, stack trace, and root cause.

Runtime-healed actions are reported as `WARNING` and retain both the original and healed locator evidence in metadata.

## Screenshot policy

By default, screenshots are captured after successful framework steps and immediately on failed steps. Test-level failures outside an action also receive a failure screenshot through the pytest execution hook.

## Sensitive test data

Sensitive inputs are masked automatically when a locator/logical name indicates passwords, secrets, tokens, CVV/CVC, card data, or similar fields. Common payment-card values are also masked by shape. This preserves evidence while avoiding clear-text credentials in the report.

## Configuration

Edit `framework/config/reporting.json` or use environment variables:

- `M2A_REPORTING_ENABLED=false` disables centralized reporting.
- `M2A_REPORT_ROOT=<path>` changes the report root.
- `M2A_EXECUTION_ID=<id>` lets an external Execution Agent supply its execution identifier.

The JSON configuration controls pass/fail screenshots, full-page screenshots, sensitive-input masking, and report root.

## Script generation contract

Generated tests must remain limited to test flow, business/page method calls, assertions, and test-data references. Do not generate Extent/report imports, screenshot calls, logging calls, report lifecycle code, or report steps. The current generated test in this package was intentionally left unchanged.
