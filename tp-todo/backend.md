# Backend Domain Sections

Insert these sections after **Success Criteria** and before **Risk Assessment** for backend or fullstack tasks.

---

## Wire Compatibility

_For API changes only. Skip if the change is internal (DB, tools, agent logic)._

**Endpoint(s) affected**: _`POST /api/v1/...`, `GET /api/v1/...`_

**Breaking changes**:
- [ ] Request schema changed (field added/removed/renamed)
- [ ] Response schema changed (field added/removed/renamed)
- [ ] Status code behavior changed
- [ ] Error format changed

**Migration strategy**:
- _If breaking: version bump, deprecation timeline, client rollout plan._
- _If non-breaking: additive changes only, defaults for new fields._

**Frontend coordination**:
- _Does frontend need to change? Who's handling it? Which PR?_

---

## Section-specific tips (Backend)

- **Wire Compatibility**: If you're unsure whether a change is breaking, it probably is. Ask the user. Breaking changes need a migration path — don't surprise frontend devs.
- **Implementation Steps**: For DB migrations, always include a "verify migration in dev" step before "run in prod". For tool changes, include a "test tool in isolation" step before "wire into agent".
- **Success Criteria**: Backend tests should cover happy path, error path, and edge cases. Name the test files and test functions. "All tests pass" is not enough.
- **Risk Assessment**: Call out deployment risks. If this change requires a DB migration, a service restart, or a feature flag flip, say so. If the change touches a high-traffic endpoint, flag it.
