<script lang="ts">
  import { CheckCircle, Save, RotateCcw } from 'lucide-svelte';

  interface Props {
    onFinalize?: () => void;
    onGuardar?: () => void;
    onContinue?: () => void;
    showGuardar?: boolean;
    showContinue?: boolean;
  }

  let { onFinalize, onGuardar, onContinue, showGuardar = false, showContinue = false }: Props = $props();
</script>

<header class="hidden md:flex items-center justify-between px-5 py-3 bg-white border-b border-slate-100 z-10">
  <div class="flex flex-col">
    <h2 class="text-base font-semibold text-slate-800">Nueva Consulta</h2>
    <p class="text-xs text-slate-400">Asistente capacitado con vademécum nacional</p>
  </div>
  <div class="flex items-center gap-2">
    {#if showContinue}
      <button
        onclick={onContinue}
        class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-blue-600 text-white hover:bg-blue-700 transition-colors shadow-sm"
      >
        <RotateCcw size={18} />
        <span>Continuar</span>
      </button>
    {/if}
    {#if showGuardar}
      <button
        onclick={onGuardar}
        class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-teal-50 text-teal-700 hover:bg-teal-100 transition-colors"
      >
        <Save size={18} />
        <span>Guardar</span>
      </button>
    {/if}
    <button
      onclick={onFinalize}
      class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-teal-600 text-white hover:bg-teal-700 transition-colors shadow-sm"
    >
      <CheckCircle size={18} />
      <span>Finalizar</span>
    </button>
  </div>
</header>