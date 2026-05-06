<script lang="ts">
  import { Paperclip, Send } from 'lucide-svelte';

  interface Props {
    value: string;
    isLoading: boolean;
    onSend: (message: string) => void;
  }

  let { value = $bindable(''), isLoading, onSend }: Props = $props();

  function handleSubmit() {
    if (!value.trim() || isLoading) return;
    onSend(value.trim());
    value = '';
    const textarea = document.querySelector('textarea') as HTMLTextAreaElement;
    if (textarea) textarea.style.height = 'auto';
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleInput(e: Event) {
    const target = e.target as HTMLTextAreaElement;
    value = target.value;
    target.style.height = 'auto';
    target.style.height = Math.min(target.scrollHeight, 120) + 'px';
  }
</script>

<div class="flex-shrink-0 bg-white px-4 py-3 md:px-6 md:py-4 border-t border-slate-100 z-10">
  <div class="max-w-3xl mx-auto">
    <div class="relative bg-white rounded-2xl border border-slate-200 shadow-sm focus-within:shadow-md focus-within:border-teal-300 transition-all">
      <textarea
        bind:value
        onkeydown={handleKeydown}
        oninput={handleInput}
        placeholder="Escribe tu consulta..."
        rows="1"
        disabled={isLoading}
        class="w-full bg-transparent border-none outline-none focus:ring-0 resize-none text-sm text-slate-800 p-4 pr-12 min-h-[56px] max-h-[120px] placeholder:text-slate-400 disabled:opacity-50"
      ></textarea>
      <div class="absolute right-2 bottom-2 flex items-center gap-1">
        <button
          class="p-2 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors"
          title="Adjuntar"
        >
          <Paperclip size={20} />
        </button>
        <button
          onclick={handleSubmit}
          disabled={!value.trim() || isLoading}
          class="p-2 rounded-lg bg-teal-600 text-white hover:bg-teal-700 disabled:opacity-40 transition-colors shadow-sm"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
    <p class="text-center text-[11px] text-slate-400 mt-2">El asistente puede cometer errores. Verifica información importante.</p>
  </div>
</div>