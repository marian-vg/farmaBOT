<script lang="ts">
  import { clsx } from 'clsx';
  import { fly } from 'svelte/transition';
  import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-svelte';
  import { getToasts, dismiss, type ToastType } from '../lib/toast.svelte';

  const styleMap: Record<ToastType, { bg: string; border: string; text: string; icon: typeof CheckCircle }> = {
    success: { bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-800', icon: CheckCircle },
    error: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-800', icon: AlertCircle },
    warning: { bg: 'bg-amber-50', border: 'border-amber-200', text: 'text-amber-800', icon: AlertTriangle },
    info: { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-800', icon: Info },
  };
</script>

<div class="fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none">
  {#each getToasts() as toast (toast.id)}
    <div
      transition:fly={{ x: 100, duration: 300 }}
      class={clsx(
        'flex items-center gap-3 px-4 py-3 rounded-xl border shadow-lg pointer-events-auto min-w-72 max-w-md',
        styleMap[toast.type].bg,
        styleMap[toast.type].border,
        styleMap[toast.type].text
      )}
    >
      {#if toast.type === 'success'}
        <CheckCircle size={20} />
      {:else if toast.type === 'error'}
        <AlertCircle size={20} />
      {:else if toast.type === 'warning'}
        <AlertTriangle size={20} />
      {:else}
        <Info size={20} />
      {/if}
      <span class="flex-1 text-sm font-medium">{toast.message}</span>
      <button
        onclick={() => dismiss(toast.id)}
        class="opacity-60 hover:opacity-100 transition-opacity"
      >
        <X size={16} />
      </button>
    </div>
  {/each}
</div>