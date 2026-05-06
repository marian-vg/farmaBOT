<script lang="ts">
  import { clsx } from 'clsx';
  import { marked } from 'marked';
  import { User, Bot, AlertCircle } from 'lucide-svelte';
  import type { Message } from '../lib/types';

  interface Props {
    message: Message;
    senderName?: string;
  }

  let { message, senderName = 'Farmy' }: Props = $props();

  function renderMarkdown(content: string): string {
    return marked.parse(content, { async: false }) as string;
  }

  const roleClasses = {
    user: 'bg-teal-600 text-white rounded-tr-xl',
    assistant: 'bg-white text-slate-700 rounded-tl-xl border border-slate-200',
    error: 'bg-red-50 text-red-700 rounded-tl-xl border border-red-100',
  };
</script>

<div class={clsx('flex flex-col gap-1.5 max-w-[80%]', message.role === 'user' ? 'self-end' : 'self-start')}>
  {#if message.role !== 'user'}
    <span class="text-[11px] text-slate-400 ml-2">{message.role === 'assistant' ? senderName : 'Error'}</span>
  {/if}

  <div class="flex items-end gap-2">
    {#if message.role !== 'user'}
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center flex-shrink-0 shadow-sm">
        {#if message.role === 'assistant'}
          <Bot size={16} color="white" />
        {:else}
          <AlertCircle size={16} color="white" />
        {/if}
      </div>
    {/if}

    <div class={clsx('px-4 py-3 rounded-2xl shadow-sm', roleClasses[message.role])}>
      {#if message.role === 'user'}
        <p class="text-sm">{message.content}</p>
      {:else}
        <div class="prose prose-sm max-w-none prose-slate">
          {@html renderMarkdown(message.content)}
        </div>
      {/if}
    </div>

    {#if message.role === 'user'}
      <div class="w-8 h-8 rounded-lg bg-teal-700 flex items-center justify-center flex-shrink-0 shadow-sm">
        <User size={16} color="white" />
      </div>
    {/if}
  </div>
</div>