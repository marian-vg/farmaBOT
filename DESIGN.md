<!DOCTYPE html>

<html lang="es"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Farmarag-Rasa - Consultas Farmacéuticas</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;900&amp;family=Inter:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "status-offline": "#EF4444",
                        "tertiary-fixed": "#ffdbce",
                        "tertiary-fixed-dim": "#ffb59a",
                        "primary-fixed-dim": "#6bd8cb",
                        "on-tertiary-fixed-variant": "#773215",
                        "on-primary": "#ffffff",
                        "inverse-surface": "#2c3130",
                        "on-tertiary-fixed": "#370e00",
                        "error-border": "#FEE2E2",
                        "tertiary-container": "#b05e3d",
                        "on-primary-container": "#f4fffc",
                        "primary-container": "#008378",
                        "surface-container-high": "#e4e9e7",
                        "error-container": "#ffdad6",
                        "error-surface": "#FEF2F2",
                        "on-error": "#ffffff",
                        "surface-container-highest": "#dee4e1",
                        "inverse-on-surface": "#edf2f0",
                        "on-surface": "#171d1c",
                        "secondary-fixed": "#6ffbbe",
                        "on-error-container": "#93000a",
                        "on-secondary-container": "#00714d",
                        "surface-variant": "#dee4e1",
                        "surface": "#f5faf8",
                        "on-secondary": "#ffffff",
                        "on-surface-variant": "#3d4947",
                        "on-secondary-fixed": "#002113",
                        "primary": "#00685f",
                        "status-online": "#10B981",
                        "secondary-container": "#6cf8bb",
                        "secondary-fixed-dim": "#4edea3",
                        "surface-container": "#eaefed",
                        "surface-dim": "#d6dbd9",
                        "on-tertiary": "#ffffff",
                        "on-tertiary-container": "#fffbff",
                        "background": "#f5faf8",
                        "on-secondary-fixed-variant": "#005236",
                        "text-main": "#334155",
                        "surface-base": "#F8FAFC",
                        "surface-panel": "#F1F5F9",
                        "on-primary-fixed-variant": "#005049",
                        "inverse-primary": "#6bd8cb",
                        "outline-variant": "#bcc9c6",
                        "on-primary-fixed": "#00201d",
                        "secondary": "#006c49",
                        "surface-bright": "#f5faf8",
                        "surface-container-lowest": "#ffffff",
                        "tertiary": "#924628",
                        "on-background": "#171d1c",
                        "text-muted": "#64748B",
                        "surface-container-low": "#f0f5f2",
                        "outline": "#6d7a77",
                        "surface-tint": "#006a61",
                        "primary-fixed": "#89f5e7",
                        "error": "#ba1a1a"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.25rem",
                        "lg": "0.5rem",
                        "xl": "0.75rem",
                        "full": "9999px"
                    },
                    "spacing": {
                        "stack-md": "1rem",
                        "stack-sm": "0.5rem",
                        "bubble-gap": "1rem",
                        "container-padding": "1.5rem",
                        "panel-width": "420px"
                    },
                    "fontFamily": {
                        "h1": ["Manrope"],
                        "body-sm": ["Inter"],
                        "label-caps": ["Inter"]
                    },
                    "fontSize": {
                        "h1": ["24px", { "lineHeight": "1.2", "letterSpacing": "-0.025em", "fontWeight": "900" }],
                        "body-sm": ["14px", { "lineHeight": "1.625", "fontWeight": "400" }],
                        "label-caps": ["12px", { "lineHeight": "1", "letterSpacing": "0.1em", "fontWeight": "700" }]
                    }
                }
            }
        }
    </script>
<style>
        .prose-sm p { margin-bottom: 0.5em; }
        .prose-sm p:last-child { margin-bottom: 0; }
        .prose-sm ul { list-style-type: disc; padding-left: 1.5em; margin-bottom: 0.5em; }
        .prose-sm strong { font-weight: 700; color: inherit; }
    </style>
