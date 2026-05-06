# Design: Migrate Frontend to Material Design 3

## Technical Approach

Migrate the Svelte frontend from basic TailwindCSS to a full Material Design 3 system. The approach involves installing `material-symbols`, creating a wrapper component, updating CSS with custom tokens, and incrementally replacing components. The new UI will have responsive navigation (mobile navs + desktop sidebar) and a chat header with action buttons.

## Architecture Decisions

### Decision: Icon System Wrapper

**Choice**: Create `MaterialSymbol.svelte` component wrapping material-symbols
**Alternatives considered**: Direct `<span class="material-symbols-outlined">` inline, use of Google Fonts link
**Rationale**: Svelte idiom - component props provide type safety, consistent API across app. Using NPM package ensures icons work offline and are versioned.

### Decision: Color Token Strategy

**Choice**: Preserve Teal as primary (`#00685f`), integrate new MD3 colors as secondary
**Alternatives considered**: Full replacement with MD3 colors, dual-theme system
**Rationale**: User preference - Teal is brand identity. Adding secondary colors expands design options without breaking existing teal usages.

### Decision: Responsive Detection

**Choice**: CSS-based visibility (hidden md:flex classes) + Svelte state for mobile-specific behavior
**Alternatives considered**: matchMedia JavaScript API, CSS media queries only
**Rationale**: Tailwind breakpoints (md:) handle layout cleanly. Svelte state needed for mobile-specific interactions (like bottom nav active states).

### Decision: Session ID Display

**Choice**: Truncate senderId to 8 chars + "..." suffix in sidebar footer
**Alternatives considered**: Show full ID, show hash only
**Rationale**: Balances usability (recognizable session) with privacy (full UUID not exposed). Consistent with original design's truncated display.

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        App.svelte                          │
│  ┌─────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │ MobileTopNav│  │  ChatHeader      │  │MobileBottom  │   │
│  │ (mobile)    │  │  (desktop)       │  │Nav(mobile)   │   │
│  └─────────────┘  └──────────────────┘  └──────────────┘   │
│         │                 │                  │            │
│         └─────────────────┼──────────────────┘            │
│                           │                                │
│              ┌────────────┴────────────┐                 │
│              │    NavigationSidebar    │                 │
│              │    (desktop only)       │                 │
│              │    - Logo/Branding      │                 │
│              │    - Nav links         │                 │
│              │    - Topics (OptionCard)│                │
│              │    - Session footer    │                 │
│              └─────────────────────────┘                 │
│                           │                                │
│         ┌─────────────────┼─────────────────┐            │
│         │                 │                 │            │
│  ┌──────┴──────┐  ┌───────┴───────┐  ┌─────┴────────┐  │
│  │ ChatWindow  │  │  ChatInput    │  │   Toast       │  │
│  │ - Messages  │  │  - textarea   │  │   Notification│  │
│  │ - Typing    │  │  - send btn   │  │   System     │  │
│  └─────────────┘  └───────────────┘  └──────────────┘  │
│                           │                                │
│                           ▼                                │
│                    rasaClient.ts                           │
│                    (Rasa API /webhooks/rest/webhook)       │
└─────────────────────────────────────────────────────────────┘
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `frontend/package.json` | Modify | Add `material-symbols` dependency |
| `frontend/src/app.css` | Modify | Add MD3 color tokens, fonts, custom scrollbar |
| `frontend/src/components/MaterialSymbol.svelte` | Create | Icon wrapper component |
| `frontend/src/components/NavigationSidebar.svelte` | Create | Desktop sidebar (refactored from PresentationPanel) |
| `frontend/src/components/MobileTopNav.svelte` | Create | Mobile top navigation bar |
| `frontend/src/components/MobileBottomNav.svelte` | Create | Mobile bottom navigation bar |
| `frontend/src/components/ChatHeader.svelte` | Create | Desktop chat header with actions |
| `frontend/src/components/MessageBubble.svelte` | Modify | Add sender labels, update styling |
| `frontend/src/components/ChatWindow.svelte` | Modify | Add date dividers, update typing indicator |
| `frontend/src/components/ChatInput.svelte` | Replace | New textarea-based component |
| `frontend/src/components/OptionCard.svelte` | Modify | Material icons, gradient backgrounds |
| `frontend/src/components/Toast.svelte` | Modify | Update to new color palette |
| `frontend/src/App.svelte` | Modify | Add new nav components, responsive layout |
| `frontend/src/lib/theme.ts` | Create | Color token exports for reuse |

## Component Interfaces

### MaterialSymbol.svelte

```svelte
<script lang="ts">
  interface Props {
    name: string;      // Material Symbol name
    size?: number;     // Font size in px (default: 24)
    filled?: boolean;  // Use filled variant (default: false)
  }
  let { name, size = 24, filled = false }: Props = $props();
</script>

<span
  class="material-symbols-outlined"
  style="font-variation-settings: 'FILL' {filled ? 1 : 0}; font-size: {size}px;"
>
  {name}
</span>
```

### ChatInput.svelte

```svelte
<script lang="ts">
  interface Props {
    value: string;
    isLoading: boolean;
    onSend: (message: string) => void;
  }
  // Binds to parent via $bindable
  // Textarea auto-expands 60px-150px
  // Includes attach_file and send buttons
</script>
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Component | MaterialSymbol renders correct icon | Unit test with different props |
| Component | ChatInput textarea expansion | Visual/manual test |
| Integration | Mobile nav visibility toggles at 768px | Browser devtools responsive mode |
| E2E | Full chat flow with Rasa | Manual test after implementation |
| Integration | Health check shows correct status | Visual indicator in header/sidebar |

## Migration / Rollout

**Phase 1**: Install dependencies, update app.css with tokens
**Phase 2**: Create MaterialSymbol wrapper, update OptionCard (lowest risk)
**Phase 3**: Replace PresentationPanel → NavigationSidebar
**Phase 4**: Add mobile navs, ChatHeader, update ChatWindow
**Phase 5**: Replace ChatInput, update MessageBubble, Toast
**Phase 6**: App.svelte layout integration, final testing

No data migration required. No feature flags needed. Rollback via `git checkout HEAD -- frontend/src/components frontend/src/app.css frontend/package.json`.

## Open Questions

- [ ] Exportar consulta: Should this export chat history as JSON/TXT? (placeholder only for now)
- [ ] Finalizar consulta: Should this end the Rasa session? (not implemented yet)
- [ ] Attachment button: Should it trigger file picker or just be visual placeholder? (placeholder for now)