<script lang="ts">
  interface Props {
    isOpen: boolean;
    onConfirm: (dontAskAgain: boolean) => void;
    onCancel: () => void;
  }

  let { isOpen, onConfirm, onCancel }: Props = $props();

  let dontAskAgain = $state(false);
</script>

{#if isOpen}
  <div class="fixed inset-0 z-[100] flex items-center justify-center">
    <div class="absolute inset-0 bg-slate-900/50" onclick={onCancel} onkeydown={(e) => e.key === 'Escape' && onCancel()} role="button" tabindex="-1" aria-label="Cerrar modal"></div>
    <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm mx-4 overflow-hidden">
      <div class="p-6">
        <h3 class="text-lg font-semibold text-slate-800 mb-2">¿Eliminar esta conversación?</h3>
        <p class="text-sm text-slate-500 mb-5">Esta acción no se puede deshacer.</p>

        <label class="flex items-center gap-2 mb-5 cursor-pointer">
          <input
            type="checkbox"
            bind:checked={dontAskAgain}
            class="w-4 h-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
          />
          <span class="text-sm text-slate-600">No volver a preguntarme</span>
        </label>

        <div class="flex gap-3 justify-end">
          <button
            onclick={onCancel}
            class="px-4 py-2 rounded-lg text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors"
          >
            Cancelar
          </button>
          <button
            onclick={() => onConfirm(dontAskAgain)}
            class="px-4 py-2 rounded-lg text-sm font-medium text-white bg-red-600 hover:bg-red-700 transition-colors shadow-sm"
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}