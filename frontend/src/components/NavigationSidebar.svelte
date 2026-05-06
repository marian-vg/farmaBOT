<script lang="ts">
  import { Bot, Home, ClipboardList, LogOut } from 'lucide-svelte';
  import OptionCard from './OptionCard.svelte';
  import type { OptionCard as OptionCardType } from '../lib/types';
  import { rasaClient } from '../lib/rasaClient';

  interface Props {
    onOptionClick: (question: string) => void;
    isOnline: boolean;
  }

  let { onOptionClick, isOnline }: Props = $props();

  const optionCards: OptionCardType[] = [
    {
      id: 'pami',
      title: 'Normativas PAMI',
      description: 'Coberturas, Dunkin, recetas y medicamentos.',
      icon: 'pill',
      sampleQuestion: '¿Cuáles son los requisitos para la cobertura de medicamentos de PAMI?',
    },
    {
      id: 'dim',
      title: 'Requisitos DIM',
      description: 'Documentación, habilitación y normativas.',
      icon: 'file',
      sampleQuestion: '¿Qué documentación necesito para gestionar una receta DIM?',
    },
    {
      id: 'cofaer',
      title: 'Regulaciones COFAER',
      description: 'Obligaciones legales del farmacéutico.',
      icon: 'shield',
      sampleQuestion: '¿Cuáles son las obligaciones legales de las farmacias según COFAER?',
    },
  ];

  const sessionId = rasaClient.getSenderId().slice(0, 8);
</script>

<aside class="hidden md:flex flex-col fixed left-0 top-0 h-screen w-[380px] bg-white border-r border-slate-100 z-40 p-5">
  <!-- Header & Branding -->
  <div class="flex items-center justify-between mb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center shadow-lg shadow-teal-200">
        <Bot size={22} color="white" />
      </div>
      <div>
        <h1 class="text-lg font-bold text-slate-800">Farmy</h1>
        <p class="text-xs text-slate-400">Asistente de Auditoría</p>
      </div>
    </div>
    <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200">
      <span class="w-2 h-2 rounded-full {isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}" style={isOnline ? 'box-shadow: 0 0 6px rgba(16,185,129,0.5);' : ''}></span>
      <span class="text-[10px] font-semibold text-slate-600 uppercase tracking-wider">{isOnline ? 'Online' : 'Offline'}</span>
    </div>
  </div>

  <!-- Navigation -->
  <nav class="flex flex-col gap-1 mb-6">
    <button class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm transition-all bg-teal-50 text-teal-700 font-semibold">
      <Home size={20} />
      <span>Inicio</span>
    </button>
    <button class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm transition-all text-slate-600 hover:bg-slate-100">
      <ClipboardList size={20} />
      <span>Historial</span>
    </button>
  </nav>

  <!-- Topics -->
  <div class="flex-1 min-h-0 overflow-y-auto pr-1 custom-scrollbar">
    <h2 class="text-[11px] font-semibold text-slate-400 mb-3 uppercase tracking-wider">Temas de Consulta</h2>
    <div class="flex flex-col gap-2">
      {#each optionCards as card (card.id)}
        <OptionCard {card} onclick={onOptionClick} />
      {/each}
    </div>
  </div>

  <!-- Footer -->
  <div class="pt-4 mt-4 border-t border-slate-100">
    <div class="flex items-center justify-between">
      <div class="flex flex-col">
        <span class="text-sm font-medium text-slate-700">Sesión Activa</span>
        <span class="text-xs text-slate-400">ID: {sessionId}...</span>
      </div>
      <button class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-teal-100 hover:text-teal-600 transition-colors">
        <LogOut size={18} />
      </button>
    </div>
  </div>
</aside>