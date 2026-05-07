# Japan AI Guide UI Design System

JAG-R003 establishes the first shared UI rules for Japan AI Guide. The goal is to keep future pages, chat components, and AnswerCards visually consistent.

## Token Source

Primary token file:

```text
frontend/styles/tokens.css
```

The app imports this token file from:

```text
frontend/src/app/globals.css
```

Components should reference tokens through CSS variables or shared `.jag-*` classes rather than hard-coding new colors, radii, shadows, or spacing.

## Design Token List

### Colors

| Token | Purpose |
| --- | --- |
| `--jag-color-page` | Base page background |
| `--jag-color-page-soft` | Top radial background accent |
| `--jag-color-surface` | Main white surface |
| `--jag-color-surface-muted` | Soft panel background |
| `--jag-color-ink` | Primary text |
| `--jag-color-ink-soft` | Secondary strong text |
| `--jag-color-muted` | Muted body text |
| `--jag-color-line` | Borders and separators |
| `--jag-color-primary` | Primary action blue |
| `--jag-color-primary-strong` | Hover/strong blue |
| `--jag-color-primary-soft` | Badge and soft action fill |
| `--jag-color-audio` | Dark audio module surface |

### Typography

| Token | Purpose |
| --- | --- |
| `--jag-font-sans` | Product sans-serif stack |
| `--jag-font-size-xs` | Labels and metadata |
| `--jag-font-size-sm` | Small controls |
| `--jag-font-size-md` | Body and input text |
| `--jag-font-size-lg` | Larger body emphasis |
| `--jag-font-size-xl` | Card headings |
| `--jag-font-size-hero` | Hero headline |

### Radius

| Token | Purpose |
| --- | --- |
| `--jag-radius-sm` | Compact buttons and small controls |
| `--jag-radius-md` | Panels and modules |
| `--jag-radius-lg` | AnswerCard and input shell |
| `--jag-radius-pill` | Pills, badges, quick actions |

### Shadows

| Token | Purpose |
| --- | --- |
| `--jag-shadow-sm` | Small cards and buttons |
| `--jag-shadow-md` | Logo and medium elevated surfaces |
| `--jag-shadow-lg` | AnswerCard and input shell |
| `--jag-shadow-primary` | Primary user message and primary CTA |

### Spacing

| Token | Purpose |
| --- | --- |
| `--jag-space-1` to `--jag-space-10` | Shared spacing scale for future CSS and component-level layout |

## Shared Component Classes

Defined in `frontend/src/app/globals.css`:

| Class | Use |
| --- | --- |
| `.jag-page` | Full app background and base page shell |
| `.jag-sidebar` | Desktop history sidebar |
| `.jag-card` | Main elevated card surface |
| `.jag-panel` | Subsection panels inside cards |
| `.jag-button-primary` | Main action buttons |
| `.jag-button-secondary` | Secondary and quick buttons |
| `.jag-button-compact` | Mobile menu and compact controls |
| `.jag-input-shell` | Bottom chat input container |
| `.jag-answer-badge` | AnswerCard status badge |

## Component Style Rules

- Buttons must use `.jag-button-primary`, `.jag-button-secondary`, or `.jag-button-compact`.
- AnswerCard outer containers must use `.jag-card`.
- Inner AnswerCard sections must use `.jag-panel`.
- Sidebar shells must use `.jag-sidebar`.
- Input dock containers must use `.jag-input-shell`.
- Badges inside AnswerCard must use `.jag-answer-badge`.
- Use Chinese-first labels for the operator/traveler UI unless the control is a language selector.
- Avoid introducing new one-off shadows, border colors, or radius values unless the token file is updated first.
- Mobile components must preserve `min-w-0`, wrapping, and overflow controls so long Chinese/Japanese text does not break layout.

## Before / After

Before JAG-R003:

- Components directly embedded many Tailwind color, radius, shadow, and border choices.
- Several components had duplicated button/card styling.
- Some UI text had encoding damage.

After JAG-R003:

- Tokens live in `frontend/styles/tokens.css`.
- Shared `.jag-*` classes define the first reusable visual system.
- ChatShell, Sidebar, AnswerCard, quick buttons, language selector, and input shell reference the design system.
- Visible UI text is restored to readable Chinese-first labels.

## Mock Boundary

This round changes visual consistency only. It does not add backend calls, AI logic, map logic, TTS, persistence, auth, or routing changes.
