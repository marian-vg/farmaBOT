<script lang="ts">
  import { Bot, Headphones, Mic, Star } from 'lucide-svelte';
  import OptionCard from './OptionCard.svelte';
  import type { OptionCard as OptionCardType } from '../lib/types';

  interface Props {
    onOptionClick: (question: string) => void;
    isOnline: boolean;
  }

  let { onOptionClick, isOnline }: Props = $props();

  const optionCards: OptionCardType[] = [
    {
      id: 'pami',
      title: 'Normativa PAMI',
      description: 'Coberturas, medicamentos esenciales, recetas y Dunkin',
      icon: 'pill',
      sampleQuestion: '¿Cuáles son los requisitos para la cobertura de medicamentos de PAMI?',
    },
    {
      id: 'dim',
      title: 'Requisitos DIM',
      description: 'Documentación, habilitación y normativas DM',
      icon: 'file',
      sampleQuestion: '¿Qué documentación necesito para gestionar una receta DEX?',
    },
    {
      id: 'cofaer',
      title: 'Regulaciones COFAER',
      description: 'Normativa del Consejo Profesional de Farmacéuticos',
      icon: 'shield',
      sampleQuestion: '¿Cuáles son las obligaciones legales de las farmacias respecto al control de cadena de frío?',
    },
    {
      id: 'oser',
      title: 'Criterios OSER',
      description: 'Regulaciones específicas de la obra social',
      icon: 'thermometer',
      sampleQuestion: '¿Qué dice la normativa sobre el control de temperatura en el almacenamiento de vacunas?',
    },
    {
      id: 'trazabilidad',
      title: 'Trazabilidad',
      description: 'Sistema de trazabilidad de medicamentos',
      icon: 'truck',
      sampleQuestion: '¿Cómo funciona el sistema de trazabilidad para medicamentos oncológicos?',
    },
  ];
</script>

<aside class="flex flex-col h-full bg-white border-r border-slate-100 overflow-hidden">
  <div class="p-8 border-b border-slate-100">
    <div class="flex items-center gap-4 mb-6">
      <div class="p-3.5 rounded-2xl bg-gradient-to-br from-teal-500 to-emerald-500 text-white shadow-lg shadow-teal-200">
        <Bot size={28} />
      </div>
      <div>
        <h1 class="text-2xl font-black text-slate-800 tracking-tight">
          Farmy<span class="text-teal-600 font-medium">Auditor</span>
        </h1>
        <div class="flex items-center gap-2 mt-0.5">
          <span class="flex h-2 w-2 rounded-full {isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}"></span>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
            {isOnline ? 'Rasa Orchestrator' : 'Offline'}
          </p>
        </div>
      </div>
    </div>

    <p class="text-sm text-slate-600 leading-relaxed mb-1">
      Asistente de <strong>auditoría farmacéutica</strong> especializado en normativas, trazabilidad y regulaciones vigentes.
    </p>
    <div class="flex items-center gap-3 text-[10px] text-slate-400 font-medium">
      <span class="flex items-center gap-1"><Headphones size={12} /> Voz + Texto</span>
      <span class="flex items-center gap-1"><Star size={12} /> RAG-powered</span>
    </div>
  </div>

  <div class="flex-1 overflow-y-auto p-6 space-y-4">
    <div class="mb-4">
      <h2 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3">
        Temas de Consulta
      </h2>
      <div class="space-y-2">
        {#each optionCards as card (card.id)}
          <OptionCard {card} onclick={onOptionClick} />
        {/each}
      </div>
    </div>
  </div>

  <div class="p-6 border-t border-slate-100 bg-slate-50/50">
    <div class="flex items-center gap-3 text-xs text-slate-500">
      <span class="text-teal-500"><Mic size={14} /></span>
      <span>Usa el micrófono o escribe tu consulta</span>
    </div>
  </div>
</aside>