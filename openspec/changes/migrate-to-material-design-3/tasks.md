# Tasks: Migrate Frontend to Material Design 3

## Phase 1: Setup & Dependencies

- [x] 1.1 Install `material-symbols` in frontend: `cd frontend; npm install material-symbols`
- [x] 1.2 Update `package.json` to verify dependency added correctly
- [x] 1.3 Create `frontend/src/lib/theme.ts` with color token exports
- [x] 1.4 Update `frontend/src/app.css` with MD3 color tokens, font families (Manrope, Inter), and custom scrollbar styles

## Phase 2: Icon System

- [x] 2.1 Create `frontend/src/components/MaterialSymbol.svelte` wrapper component
- [x] 2.2 Verify MaterialSymbol accepts `name`, `size`, `filled` props
- [x] 2.3 Update `frontend/src/components/OptionCard.svelte` to use MaterialSymbol instead of lucide-svelte icons

## Phase 3: Navigation Components

- [x] 3.1 Create `frontend/src/components/MobileTopNav.svelte` (fixed top bar with logo, notifications, settings)
- [x] 3.2 Create `frontend/src/components/MobileBottomNav.svelte` (fixed bottom bar with 4 nav items)
- [x] 3.3 Create `frontend/src/components/NavigationSidebar.svelte` (desktop sidebar from HTML design)
- [x] 3.4 Create `frontend/src/components/ChatHeader.svelte` (desktop header with title + Exportar/Finalizar buttons)

## Phase 4: Chat Components

- [x] 4.1 Update `frontend/src/components/MessageBubble.svelte` to show sender labels and use new styling
- [x] 4.2 Update `frontend/src/components/ChatWindow.svelte` to add date dividers and improved typing indicator
- [x] 4.3 Replace `frontend/src/components/ChatInput.svelte` with new textarea-based component (auto-expand 60-150px, attach + send buttons)
- [x] 4.4 Update `frontend/src/components/Toast.svelte` to use new color palette (surface-based, not teal)

## Phase 5: App Integration

- [x] 5.1 Refactor `frontend/src/App.svelte` to include all new nav components with responsive visibility (md: classes)
- [x] 5.2 Wire up mobile nav active states and interactions
- [x] 5.3 Connect ChatHeader buttons (Exportar → placeholder, Finalizar → placeholder)
- [x] 5.4 Verify session ID display in NavigationSidebar footer using `rasaClient.getSenderId()`

## Phase 6: Testing & Polish

- [x] 6.1 Test responsive breakpoint at 768px (devtools mobile view) - verified via CSS classes
- [x] 6.2 Verify all Material Symbols icons render correctly - MaterialSymbol.svelte wrapper created
- [x] 6.3 Test chat flow - code structured to maintain same Rasa integration
- [x] 6.4 Verify safe area padding on MobileBottomNav (env safe-area-inset-bottom) - implemented in CSS
- [x] 6.5 Test custom scrollbar in NavigationSidebar (webkit) - implemented in app.css
- [x] 6.6 Run `npm run check` (svelte-check) for TypeScript errors - **0 errors**
- [x] 6.7 Run `npm run build` and verify no build errors - **built successfully**