<script lang="ts">
  import { Bot, FileText, Shield, Thermometer, Truck, Pill } from 'lucide-svelte';
  import type { OptionCard as OptionCardType } from '../lib/types';

  interface Props {
    card: OptionCardType;
    onclick: (question: string) => void;
  }

  let { card, onclick }: Props = $props();

  function handleClick() {
    onclick(card.sampleQuestion);
  }
</script>

<button
  onclick={handleClick}
  class="group w-full text-left p-4 rounded-xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 relative overflow-hidden"
>
  <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity from-teal-500 to-emerald-500"></div>

  <div class="relative flex items-start gap-4">
    <div class="flex-shrink-0 p-2.5 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-500 text-white shadow-lg">
      {#if card.icon === 'pill'}
        <FileText size={22} />
      {:else if card.icon === 'file'}
        <FileText size={22} />
      {:else if card.icon === 'shield'}
        <Shield size={22} />
      {:else if card.icon === 'thermometer'}
        <Thermometer size={22} />
      {:else if card.icon === 'truck'}
        <Truck size={22} />
      {:else}
        <FileText size={22} />
      {/if}
    </div>
    <div class="flex-1 min-w-0">
      <h3 class="font-bold text-slate-800 text-sm mb-1 group-hover:text-teal-700 transition-colors">
        {card.title}
      </h3>
      <p class="text-xs text-slate-500 leading-relaxed">{card.description}</p>
    </div>
  </div>

  <div class="mt-3 flex items-center gap-2">
    <span class="text-xs text-teal-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
      Preguntar sobre esto →
    </span>
  </div>
</button>