</head>
<body class="bg-surface-base text-text-main font-body-sm h-screen w-full overflow-hidden flex flex-col md:flex-row">
<!-- Top Navigation Bar for Mobile -->
<nav class="md:hidden fixed top-0 left-0 w-full h-16 flex justify-between items-center px-container-padding z-50 bg-surface shadow-sm border-b border-surface-variant">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-2xl" data-weight="fill" style="font-variation-settings: 'FILL' 1;">medical_services</span>
<span class="font-h1 text-h1 text-primary">Farmarag</span>
</div>
<div class="flex items-center gap-4">
<span class="material-symbols-outlined text-on-surface-variant">notifications</span>
<span class="material-symbols-outlined text-on-surface-variant">settings</span>
</div>
</nav>
<!-- Side Navigation / Presentation Panel (Web) -->
<aside class="hidden md:flex flex-col fixed left-0 top-0 h-screen w-panel-width bg-surface-container-low border-r border-surface-variant z-40 p-container-padding">
<!-- Header & Branding -->
<div class="flex flex-col gap-4 mb-8 mt-2">
<div class="flex items-center justify-between">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-lg bg-primary-container flex items-center justify-center">
<span class="material-symbols-outlined text-primary text-xl" data-weight="fill" style="font-variation-settings: 'FILL' 1;">medical_information</span>
</div>
<div>
<h1 class="font-h1 text-h1 text-on-surface">Farmarag</h1>
<p class="font-body-sm text-body-sm text-text-muted">Asistente Virtual</p>
</div>
</div>
<!-- Status Indicator -->
<div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-base border border-surface-variant">
<span class="w-2 h-2 rounded-full bg-status-online animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.6)]"></span>
<span class="font-label-caps text-label-caps text-status-online uppercase tracking-widest">Online</span>
</div>
</div>
</div>
<!-- Navigation Links -->
<nav class="flex flex-col gap-stack-sm mb-8 flex-shrink-0">
<a class="flex items-center gap-3 px-4 py-3 rounded-lg bg-primary-container text-on-primary-container font-bold transition-colors" href="#">
<span class="material-symbols-outlined">dashboard</span>
<span class="font-body-sm text-body-sm">Home</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-colors" href="#">
<span class="material-symbols-outlined">medical_services</span>
<span class="font-body-sm text-body-sm">Consultations</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-colors" href="#">
<span class="material-symbols-outlined">medication</span>
<span class="font-body-sm text-body-sm">Prescriptions</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-colors" href="#">
<span class="material-symbols-outlined">analytics</span>
<span class="font-body-sm text-body-sm">Analytics</span>
</a>
</nav>
<!-- Suggested Topics Section -->
<div class="flex-grow flex flex-col min-h-0 overflow-y-auto pr-2 custom-scrollbar">
<h2 class="font-label-caps text-label-caps text-text-muted mb-4 uppercase tracking-wider">Temas sugeridos</h2>
<div class="flex flex-col gap-3">
<!-- Option Card 1 -->
<button class="w-full text-left p-4 rounded-xl border border-surface-variant bg-gradient-to-br from-primary-container/20 to-secondary-container/20 hover:scale-[1.02] hover:shadow-xl transition-all duration-300 relative overflow-hidden group">
<div class="flex items-center gap-3 mb-1">
<span class="material-symbols-outlined text-primary">search</span>
<span class="font-body-sm text-body-sm font-bold text-on-surface">Consultar Medicamento</span>
</div>
<p class="font-body-sm text-body-sm text-text-muted pl-9">Información sobre dosis, efectos secundarios y contraindicaciones.</p>
</button>
<!-- Option Card 2 -->
<button class="w-full text-left p-4 rounded-xl border border-surface-variant bg-gradient-to-br from-primary-container/20 to-secondary-container/20 hover:scale-[1.02] hover:shadow-xl transition-all duration-300 relative overflow-hidden group">
<div class="flex items-center gap-3 mb-1">
<span class="material-symbols-outlined text-primary">location_on</span>
<span class="font-body-sm text-body-sm font-bold text-on-surface">Farmacias Cercanas</span>
</div>
<p class="font-body-sm text-body-sm text-text-muted pl-9">Encuentra locales abiertos en tu zona actualmente.</p>
</button>
<!-- Option Card 3 -->
<button class="w-full text-left p-4 rounded-xl border border-surface-variant bg-gradient-to-br from-primary-container/20 to-secondary-container/20 hover:scale-[1.02] hover:shadow-xl transition-all duration-300 relative overflow-hidden group">
<div class="flex items-center gap-3 mb-1">
<span class="material-symbols-outlined text-primary">schedule</span>
<span class="font-body-sm text-body-sm font-bold text-on-surface">Horarios de Atención</span>
</div>
<p class="font-body-sm text-body-sm text-text-muted pl-9">Verifica horarios regulares y turnos de guardia.</p>
</button>
</div>
</div>
<!-- Session Info / Footer -->
<div class="mt-auto pt-6 border-t border-surface-variant flex items-center justify-between mt-4">
<div class="flex flex-col">
<span class="font-body-sm text-body-sm text-on-surface font-bold">Sesión Activa</span>
<span class="font-body-sm text-body-sm text-text-muted text-xs">ID: FRA-09283-A</span>
</div>
<button class="w-8 h-8 rounded-full bg-surface-container-high flex items-center justify-center text-on-surface-variant hover:bg-primary hover:text-on-primary transition-colors">
<span class="material-symbols-outlined text-sm">logout</span>
</button>
</div>
</aside>
<!-- Main Content Area (Chat Window) -->
<main class="flex-1 flex flex-col h-full w-full md:ml-[420px] pt-16 md:pt-0 bg-surface-base">
<!-- Chat Header (Visible on Desktop, sticky) -->
<header class="hidden md:flex flex-shrink-0 items-center justify-between px-container-padding py-4 bg-surface border-b border-surface-variant shadow-sm z-10">
<div class="flex flex-col">
<h2 class="font-body-sm text-body-sm font-bold text-on-surface">Nueva Consulta Farmacéutica</h2>
<p class="font-body-sm text-body-sm text-text-muted text-xs">Asistente capacitado con vademécum nacional</p>
</div>
<div class="flex gap-2">
<button class="px-4 py-2 rounded-lg bg-surface-container-high text-on-surface font-body-sm text-body-sm hover:bg-surface-variant transition-colors flex items-center gap-2">
<span class="material-symbols-outlined text-sm">download</span>
                    Exportar
                </button>
