# Reference: schema, output modes, platform defaults

Detailed material for `building-automation-prompts`. Read when you need the example schema, the output-mode templates, or platform-specific defaults.

## Example JSON schema

Adapt to the workflow. Reasoning fields (`summary`) come before decision fields so the model reasons before committing. No hidden chain-of-thought fields.

```json
{
  "summary": "short reasoning about the input",
  "decision": "qualified | not_qualified | needs_review",
  "confidence": 0.0,
  "recommended_action": "next action",
  "needs_human_review": true,
  "review_reason": "reason or empty string",
  "missing_fields": [],
  "tags": []
}
```

## Output modes

### Incomplete context

Return only the next blocking questions. Nothing else.

### Automation prompt

```
## Automation Prompt
[copy-ready prompt]

## Input Variables
[variables expected]

## Output Schema
[exact JSON or format]

## Failure Handling
[uncertainty/error behavior]
```

### Tool-calling agent spec

```
## Agent Prompt
[copy-ready prompt using the standard section order]

## Tools Needed
[tool name, purpose, when to use]

## Input Contract
[fields or payload]

## Output Contract
[exact schema]

## Review Rules
[when to escalate]
```

### Critique

```
## Keep
[what is useful]

## Remove
[what is unnecessary]

## Fix
[highest-impact changes]

## Revised Prompt
[lean version]
```

## Platform defaults

- **n8n**: strict JSON, branch-friendly booleans, fields that map cleanly into IF/Switch nodes.
- **Trigger.dev**: schema-enforced typed input/output (zod), idempotency, retry/error states. Typed contract means schema-enforced output, not prose-enforced.
- **Zapier/Make**: simpler schemas, fewer branches, defensive missing-field handling.
- **CRM workflows**: audit fields such as summary, action, score, tags, and review reason.
