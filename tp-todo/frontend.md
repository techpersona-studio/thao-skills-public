# Frontend Domain Sections

Insert these sections after **Success Criteria** and before **Risk Assessment** for frontend or fullstack tasks.

---

## Visual Specification

_Describe the UI change in concrete terms. Include sketches, Figma links, or before/after screenshots when available._

- **Layout**: _Where does this component live? What's its relationship to surrounding elements?_
- **States**: _Default, hover, active, disabled, loading, error — which apply?_
- **Responsive behavior**: _Mobile, tablet, desktop breakpoints — what changes?_
- **Interactions**: _Click, keyboard nav, drag-drop — what actions trigger what?_
- **Animations**: _Transitions, loading spinners, slide-ins — what moves and when?_

---

## Component Map

_List components touched or created, with their responsibility in one sentence._

| Component | Path | Responsibility |
|-----------|------|----------------|
| _ComponentName_ | `frontend2/src/...` | _One-sentence job description_ |

---

## Style & Theme Checklist

_Verify alignment with the design system. Check against `.cursor/rules/frontend-styling.mdc` for authoritative rules._

- [ ] Uses CSS Modules (`.module.css`) for component-specific styles
- [ ] Uses Ant Design theme tokens (`@primary-color`, `@text-color`, etc.) — no hardcoded colors
- [ ] Respects spacing scale (`@padding-xs`, `@padding-sm`, etc.)
- [ ] Typography uses theme vars (`@font-size-base`, `@font-family`)
- [ ] Dark mode compatible (if applicable)
- [ ] No inline styles except for dynamic values (e.g., `style={{width: computedWidth}}`)

---

## Accessibility Checklist

- [ ] Keyboard navigable (tab order logical, no keyboard traps)
- [ ] Screen reader friendly (ARIA labels, roles, live regions where needed)
- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for UI components)
- [ ] Focus indicators visible
- [ ] Error messages announced to screen readers
- [ ] Interactive elements have sufficient hit targets (44x44px minimum)

---

## Visual Verification Plan

_Manual steps to verify the UI works as designed. Run these after the final UI-facing step, before the docs step._

1. **Load the page**: _URL or nav path_
2. **Verify default state**: _What should be visible?_
3. **Trigger interactions**: _Click X, type Y, hover Z — what changes?_
4. **Test edge cases**: _Empty state, error state, loading state, overflow content_
5. **Check responsive**: _Resize to mobile (375px), tablet (768px), desktop (1440px)_
6. **Keyboard nav**: _Tab through, trigger with Enter/Space, ESC to close_
7. **Screen reader**: _VoiceOver on Mac, NVDA on Windows — does it make sense?_

---

## Test Selectors

_Data attributes or test IDs for E2E/integration tests. Use `data-testid` for Playwright/Cypress._

| Element | Selector | Purpose |
|---------|----------|---------|
| _Button_ | `[data-testid="submit-button"]` | _Trigger form submission_ |

---

## Section-specific tips (Frontend)

- **Visual Specification**: If there's no Figma, sketch it in ASCII or describe it like you're on a phone call with a designer who can't see your screen.
- **Component Map**: Include both new and modified components. If you're touching a shared component (e.g., `Button`, `Dropdown`), flag it — changes affect every consumer.
- **Style & Theme Checklist**: If you're adding a new color, spacing value, or font size, it probably belongs in the theme config, not hardcoded. Check with the user first.
- **Accessibility Checklist**: Don't check a box just because you added an `aria-label`. Test with an actual screen reader. If you can't, say so in the Risk Assessment.
- **Visual Verification Plan**: Write steps a QA person can follow without reading the code. Include the exact URL or nav path.
- **Test Selectors**: Define selectors **before** writing tests. Changing selectors later breaks tests.
