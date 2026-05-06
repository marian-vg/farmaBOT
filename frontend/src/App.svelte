<script lang="ts">
  import MobileTopNav from './components/MobileTopNav.svelte';
  import MobileBottomNav from './components/MobileBottomNav.svelte';
  import NavigationSidebar from './components/NavigationSidebar.svelte';
  import ChatHeader from './components/ChatHeader.svelte';
  import ChatWindow from './components/ChatWindow.svelte';
  import ChatInput from './components/ChatInput.svelte';
  import Toast from './components/Toast.svelte';
  import { rasaClient } from './lib/rasaClient';
  import { show } from './lib/toast.svelte';
  import type { Message } from './lib/types';
  import { onMount } from 'svelte';

  let messages = $state<Message[]>([
    {
      role: 'assistant',
      content: '**Buenos días.** Soy el asistente de auditoría farmacéutica.\n\nPuedo ayudarle con consultas sobre **PAMI**, **DIM**, **COFAER**, **OSER**, recetas, trazabilidad y cadena de frío.\n\n ¿Qué desea revisar?',
    },
  ]);
  let input = $state('');
  let isLoading = $state(false);
  let isOnline = $state(false);

  onMount(async () => {
    isOnline = await rasaClient.checkHealth();
    if (!isOnline) {
      show('Rasa no está disponible. Verifique que esté ejecutándose en el puerto 5005.', 'error');
    }
  });

  async function handleSend(messageText: string) {
    if (!messageText.trim() || isLoading) return;

    messages = [...messages, { role: 'user', content: messageText }];
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

  function handleExport() {
    show('Exportar consulta - funcionalidad pendiente', 'info');
  }

  function handleFinalize() {
    show('Finalizar consulta - funcionalidad pendiente', 'info');
  }
</script>

<Toast />

<div class="flex h-screen bg-slate-50 overflow-hidden">
  <NavigationSidebar onOptionClick={handleOptionClick} {isOnline} />

  <div class="flex-1 flex flex-col h-full w-full md:pl-96">
    <MobileTopNav />
    <ChatHeader onExport={handleExport} onFinalize={handleFinalize} />

    <div class="flex-1 flex flex-col min-h-0 pt-14 md:pt-0">
      <ChatWindow {messages} {isLoading} />
    </div>

    <ChatInput bind:value={input} {isLoading} onSend={handleSend} />
  </div>

  <MobileBottomNav />
</div>