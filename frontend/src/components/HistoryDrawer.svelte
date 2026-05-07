<script lang="ts">
  import { fly } from 'svelte/transition';
  import { X, Trash2, ChevronLeft, ChevronRight, Clock, Save } from 'lucide-svelte';
  import { historyClient, type ConversationSummary, type ConversationsResponse } from '../lib/historyClient';
  import type { Message } from '../lib/types';
  import ConfirmDeleteModal from './ConfirmDeleteModal.svelte';

  interface Props {
    isOpen: boolean;
    onClose: () => void;
    onLoadConversation: (messages: Message[]) => void;
  }

  let { isOpen, onClose, onLoadConversation }: Props = $props();

  let conversations = $state<ConversationSummary[]>([]);
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let sort = $state<'recent' | 'old'>('recent');
  let page = $state(1);
  let totalPages = $state(1);
  let deletingId = $state<number | null>(null);
  let showConfirmModal = $state(false);
  let pendingDeleteId = $state<number | null>(null);
  let skipDeleteConfirm = $state(false);

  async function loadSkipPreference() {
    try {
      const val = await historyClient.getPreference('skip_delete_confirm');
      skipDeleteConfirm = val === 'true';
    } catch {
      skipDeleteConfirm = false;
    }
  }

  async function loadConversations() {
    isLoading = true;
    error = null;
    try {
      const response = await historyClient.getConversations(sort, page);
      conversations = response.conversations;
      totalPages = response.total_pages;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Error cargando conversaciones';
    } finally {
      isLoading = false;
    }
  }

  async function handleLoad(id: number) {
    try {
      const detail = await historyClient.getConversation(id);
      onLoadConversation(detail.messages);
      onClose();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Error cargando conversación';
    }
  }

  async function handleDelete(id: number) {
    if (skipDeleteConfirm) {
      await performDelete(id);
      return;
    }
    pendingDeleteId = id;
    showConfirmModal = true;
  }

  async function performDelete(id: number) {
    deletingId = id;
    try {
      await historyClient.deleteConversation(id);
      await loadConversations();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Error eliminando conversación';
    } finally {
      deletingId = null;
    }
  }

  function handleConfirmDelete(dontAskAgain: boolean) {
    if (pendingDeleteId === null) return;
    if (dontAskAgain) {
      historyClient.setPreference('skip_delete_confirm', 'true').catch(() => {});
      skipDeleteConfirm = true;
    }
    performDelete(pendingDeleteId);
    showConfirmModal = false;
    pendingDeleteId = null;
  }

  function handleCancelDelete() {
    showConfirmModal = false;
    pendingDeleteId = null;
  }

  async function handleSortChange() {
    page = 1;
    await loadConversations();
  }

  function handlePrevPage() {
    if (page > 1) {
      page--;
      loadConversations();
    }
  }

  function handleNextPage() {
    if (page < totalPages) {
      page++;
      loadConversations();
    }
  }

  function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  $effect(() => {
    if (isOpen) {
      loadConversations();
      loadSkipPreference();
    }
  });
</script>

{#if isOpen}
  <div class="fixed inset-0 z-50 flex justify-end" transition:fly={{ x: 300, duration: 300 }}>
    <button
      class="absolute inset-0 bg-slate-900/40 cursor-default"
      onclick={onClose}
      aria-label="Cerrar drawer"
    ></button>

    <aside
      class="relative w-full max-w-md h-full bg-white shadow-2xl flex flex-col z-10"
      transition:fly={{ x: 300, duration: 300 }}
    >
      <header class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
        <h2 class="text-base font-semibold text-slate-800 flex items-center gap-2">
          <Clock size={18} class="text-teal-600" />
          Historial
        </h2>
        <button
          onclick={onClose}
          class="p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors"
        >
          <X size={20} />
        </button>
      </header>

      <div class="px-5 py-3 border-b border-slate-100">
        <select
          bind:value={sort}
          onchange={handleSortChange}
          class="w-full px-3 py-2 rounded-lg border border-slate-200 text-sm text-slate-700 bg-white focus:outline-none focus:border-teal-300"
        >
          <option value="recent">Más recientes</option>
          <option value="old">Más antiguos</option>
        </select>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar">
        {#if isLoading}
          <div class="flex items-center justify-center h-32">
            <div class="flex gap-1">
              <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
              <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
            </div>
          </div>
        {:else if error}
          <div class="p-5 text-center text-sm text-red-500">{error}</div>
        {:else if conversations.length === 0}
          <div class="flex flex-col items-center justify-center h-32 text-center px-4">
            <p class="text-sm text-slate-500">No hay conversaciones guardadas</p>
            <p class="text-xs text-slate-400 mt-1">Guarda una desde el chat para verla aquí</p>
          </div>
        {:else}
          <ul class="divide-y divide-slate-50">
            {#each conversations as conv (conv.id)}
              <li class="p-4 hover:bg-slate-50 transition-colors">
                <div class="flex items-start justify-between gap-2">
                  <button
                    onclick={() => handleLoad(conv.id)}
                    class="flex-1 text-left"
                  >
                    <p class="text-sm font-medium text-slate-700 line-clamp-2">{conv.title}</p>
                    <p class="text-xs text-slate-400 mt-1">{formatDate(conv.created_at)}</p>
                  </button>
                  <button
                    onclick={() => handleDelete(conv.id)}
                    disabled={deletingId === conv.id}
                    class="p-2 rounded-lg text-slate-300 hover:bg-red-50 hover:text-red-500 transition-colors disabled:opacity-50"
                    title="Eliminar"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </li>
            {/each}
          </ul>
        {/if}
      </div>

      {#if totalPages > 1}
        <footer class="flex items-center justify-between px-5 py-3 border-t border-slate-100">
          <button
            onclick={handlePrevPage}
            disabled={page === 1}
            class="p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronLeft size={18} />
          </button>
          <span class="text-xs text-slate-500">{page} / {totalPages}</span>
          <button
            onclick={handleNextPage}
            disabled={page === totalPages}
            class="p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronRight size={18} />
          </button>
        </footer>
      {/if}
    </aside>
  </div>
{/if}

<ConfirmDeleteModal
  isOpen={showConfirmModal}
  onConfirm={handleConfirmDelete}
  onCancel={handleCancelDelete}
/>