<button class="px-4 py-2 rounded-lg bg-primary text-on-primary font-body-sm text-body-sm hover:bg-primary-fixed-variant transition-colors shadow-sm">
                    Finalizar Consulta
                </button>
</div>
</header>
<!-- Chat History Area -->
<div class="flex-1 overflow-y-auto px-container-padding py-6 flex flex-col gap-bubble-gap custom-scrollbar">
<!-- Date Divider -->
<div class="flex items-center justify-center mb-4">
<span class="px-3 py-1 rounded-full bg-surface-container-low text-text-muted font-label-caps text-[10px] tracking-wider">Hoy, 10:42 AM</span>
</div>
<!-- Assistant Welcome Message -->
<div class="flex flex-col max-w-[85%] self-start">
<span class="font-body-sm text-xs text-text-muted mb-1 ml-1">Farmarag Assistant</span>
<div class="bg-surface text-on-surface p-4 rounded-xl rounded-tl-sm border border-surface-variant shadow-sm prose-sm">
<p>¡Hola! Soy Farmarag, tu asistente farmacéutico virtual. Estoy aquí para ayudarte con información sobre medicamentos, ubicaciones de farmacias y horarios.</p>
<p>¿En qué puedo asistirte hoy? Puedes seleccionar una de las opciones del panel lateral o escribirme tu consulta directamente.</p>
</div>
</div>
<!-- User Message -->
<div class="flex flex-col max-w-[85%] self-end">
<span class="font-body-sm text-xs text-text-muted mb-1 mr-1 text-right">Tú</span>
<div class="bg-primary text-on-primary p-4 rounded-xl rounded-tr-sm shadow-sm font-body-sm text-body-sm">
                    Hola. Necesito saber las contraindicaciones del Ibuprofeno 600mg, estoy tomando medicación para la presión.
                </div>
