# R223T sandbox preview spec

stage_id: 1013R_R223T_FIXTURE_ONLY_SANDBOX_PREVIEW  
status: fixture_only_static_preview  
source: R223S_OPT_IN_SANDBOX_ROUTE_SPEC

## Preview purpose

R223T creates a standalone static preview so reviewers can inspect how v0.2 candidate would appear in an opt-in sandbox. It does not implement a formal route.

## Preview contents

The preview contains:

- safety banner
- sample selector
- v0.1 / v0.2 candidate comparison
- teacher default draft preview
- review ledger summary preview
- unit_phase_role / practice_intensity explanation
- component trigger status as review-only metadata
- screen / learning sheet / evidence mapping as review-only metadata

## Non-goals

R223T does not:

- modify R97B
- add a formal route
- modify frontend/backend
- connect runtime/model/prompt/db
- write back lesson body
- publish v0.2
- execute classroom components
- formal apply

## Required safety banner

```text
Preview only. v0.2 candidate is not published. No lesson body writeback.
```

## Current decision

```text
PASS_CONTINUE_TO_R223U_SANDBOX_TEACHER_REVIEW
```

