# Delta for Frontend UI

## ADDED Requirements

### Requirement: Material Design 3 Icon System

The system SHALL use Material Symbols icons via the `material-symbols` package. All icon usage MUST be wrapped in a `MaterialSymbol.svelte` component that accepts `name`, `size`, and `filled` props.

#### Scenario: Render a filled icon at custom size

- GIVEN a MaterialSymbol component with props `name="send"`, `size=24`, `filled=true`
- WHEN rendered in the UI
- THEN the component displays a filled Material Symbol with font-variation-settings 'FILL' 1

#### Scenario: Render outline icon at default size

- GIVEN a MaterialSymbol component with props `name="medical_services"`
- WHEN rendered
- THEN the component displays an outline icon at 24px default size

### Requirement: Responsive Navigation

The system MUST display different navigation components based on viewport width:
- Mobile (< 768px): MobileTopNav (top) + MobileBottomNav (bottom)
- Desktop (≥ 768px): NavigationSidebar (fixed left)

#### Scenario: Mobile view displays both navs

- GIVEN viewport width is 375px
- WHEN app loads
- THEN MobileTopNav is visible at top, MobileBottomNav is visible at bottom, NavigationSidebar is hidden

#### Scenario: Desktop view displays sidebar only

- GIVEN viewport width is 1024px
- WHEN app loads
- THEN NavigationSidebar is visible on left, MobileTopNav and MobileBottomNav are hidden

### Requirement: Custom Color Palette

The system SHALL use a custom color palette where Teal primary colors are preserved. The following tokens MUST be available:

| Token | Value | Purpose |
|-------|-------|---------|
| `primary` | #00685f | Primary actions, headers |
| `primary-container` | #008378 | Active states, highlights |
| `on-primary` | #ffffff | Text on primary |
| `surface` | #f5faf8 | Main background |
| `surface-container-low` | #f0f5f2 | Panel backgrounds |
| `on-surface` | #171d1c | Primary text |
| `text-main` | #334155 | Body text |
| `text-muted` | #64748B | Secondary text |

#### Scenario: Chat bubbles use correct surface colors

- GIVEN a user views the chat window
- WHEN assistant messages render
- THEN they use `surface` (#f5faf8) background with `on-surface` (#171d1c) text

### Requirement: Chat Header with Actions

The desktop chat view MUST display a header with the title "Nueva Consulta Farmacéutica" and action buttons: "Exportar" and "Finalizar Consulta".

#### Scenario: Header actions are clickable

- GIVEN the chat header is visible on desktop
- WHEN user clicks "Exportar"
- THEN appropriate export handler is triggered (placeholder for future implementation)

### Requirement: Session Display

The system SHALL display the active session ID in the sidebar footer, derived from `rasaClient.getSenderId()` truncated to 8 characters.

#### Scenario: Session ID displayed correctly

- GIVEN rasaClient returns senderId "abc-123-def-456"
- WHEN NavigationSidebar renders session info
- THEN it displays "ID: abc-123-d..."

### Requirement: Custom Scrollbar Styling

Webkit browsers MUST show a custom scrollbar (6px width, rounded) on scrollable areas.

#### Scenario: Custom scrollbar applied

- GIVEN a user views NavigationSidebar with many topics
- WHEN scrolling occurs
- THEN the scrollbar is 6px wide with background-color #d6dbd9

### Requirement: Safe Area Padding for Mobile

Mobile bottom navigation MUST respect safe-area-inset-bottom on supported devices.

#### Scenario: Safe area respected on iOS

- GIVEN a user on iPhone with home indicator
- WHEN MobileBottomNav renders
- THEN padding-bottom accounts for safe-area-inset-bottom

## MODIFIED Requirements

### Requirement: Chat Input Component

The ChatInput component (previously simple input) SHALL be replaced with a textarea-based input that includes:
- Auto-expanding textarea (min 60px, max 150px height)
- Attachment button (placeholder)
- Send button with primary color
- Placeholder text "Escribe tu consulta farmacéutica aquí..."

(Previously: Simple input with send button only)

#### Scenario: Textarea auto-expands

- GIVEN user types a long message
- WHEN content exceeds one line
- THEN textarea expands up to max-height 150px before scrolling

### Requirement: Message Bubble with Metadata

The MessageBubble component SHALL display sender name (for assistant) and timestamp context.

(Previously: Simple bubbles without metadata labels)

#### Scenario: Assistant bubble shows sender label

- GIVEN an assistant message is rendered
- WHEN it appears in chat
- THEN it shows "Farmarag Assistant" label above the bubble

## REMOVED Requirements

### Requirement: Lucide Icons

The system SHALL NOT use lucide-svelte for icon display.

(Reason: Transitioning to Material Symbols per design requirement)

### Requirement: Teal-only Color Scheme

The previous limited teal/slate color palette is replaced by full MD3 palette.

(Reason: New design system requires comprehensive color tokens)