</div>
<!-- Assistant Response -->
<div class="flex flex-col max-w-[85%] self-start">
<span class="font-body-sm text-xs text-text-muted mb-1 ml-1">Farmarag Assistant</span>
<div class="bg-surface text-on-surface p-4 rounded-xl rounded-tl-sm border border-surface-variant shadow-sm prose-sm">
<p>Entiendo tu consulta. El <strong>Ibuprofeno 600mg</strong> es un antiinflamatorio no esteroideo (AINE).</p>
<p>Respecto a la hipertensión (presión alta), debes tener en cuenta lo siguiente:</p>
<ul>
<li>El ibuprofeno puede reducir el efecto de algunos medicamentos para la presión arterial, como los inhibidores de la ECA o los diuréticos.</li>
<li>Su uso regular o en dosis altas puede causar retención de líquidos y elevar la presión arterial.</li>
<li>Se recomienda precaución y, preferiblemente, consultar con el médico que prescribió tu medicación antihipertensiva antes de iniciar un tratamiento con ibuprofeno.</li>
</ul>
<p class="text-xs text-error mt-3 border-t border-surface-variant pt-2"><em>Aviso: Esta información no reemplaza el consejo médico profesional. Ante cualquier duda, consulta con tu médico de cabecera.</em></p>
</div>
</div>
<!-- Typing Indicator (Loading state example) -->
<div class="flex flex-col max-w-[85%] self-start mt-2">
<span class="font-body-sm text-xs text-text-muted mb-1 ml-1">Farmarag Assistant</span>
<div class="bg-surface p-4 rounded-xl rounded-tl-sm border border-surface-variant shadow-sm flex items-center gap-1.5 w-16">
<div class="w-1.5 h-1.5 bg-outline rounded-full animate-bounce" style="animation-delay: 0ms;"></div>
<div class="w-1.5 h-1.5 bg-outline rounded-full animate-bounce" style="animation-delay: 150ms;"></div>
<div class="w-1.5 h-1.5 bg-outline rounded-full animate-bounce" style="animation-delay: 300ms;"></div>
</div>
</div>
</div>
<!-- Chat Input Area -->
<div class="flex-shrink-0 bg-surface-base px-container-padding py-4 border-t border-surface-variant z-10 pb-8 md:pb-4">
<div class="max-w-4xl mx-auto relative bg-surface rounded-xl border border-surface-variant shadow-sm focus-within:ring-2 focus-within:ring-primary focus-within:border-primary transition-all">
<textarea class="w-full bg-transparent border-none focus:ring-0 resize-none font-body-sm text-body-sm text-on-surface p-4 pr-14 min-h-[60px] max-h-[150px]" placeholder="Escribe tu consulta farmacéutica aquí..." rows="1"></textarea>
<div class="absolute right-2 bottom-2 flex gap-1">
<button class="p-2 rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-colors" title="Adjuntar receta">
<span class="material-symbols-outlined text-xl">attach_file</span>
</button>
<button class="p-2 rounded-lg bg-primary text-on-primary hover:bg-primary-fixed-variant transition-colors shadow-sm flex items-center justify-center">
<span class="material-symbols-outlined text-xl" data-weight="fill" style="font-variation-settings: 'FILL' 1;">send</span>
</button>
</div>
</div>
<div class="text-center mt-2">
<span class="font-body-sm text-[11px] text-text-muted">Farmarag puede cometer errores. Considera verificar la información importante con un profesional de la salud.</span>
</div>
</div>
</main>
<!-- Bottom Navigation Bar for Mobile -->
<nav class="md:hidden fixed bottom-0 left-0 w-full bg-surface border-t border-surface-variant shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-50 flex justify-around items-center h-16 px-2 pb-safe">
<a class="flex flex-col items-center justify-center w-16 h-full text-primary" href="#">
<div class="w-12 h-8 rounded-full bg-primary-container flex items-center justify-center mb-1">
<span class="material-symbols-outlined text-xl" data-weight="fill" style="font-variation-settings: 'FILL' 1;">dashboard</span>
</div>
<span class="font-label-caps text-[10px] font-bold">Home</span>
</a>
<a class="flex flex-col items-center justify-center w-16 h-full text-on-surface-variant hover:text-primary transition-colors" href="#">
<span class="material-symbols-outlined text-xl mb-1">medical_services</span>
<span class="font-label-caps text-[10px]">Consults</span>
</a>
<a class="flex flex-col items-center justify-center w-16 h-full text-on-surface-variant hover:text-primary transition-colors" href="#">
<span class="material-symbols-outlined text-xl mb-1">medication</span>
<span class="font-label-caps text-[10px]">Meds</span>
</a>
<a class="flex flex-col items-center justify-center w-16 h-full text-on-surface-variant hover:text-primary transition-colors" href="#">
<span class="material-symbols-outlined text-xl mb-1">analytics</span>
<span class="font-label-caps text-[10px]">Data</span>
</a>
</nav>
<style>
        /* Custom scrollbar for webkit */
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background-color: #d6dbd9;
            border-radius: 20px;
        }
        .dark .custom-scrollbar::-webkit-scrollbar-thumb {
            background-color: #3d4947;
        }
        
        /* Safe area padding for mobile bottom nav */
        @supports (padding-bottom: env(safe-area-inset-bottom)) {
            .pb-safe {
                padding-bottom: env(safe-area-inset-bottom);
                height: calc(4rem + env(safe-area-inset-bottom));
            }
        }
    </style>
</body></html>