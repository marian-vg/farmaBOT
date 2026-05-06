<script lang="ts">
  import { Bot } from 'lucide-svelte';
  import MessageBubble from './MessageBubble.svelte';
  import type { Message } from '../lib/types';

  interface Props {
    messages: Message[];
    isLoading: boolean;
  }

  let { messages, isLoading }: Props = $props();

  let messagesEndRef = $state<HTMLDivElement | null>(null);

  function scrollToBottom() {
    messagesEndRef?.scrollIntoView({ behavior: 'smooth' });
  }

  $effect(() => {
    if (messages.length > 0) {
      scrollToBottom();
    }
  });

  const timeString = new Date().toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
</script>

<main class="flex-1 min-h-0 overflow-y-auto p-4 md:p-6 flex flex-col gap-4 bg-slate-50 custom-scrollbar">
  {#if messages.length === 0}
    <div class="flex flex-col items-center justify-center h-full text-center px-4">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center mb-4 shadow-lg shadow-teal-200">
        <Bot size={32} color="white" />
      </div>
      <h2 class="text-lg font-semibold text-slate-800 mb-2">Bienvenido al Asistente</h2>
      <p class="text-sm text-slate-500 max-w-sm">
        Selecciona un tema del panel lateral o escribe tu consulta para comenzar.
      </p>
    </div>
  {/if}

  {#if messages.length > 0}
    <div class="flex items-center justify-center">
      <span class="px-3 py-1 rounded-full bg-white text-slate-400 text-[11px] font-medium shadow-sm">
        Hoy, {timeString}
      </span>
    </div>
  {/if}

  {#each messages as message, index (index)}
    <MessageBubble {message} />
  {/each}

  {#if isLoading}
    <div class="flex flex-col gap-1 max-w-[80%] self-start">
      <span class="text-[11px] text-slate-400 ml-2">Farmarag</span>
      <div class="flex items-center gap-3 p-4 bg-white rounded-2xl rounded-tl-md border border-slate-200 shadow-sm">
        <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
        <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
        <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
      </div>
    </div>
  {/if}

  <div bind:this={messagesEndRef}></div>
</main>