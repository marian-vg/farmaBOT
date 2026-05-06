<script lang="ts">
  import { Stethoscope, Bell, Settings } from 'lucide-svelte';
</script>

<nav class="md:hidden fixed top-0 left-0 w-full h-14 flex justify-between items-center px-4 z-50 bg-white shadow-sm border-b border-slate-100">
  <div class="flex items-center gap-2">
    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center">
      <Stethoscope size={18} color="white" />
    </div>
    <span class="text-base font-bold text-slate-800">Farmy</span>
  </div>
  <div class="flex items-center gap-1">
    <button class="p-2 rounded-lg hover:bg-slate-100 transition-colors">
      <Bell size={20} color="#64748b" />
    </button>
    <button class="p-2 rounded-lg hover:bg-slate-100 transition-colors">
      <Settings size={20} color="#64748b" />
    </button>
  </div>
</nav>