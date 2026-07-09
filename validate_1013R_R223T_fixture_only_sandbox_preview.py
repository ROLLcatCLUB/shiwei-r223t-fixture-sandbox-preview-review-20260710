import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "R223T_fixture_only_sandbox_preview.html",
    "R223T_fixture_data.json",
    "R223T_sandbox_preview_spec.md",
    "R223T_v0_1_vs_v0_2_comparison_view.md",
    "R223T_review_ledger_summary_policy.md",
    "R223T_safety_flags_runtime_check.json",
    "R223T_screenshot.png",
    "R223T_screenshot_smoke_result.md",
    "R223T_guard_compliance_check.md",
    "R223T_decision_report.md",
    "README_FOR_GPT_REVIEW.md",
    "PACKAGE_MANIFEST.json",
]

FALSE_KEYS = [
    "schema_v0_2_published",
    "teacher_confirmed",
    "formal_apply_allowed",
    "lesson_body_writeback",
    "r97b_modified",
    "formal_route_added",
    "frontend_backend_modified",
    "runtime_connected",
    "provider_model_connected",
    "prompt_modified",
    "database_written",
    "existing_teacher_drafts_modified",
    "r222d_component_library_modified",
    "formal_apply",
]

TRUE_KEYS = [
    "fixture_only",
    "non_persistent_preview",
]

REQUIRED_DECISIONS = [
    "PASS_CONTINUE_TO_R223U_SANDBOX_TEACHER_REVIEW",
    "HOLD_FOR_SANDBOX_PREVIEW_REDUCTION",
    "HOLD_FORMAL_V0_2_NOT_READY",
]

REQUIRED_HTML_PHRASES = [
    "Preview only. v0.2 candidate is not published. No lesson body writeback.",
    "fixture_only=true",
    "non_persistent_preview=true",
    "teacher_confirmed=false",
    "formal_apply_allowed=false",
    "Review-only metadata. Not executable. Not written back.",
    "v0.1 baseline",
    "v0.2 candidate delta",
    "Review-only ledger",
]

BANNED_CONTROL_PHRASES = [
    "Run model",
    "Apply to R97B",
    "Save to lesson body",
    "Publish v0.2",
    "Execute component",
    "Use this draft",
    "正式发布 v0.2",
    "写回教案正文",
    "运行模型",
    "应用到 R97B",
]

TEACHER_DRAFT_BANNED_FIELDS = [
    "practice_pattern_type",
    "demonstration_type",
    "micro_practice_type",
    "appreciation_scaffold_type",
    "component_trigger",
    "screen_trigger",
    "learning_sheet_fields",
    "evidence_outputs",
    "new_surface_candidate",
    "unregistered_do_not_execute",
]

def read_text(name):
    return (ROOT / name).read_text(encoding="utf-8")

def main():
    failures = []
    checks = 0

    for name in REQUIRED_FILES:
        checks += 1
        if not (ROOT / name).exists():
            failures.append(f"missing required file: {name}")

    html = read_text("R223T_fixture_only_sandbox_preview.html") if (ROOT / "R223T_fixture_only_sandbox_preview.html").exists() else ""
    combined = "\n".join(
        read_text(name)
        for name in REQUIRED_FILES
        if (ROOT / name).exists() and name.endswith((".md", ".json", ".html"))
    )

    for phrase in REQUIRED_HTML_PHRASES:
        checks += 1
        if phrase not in html:
            failures.append(f"missing html phrase: {phrase}")

    for phrase in BANNED_CONTROL_PHRASES:
        checks += 1
        if phrase in html:
            failures.append(f"forbidden control phrase present: {phrase}")

    fixture_path = ROOT / "R223T_fixture_data.json"
    if fixture_path.exists():
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        samples = fixture.get("samples", [])
        checks += 1
        if len(samples) != 3:
            failures.append("fixture must contain 3 samples")
        for sample in samples:
            checks += 1
            if not sample.get("teacher_default_draft"):
                failures.append(f"missing teacher_default_draft: {sample.get('sample_id')}")
            draft = sample.get("teacher_default_draft", "")
            for field in TEACHER_DRAFT_BANNED_FIELDS:
                checks += 1
                if field in draft:
                    failures.append(f"teacher draft leaks backend field {field}: {sample.get('sample_id')}")
            summary = sample.get("review_ledger_summary", {})
            checks += 1
            if summary.get("event_count", 0) < 4:
                failures.append(f"event_count too low: {sample.get('sample_id')}")
            checks += 1
            if not summary.get("component_statuses"):
                failures.append(f"missing component statuses: {sample.get('sample_id')}")

    safety_path = ROOT / "R223T_safety_flags_runtime_check.json"
    if safety_path.exists():
        safety = json.loads(safety_path.read_text(encoding="utf-8"))
        for key in FALSE_KEYS:
            checks += 1
            if safety.get(key) is not False:
                failures.append(f"safety flag must be false: {key}")
        for key in TRUE_KEYS:
            checks += 1
            if safety.get(key) is not True:
                failures.append(f"safety flag must be true: {key}")
        controls = safety.get("page_controls", {})
        for key in ["publish", "save", "apply", "run_model", "writeback", "execute_component"]:
            checks += 1
            if controls.get(key) is not False:
                failures.append(f"page control must be false: {key}")

    for decision in REQUIRED_DECISIONS:
        checks += 1
        if decision not in combined:
            failures.append(f"missing decision output: {decision}")

    screenshot = ROOT / "R223T_screenshot.png"
    checks += 1
    if not screenshot.exists() or screenshot.stat().st_size < 10000:
        failures.append("screenshot missing or too small")

    result = {
        "passed": not failures,
        "check_count": checks,
        "failed": len(failures),
        "failures": failures,
        "decision": "PASS_CONTINUE_TO_R223U_SANDBOX_TEACHER_REVIEW",
    }
    (ROOT / "validate_1013R_R223T_fixture_only_sandbox_preview_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if not failures else 1)

if __name__ == "__main__":
    main()

