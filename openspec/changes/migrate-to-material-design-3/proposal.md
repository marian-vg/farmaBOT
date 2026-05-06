# Proposal: Migrate Frontend to Material Design 3

## Intent

Reemplazar el frontend actual del chatbot (Svelte + TailwindCSS básico) con un sistema de diseño Material Design 3 completo. El objetivo es mejorar la experiencia de usuario con navegación responsive, paleta de colores profesional y tipografía definida, manteniendo la integración existente con Rasa.

## Scope

### In Scope
- Instalar dependencia `material-symbols`
- Actualizar configuración Tailwind con tokens MD3
- Crear wrapper `MaterialSymbol.svelte` para iconos
- Migrar todos los componentes UI a nueva estética
- Implementar navegación responsive (mobile top/bottom + desktop sidebar)
- Agregar header de chat con acciones (exportar, finalizar consulta)
- Mantener Teal como color primario, integrar nuevos colores como secundarios

### Out of Scope
- Cambios en la lógica de negocio o integración con Rasa
- Dark mode (futuro)
- PWA/offline capabilities

## Approach

1. **Fase 1**: Setup - instalar dependencias, actualizar config Tailwind/fonts
2. **Fase 2**: Componentes base - MessageBubble, OptionCard, ChatInput, ChatWindow
3. **Fase 3**: Navegación - MobileTopNav, MobileBottomNav, NavigationSidebar, ChatHeader
4. **Fase 4**: Layout - Reorganizar App.svelte con nuevos componentes
5. **Fase 5**: Refinamiento - scrollbar, safe areas, testing responsive

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `frontend/src/app.css` | Modified | Nuevos tokens de colores y fuentes |
| `frontend/src/components/*.svelte` | New/Modified | Todos los componentes UI |
| `frontend/package.json` | Modified | Añadir material-symbols dependency |
| `frontend/vite.config.ts` | Modified | Solo si requiere ajustes |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Breaking changes en iconos | Medium | Crear wrapper MaterialSymbol.svelte |
| Incompatibilidad con estilos actuales | Low | Phase-based testing, git rollback |

## Rollback Plan

```bash
git checkout HEAD -- frontend/src/components frontend/src/app.css frontend/package.json frontend/vite.config.ts
```

## Dependencies

- `material-symbols` v0.44.5 (NPM package)

## Success Criteria

- [ ] Chat funcional en desktop y mobile
- [ ] Navegación responsive visible en ambos viewports
- [ ] Iconos Material Symbols renderizando correctamente
- [ ] Colores aplicados según nueva paleta
- [ ] Toast notifications funcionando
- [ ] Integración Rasa sin cambios (health check passing)