<script lang="ts">
  import MobileTopNav from './components/MobileTopNav.svelte';
  import MobileBottomNav from './components/MobileBottomNav.svelte';
  import NavigationSidebar from './components/NavigationSidebar.svelte';
  import ChatHeader from './components/ChatHeader.svelte';
  import ChatWindow from './components/ChatWindow.svelte';
  import ChatInput from './components/ChatInput.svelte';
  import Toast from './components/Toast.svelte';
  import HistoryDrawer from './components/HistoryDrawer.svelte';
  import { rasaClient } from './lib/rasaClient';
  import { historyClient } from './lib/historyClient';
  import { show } from './lib/toast.svelte';
  import type { Message } from './lib/types';
  import { onMount } from 'svelte';

  const WELCOME_MESSAGE: Message = {
    role: 'assistant',
    content: '**Buenos días.** Soy el asistente de auditoría farmacéutica.\n\nPuedo ayudarle con consultas sobre **PAMI**, **DIM**, **COFAER**, **OSER**, recetas, trazabilidad y cadena de frío.\n\n ¿Qué desea revisar?',
  };

  const INACTIVITY_TIMEOUT_MS = 60_000;
  const RATE_LIMIT_MAX_REQUESTS = 8;
  const RATE_LIMIT_WINDOW_MS = 60_000;

  let messages = $state<Message[]>([WELCOME_MESSAGE]);
  let input = $state('');
  let isLoading = $state(false);
  let isOnline = $state(true);
  let showHistoryDrawer = $state(false);
  let userMessagesCount = $state(0);
  let isClosed = $state(false);
  let inactivityTimer: ReturnType<typeof setTimeout> | null = null;
  let requestTimestamps: number[] = [];

  function handleLoadConversation(msgs: Message[]) {
    messages = msgs;
    userMessagesCount = msgs.filter(m => m.role === 'user').length;
  }

  async function handleSend(messageText: string) {
    if (!messageText.trim() || isLoading || isClosed) return;
    if (!checkRateLimit()) return;

    resetInactivityTimer();

    messages = [...messages, { role: 'user', content: messageText }];
    userMessagesCount++;
    input = '';
    isLoading = true;

    try {
      const responses = await rasaClient.sendMessage(messageText);

      for (const response of responses) {
        if (response.text) {
          messages = [...messages, { role: 'assistant', content: response.text }];
        } else if (response.buttons) {
          const buttonText = response.buttons.map((b) => `• ${b.title}`).join('\n');
          messages = [...messages, { role: 'assistant', content: `Opciones disponibles:\n${buttonText}` }];
        }
      }

      if (responses.length === 0) {
        messages = [...messages, { role: 'error', content: 'No se recibió respuesta del servidor.' }];
        show('Respuesta vacía del servidor Rasa', 'warning');
      }
    } catch (error: unknown) {
      const err = error instanceof Error ? error.message : String(error);
      if (err === 'timeout') {
        messages = [...messages, { role: 'error', content: 'La consulta tardó demasiado. Intente nuevamente.' }];
        show('Timeout - Rasa tardó demasiado en responder', 'error');
      } else {
        messages = [...messages, { role: 'error', content: `Error: ${err}` }];
        show(`Error de conexión: ${err}`, 'error');
      }
    } finally {
      isLoading = false;
    }
  }

  function handleOptionClick(question: string) {
    handleSend(question);
  }

  function resetInactivityTimer() {
    if (inactivityTimer) clearTimeout(inactivityTimer);
    if (!isClosed) inactivityTimer = setTimeout(handleInactivityTimeout, INACTIVITY_TIMEOUT_MS);
  }

  function handleInactivityTimeout() {
    isClosed = true;
    isLoading = false;
    if (inactivityTimer) clearTimeout(inactivityTimer);
    show('Sesión cerrada por inactividad', 'info');
  }

  function handleContinue() {
    isClosed = false;
    requestTimestamps = [];
    resetInactivityTimer();
  }

  function checkRateLimit(): boolean {
    const now = Date.now();
    requestTimestamps = requestTimestamps.filter(t => now - t < RATE_LIMIT_WINDOW_MS);
    requestTimestamps.push(now);
    if (requestTimestamps.length >= RATE_LIMIT_MAX_REQUESTS) {
      isClosed = true;
      isLoading = false;
      if (inactivityTimer) clearTimeout(inactivityTimer);
      show('Demasiadas solicitudes. Sesión cerrada por rate limit.', 'error');
      return false;
    }
    return true;
  }

  function handleFinalize() {
    rasaClient.resetSession();
    messages = [WELCOME_MESSAGE];
    userMessagesCount = 0;
    input = '';
    isLoading = false;
    isClosed = false;
    requestTimestamps = [];
    resetInactivityTimer();
    show('Nueva conversación iniciada', 'info');
  }

  async function handleGuardar() {
    if (userMessagesCount === 0) return;
    try {
      await historyClient.saveConversation(rasaClient.getSenderId(), messages);
      show('Conversación guardada correctamente', 'success');
    } catch {
      show('Error al guardar la conversación', 'error');
    }
  }

  onMount(() => {
    function handleActivity() {
      if (!isClosed) resetInactivityTimer();
    }

    document.addEventListener('mousemove', handleActivity);
    document.addEventListener('keydown', handleActivity);
    document.addEventListener('click', handleActivity);

    resetInactivityTimer();

    return () => {
      document.removeEventListener('mousemove', handleActivity);
      document.removeEventListener('keydown', handleActivity);
      document.removeEventListener('click', handleActivity);
      if (inactivityTimer) clearTimeout(inactivityTimer);
    };
  });
</script>

<Toast />

<HistoryDrawer
  isOpen={showHistoryDrawer}
  onClose={() => showHistoryDrawer = false}
  onLoadConversation={handleLoadConversation}
/>

<div class="flex h-screen bg-slate-50 overflow-hidden">
  <NavigationSidebar onOptionClick={handleOptionClick} {isOnline} onHistorialClick={() => showHistoryDrawer = true} />

  <div class="flex-1 flex flex-col h-full w-full md:pl-[30%]">
    <MobileTopNav />
    <ChatHeader
      onFinalize={handleFinalize}
      onGuardar={handleGuardar}
      onContinue={handleContinue}
      showGuardar={userMessagesCount > 0}
      showContinue={isClosed}
    />

    <div class="flex-1 flex flex-col min-h-0 pt-14 md:pt-0">
      <ChatWindow {messages} {isLoading} />
    </div>

    <ChatInput bind:value={input} {isLoading} isClosed={isClosed} onSend={handleSend} />
  </div>

  <MobileBottomNav />
</div>