<script lang="ts">
  import { Download, CheckCircle } from 'lucide-svelte';

  interface Props {
    onExport?: () => void;
    onFinalize?: () => void;
  }

  let { onExport, onFinalize }: Props = $props();
</script>

<header class="hidden md:flex items-center justify-between px-5 py-3 bg-white border-b border-slate-100 z-10">
  <div class="flex flex-col">
    <h2 class="text-base font-semibold text-slate-800">Nueva Consulta</h2>
    <p class="text-xs text-slate-400">Asistente capacitado con vademécum nacional</p>
  </div>
  <div class="flex items-center gap-2">
    <button
      onclick={onExport}
      class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors"
    >
      <Download size={18} />
      <span>Exportar</span>
    </button>
    <button
      onclick={onFinalize}
      class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm bg-teal-600 text-white hover:bg-teal-700 transition-colors shadow-sm"
    >
      <CheckCircle size={18} />
      <span>Finalizar</span>
    </button>
  </div>
</header>