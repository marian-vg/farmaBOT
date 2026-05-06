<script lang="ts">
  import { Home, Stethoscope, Pill, BarChart3 } from 'lucide-svelte';

  let activeItem = $state('home');

  const navItems = [
    { id: 'home', label: 'Inicio', icon: Home },
    { id: 'consults', label: 'Consultas', icon: Stethoscope },
    { id: 'meds', label: 'Recetas', icon: Pill },
    { id: 'data', label: 'Datos', icon: BarChart3 },
  ];
</script>

<nav class="md:hidden fixed bottom-0 left-0 w-full bg-white border-t border-slate-100 shadow-[0_-2px_8px_-2px_rgba(0,0,0,0.08)] z-50" style="padding-bottom: env(safe-area-inset-bottom, 0);">
  <div class="flex justify-around items-center h-14">
    {#each navItems as item}
      <button
        onclick={() => activeItem = item.id}
        class="flex flex-col items-center justify-center w-full h-full transition-colors {activeItem === item.id ? 'text-teal-600' : 'text-slate-400'}"
      >
        <div class="w-10 h-7 rounded-full {activeItem === item.id ? 'bg-teal-50 flex items-center justify-center' : ''}">
          <item.icon size={22} />
        </div>
        <span class="text-[10px] font-medium mt-0.5">{item.label}</span>
      </button>
    {/each}
  </div>
</nav>