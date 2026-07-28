# Yorushika Music Archive — Design System

## Page goal

Create a private, content-first Yorushika archive that feels like a quiet listening notebook rather than a generic streaming dashboard. The interface should help a visitor move naturally from a mood, to an album, to one song and its source-backed note.

## Layout structure

1. A compact, stable top navigation with a typographic site mark.
2. A concise editorial introduction instead of a marketing hero.
3. One primary content module per viewport:
   - Home: daily selection and listening paths.
   - Discography: album chronology and filters.
   - Song: cover, metadata, note, official source and adjacent tracks.
4. Supporting content appears below the primary module, never in a weak decorative sidebar.
5. Desktop content width is capped at 1180px; mobile uses 20px gutters.

## Information hierarchy

- Chinese is the primary explanatory language.
- Japanese titles remain the primary work identifiers.
- English appears only as lightweight supporting metadata.
- Official facts, personal notes and external source links are visually separated.
- A page has one `h1`; headings follow a sequential hierarchy.

## Visual language

- Direction: nocturnal editorial minimalism with restrained product structure.
- Light surfaces use warm paper tones rather than pure gray.
- Dark mode uses blue-black night tones, not simple color inversion.
- Primary accent: muted hydrangea blue.
- Secondary accent: restrained dusk rose.
- Corners are medium and consistent; borders do more work than shadows.
- Gradients are limited to atmospheric page backgrounds and small highlights.
- Existing cover art is the main visual material; no decorative stock imagery.

## Color tokens

- `--archive-paper`: warm page background.
- `--archive-surface`: primary card surface.
- `--archive-ink`: primary text.
- `--archive-muted`: secondary text.
- `--archive-line`: dividers and borders.
- `--archive-blue`: primary accent and focus.
- `--archive-rose`: secondary accent.
- `--archive-night`: dark theme base.

All body text pairs must meet WCAG AA contrast. Color is never the only state indicator.

## Typography

- Use the bundled Outfit family with Chinese system fallbacks.
- Display headings: strong but compact, maximum 56px on desktop.
- Body: minimum 16px, 1.65 line-height.
- Metadata: 12–14px with increased letter spacing.
- Long copy is capped at 68 characters per line.

## Components

- Navigation links: minimum 44px target, visible active state and focus ring.
- Editorial cards: 18–28px radius, quiet border, subtle lift only on pointer devices.
- Cover art: declared aspect ratio and dimensions to prevent layout shift.
- Metadata chips: semantic labels, not ranking or fake popularity indicators.
- Filter controls: visible labels and a clear reset path.
- Song links: internal detail pages first; official pages are explicit external actions.

## Interaction

- Motion lasts 160–260ms and uses opacity/transform only.
- Respect `prefers-reduced-motion`.
- Hover is supplementary; every action works with keyboard and touch.
- Mobile navigation stays under five primary destinations where possible.
- Route changes keep a predictable URL and browser back behavior.

## Responsive rules

- 375px: single-column content, 44px controls, no horizontal scroll.
- 768px: two-column card groups where content remains readable.
- 1024px+: split editorial layouts and album grids.
- Covers always reserve their footprint.
- Secondary metadata may wrap but never truncate essential Japanese titles.

## Anti-patterns

- Generic top charts, rank numbers or `HOT` badges.
- Oversized marketing slogans.
- Heavy glassmorphism and competing gradients.
- English-only navigation or mixed-language filler.
- Unverified biography, lyrics or release claims.
- Autoplay or presenting private audio as a public streaming service.
