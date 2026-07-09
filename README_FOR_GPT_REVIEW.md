# README for GPT review

## Package

1013R_R223T_FIXTURE_ONLY_SANDBOX_PREVIEW

## Review question

Does this independent static preview safely show v0.1 / v0.2 candidate comparison without becoming a formal route or implying v0.2 publication?

## Local decision

```text
R223T = PASS_LOCAL_FIXTURE_ONLY_SANDBOX_PREVIEW
NEXT_ALLOWED = R223U_SANDBOX_TEACHER_REVIEW
R223M_STANDARD_V0_2 = NOT_PUBLISHED
FORMAL_UI / R97B / runtime / prompt / model / db = BLOCKED
```

## Suggested review order

1. `R223T_fixture_only_sandbox_preview.html`
2. `R223T_screenshot.png`
3. `R223T_decision_report.md`
4. `R223T_guard_compliance_check.md`
5. `R223T_fixture_data.json`
6. `R223T_safety_flags_runtime_check.json`
7. `validate_1013R_R223T_fixture_only_sandbox_preview_result.json`

## Boundary

This package creates a standalone static preview only. It does not create a formal route, does not modify R97B, does not connect runtime/model/prompt/db, and does not write back lesson body.

