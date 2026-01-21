## Preview Access
- Serve the website at http://127.0.0.1:8000/ (Home), /players, /drills, /plans/{player_id}. The current FastAPI+Jinja app will host all pages.

## Design System Setup
- Create CSS variables for color tokens (light/dark), spacing scale, radii (12–16px), shadows, and motion durations.
- Establish a small utility CSS layer for grid, flex, typography, tags, cards, and progress bars.
- Add a theme toggle (light/dark) with prefers-color-scheme default.

## Color Palette Tokens
- Light mode variables:
  - --color-bg: #F7F9FC, --color-surface: #FFFFFF, --color-text: #1F2933
  - --color-primary: #0B1C2D, --color-accent-green: #2DFF7A, --color-accent-cyan: #4FD1C5
- Dark mode variables:
  - --color-bg: #0A0F14, --color-surface: #121A23, --color-text: #E6EDF3, --color-text-secondary: #9AA4AF
  - --color-accent-green: #2DFF7A, --color-accent-cyan: #4FD1C5
- Apply tokens to buttons, links, cards, progress bars, tags.

## Typography
- Fonts and roles:
  - Satoshi (headings, metrics titles) or General Sans if licensing blocks Satoshi
  - JetBrains Mono (metrics, KPIs, drill parameters, tables)
  - Inter (long descriptions, coach notes, AI explanations)
- Implement font stacks with local hosting (variable fonts), define sizes:
  - H1 36–40 Bold, H2 28–32 Semibold, H3 20–24 Medium
  - Body 15–16 Regular, Secondary 14 Regular
  - Data Mono 16–18 Medium, Small stats 13–14 Regular
- Letter spacing rules: tight for headings, wide for buttons, normal for data.

## Core Components
- Cards: rounded 12–16px, navy headers, white/dark-surface bodies; compact info density.
- Progress Bars: green→cyan gradient, WCAG AA contrast, animate on load.
- Tags: position, intensity, AI suggested (cyan outline badge).
- Tooltips: subtle shadow, cyan accent line; explain “Why this drill?” in 1 sentence.
- Modals: confirmations when AI proposes changes; primary button styling in deep navy.
- KPI tiles: big numbers, small trend arrows; avoid heavy charts on top.

## Layouts
- Coach Dashboard (Home): 3-column grid (desktop), stacked on mobile; quick actions (Generate Session, Adjust Intensity), 1–2 AI insight cards.
- Player Profile: left summary card, center plan & drills, right AI insights + progression forecast; include radar chart placeholder and timeline of drill history.
- Training Plan Builder: card-based drills, drag & drop ordering (MVP placeholder with up/down controls), intensity represented by dots/labels (Light/Moderate/Intense).

## Microinteractions & Motion
- Progress bars: ease-out 400ms on load.
- Drill completion: subtle pulse.
- AI recommendations: fade-in; hover states use brightness change not color swaps.
- Motion communicates state only; no gamification effects.

## AI UX Best Practices
- Copy style: friendly, explanatory, non-robotic; 1-sentence rationale.
- Badging: subtle AI cyan outline; never auto-change plans without confirmation.
- Overrides: coaches can adjust everything; confirmation modals on commit.

## Accessibility
- Maintain ≥ WCAG AA contrast across themes; ensure icons + labels together.
- Green never sole indicator; pair with labels/icons.
- Large tap targets for tablet; semantic HTML landmarks; keyboard focus ring visible.

## Implementation Approach (Phased)
- Phase A (current SSR):
  - Integrate the design system into existing Jinja templates and static CSS.
  - Upgrade templates: index (dashboard tiles), players (cards + creation form), plan (progress bars, tags, AI tooltip), add basic builder controls.
  - Add theme toggle and local font loading.
- Phase B (optional React+Tailwind top-tier):
  - Scaffold a Vite React frontend using Tailwind, Framer Motion for microinteractions, and shadcn/ui for components.
  - Use the existing Python app only as an API for data; migrate templates gradually.
  - Recharts for visualizations (radar, trends); keep SSR pages until parity.

## Deliverables
- Design tokens CSS, updated templates, components (cards, progress, tags, tooltips, modals), theme toggle, improved pages (Dashboard, Player Profile, Plan Builder), accessible styles.

## Verification
- Manual checks for contrast and keyboard navigation.
- Snapshot screenshots in both themes.
- Lighthouse run for performance/semantics.
- Unit tests for template rendering and minimal client-side interactions.
