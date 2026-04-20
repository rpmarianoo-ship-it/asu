@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap");
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
    margin: 0;
    font-family: "Inter", system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: #f8fafc;
    color: #0f172a;
}

h1, h2, h3, h4, .font-display {
    font-family: "Space Grotesk", "Inter", sans-serif;
    letter-spacing: -0.02em;
}

code {
    font-family: source-code-pro, Menlo, Monaco, Consolas, "Courier New", monospace;
}

@layer base {
    :root {
        --background: 210 20% 98%;
        --foreground: 222 47% 11%;
        --card: 0 0% 100%;
        --card-foreground: 222 47% 11%;
        --popover: 0 0% 100%;
        --popover-foreground: 222 47% 11%;
        --primary: 222 47% 11%;
        --primary-foreground: 210 20% 98%;
        --secondary: 210 16% 93%;
        --secondary-foreground: 222 47% 11%;
        --muted: 210 16% 93%;
        --muted-foreground: 215 16% 47%;
        --accent: 217 91% 60%;
        --accent-foreground: 0 0% 100%;
        --destructive: 0 84% 60%;
        --destructive-foreground: 0 0% 98%;
        --border: 214 32% 91%;
        --input: 214 32% 91%;
        --ring: 217 91% 60%;
        --chart-1: 222 47% 11%;
        --chart-2: 217 91% 60%;
        --chart-3: 160 84% 39%;
        --chart-4: 38 92% 50%;
        --chart-5: 0 84% 60%;
        --radius: 0.5rem;
    }
}

@layer base {
    * {
        @apply border-border;
    }
    body {
        @apply bg-background text-foreground;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.sidebar-scroll::-webkit-scrollbar-thumb { background: #334155; }

/* Transitions */
.btn-hover {
    transition: all 200ms ease-in-out;
}
.btn-hover:hover {
    transform: translateY(-1px);
}

/* Print styles */
@media print {
    body * { visibility: hidden; }
    .print-area, .print-area * { visibility: visible; }
    .print-area { position: absolute; left: 0; top: 0; width: 100%; }
    .no-print { display: none !important; }
}

@layer base {
    [data-debug-wrapper="true"] { display: contents !important; }
    [data-debug-wrapper="true"] > * {
        margin-left: inherit; margin-right: inherit; margin-top: inherit; margin-bottom: inherit;
        padding-left: inherit; padding-right: inherit; padding-top: inherit; padding-bottom: inherit;
        column-gap: inherit; row-gap: inherit; gap: inherit;
        border-left-width: inherit; border-right-width: inherit; border-top-width: inherit; border-bottom-width: inherit;
        border-left-style: inherit; border-right-style: inherit; border-top-style: inherit; border-bottom-style: inherit;
        border-left-color: inherit; border-right-color: inherit; border-top-color: inherit; border-bottom-color: inherit;
    }
}
