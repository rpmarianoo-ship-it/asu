{
  "project_name": "MISE MANAGER",
  "domain": "Gastronomy SaaS Dashboard",
  "theme": "light",
  "archetype": "Archetype 4 (Swiss & High-Contrast) / Hybrid Gastronomy",
  "design_philosophy": "Modern, ultra-clean, data-focused, mobile-first SaaS. 'Profissional Blue' aesthetic blending authority (Swiss grid) with functional clarity. Eliminates 'Vercel default' look by employing deep navy sidebars, crisp 1px borders, and high-contrast typography.",
  "colors": {
    "background": {
      "default": "#F8FAFC",
      "paper": "#FFFFFF",
      "sidebar": "#0F172A"
    },
    "text": {
      "primary": "#0F172A",
      "secondary": "#475569",
      "muted": "#94A3B8",
      "inverse": "#F8FAFC"
    },
    "brand": {
      "primary": "#1E293B",
      "secondary": "#475569",
      "accent": "#2563EB",
      "highlight": "#38BDF8"
    },
    "semantic": {
      "success": "#10B981",
      "warning": "#F59E0B",
      "danger": "#EF4444",
      "info": "#3B82F6"
    },
    "chart_palette": [
      "#0F172A",
      "#3B82F6",
      "#10B981",
      "#F59E0B",
      "#EF4444",
      "#8B5CF6"
    ]
  },
  "typography": {
    "heading_font": "Cabinet Grotesk",
    "body_font": "Inter",
    "hierarchy": {
      "h1": "text-4xl sm:text-5xl tracking-tight font-black text-slate-900",
      "h2": "text-2xl sm:text-3xl tracking-tight font-bold text-slate-800",
      "h3": "text-xl sm:text-2xl font-semibold text-slate-800",
      "h4": "text-lg sm:text-xl font-medium text-slate-700",
      "body": "text-base text-slate-600 leading-relaxed",
      "small": "text-sm text-slate-500",
      "overline": "text-xs font-bold uppercase tracking-[0.2em] text-slate-400"
    }
  },
  "layout_and_spacing": {
    "spacing_scale": "Tailwind standard (p-4, p-6, p-8). Generous padding inside cards (p-6) to avoid text collision.",
    "dashboard_grid": "MODE B: THE 'CONTROL ROOM' GRID. Tight gaps (gap-4 or gap-6). Base grid: grid-cols-1 md:grid-cols-3 lg:grid-cols-4. Summary widgets col-span-1, charts col-span-2 or col-span-3.",
    "sidebar": "Fixed on desktop (w-64), retractable/collapsible on mobile (hamburger menu with slide-over). Deep Navy (#0F172A) background with inverse text.",
    "borders": "Crisp 1px solid borders (border-slate-200). Avoid heavy drop shadows; prefer light ambient shadow (shadow-sm) + border for definition."
  },
  "components": {
    "buttons": {
      "primary": "bg-slate-900 text-white hover:bg-slate-800 hover:-translate-y-0.5 transition-all duration-200 shadow-sm rounded-md px-4 py-2 font-medium",
      "secondary": "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 hover:-translate-y-0.5 transition-all duration-200 shadow-sm rounded-md px-4 py-2",
      "danger": "bg-red-500 text-white hover:bg-red-600 transition-colors rounded-md px-4 py-2"
    },
    "cards": {
      "base": "bg-white border border-slate-200 rounded-lg shadow-sm p-6",
      "interactive": "hover:shadow-md hover:border-slate-300 transition-all duration-200"
    },
    "inputs": {
      "base": "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow"
    },
    "tables": {
      "header": "bg-slate-50 text-slate-500 text-xs uppercase tracking-wider font-semibold py-3 px-4 text-left",
      "row": "border-b border-slate-200 hover:bg-slate-50/50 transition-colors",
      "cell": "py-3 px-4 text-sm text-slate-700"
    }
  },
  "icons": {
    "library": "react-icons/fa",
    "style": "FontAwesome (Solid & Regular). Use for sidebar navigation, module actions, and KPI widgets."
  },
  "charts": {
    "library": "chart.js and react-chartjs-2",
    "usage": "Ponto de Equilíbrio (Line/Area), Ticket Médio (Bar), Curva ABC (Pareto/Combo Chart), Matriz BCG (Scatter Plot)."
  },
  "motion_and_interactions": {
    "hover_states": "All buttons and interactive cards must have `-translate-y-0.5` and slight shadow increase.",
    "transitions": "Use `transition-all duration-200 ease-in-out` universally for color and transform changes.",
    "modals": "Backdrop blur (backdrop-blur-sm bg-slate-900/50) with scale-in animation."
  },
  "media": {
    "hero_backgrounds": [
      {
        "url": "https://images.unsplash.com/photo-1757621788643-395dc581dc6d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2ODl8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBjaGVmJTIwY29va2luZyUyMGluJTIwbW9kZXJuJTIwa2l0Y2hlbnxlbnwwfHx8fDE3NzY3MTMyMDN8MA&ixlib=rb-4.1.0&q=85",
        "category": "auth_background",
        "description": "Chef preparing food near a large pizza oven. Use with heavy dark or slate overlay (bg-slate-900/80) for the login screen."
      }
    ],
    "placeholders": [
      {
        "url": "https://images.unsplash.com/photo-1767500536384-8a1b29b52e92?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2ODl8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMGdvdXJtZXQlMjBjdWxpbmFyeSUyMGluZ3JlZGllbnRzJTIwcHJlcHxlbnwwfHx8fDE3NzY3MTMyMDN8MA&ixlib=rb-4.1.0&q=85",
        "category": "inventory_item_placeholder",
        "description": "Fresh ingredients for a meal laid out on a table. Fallback for inventory items."
      },
      {
        "url": "https://images.pexels.com/photos/6782744/pexels-photo-6782744.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "category": "menu_item_placeholder",
        "description": "Elegant top view of a gourmet salmon fillet. Fallback for Fichas Técnicas/Menu items."
      }
    ]
  },
  "accessibility_and_testing": {
    "contrast": "Ensure all text meets WCAG AA standards. Navy and Slate on White naturally comply.",
    "testing": "All interactive and key informational elements MUST include a `data-testid` attribute (kebab-case, role-based, e.g., `data-testid=\"sidebar-nav-inventory\"`, `data-testid=\"add-ingredient-btn\"`)."
  },
  "instructions_to_main_agent": [
    "1. Setup standard React + Tailwind + Shadcn environment. Install `react-icons`, `chart.js`, `react-chartjs-2`.",
    "2. Implement a responsive Sidebar Layout. Mobile view must use a Hamburger menu that triggers a slide-over. Desktop view is a fixed left sidebar with deep navy background (#0F172A).",
    "3. Use Inter for all body text. Use Cabinet Grotesk for Headings. If Cabinet Grotesk is unavailable, fallback to another Display Sans but NEVER use Inter for headings.",
    "4. For BI Dashboard: implement Chart.js components matching the 'Profissional Blue' palette (Navy, Slate, Blue, Green, Red).",
    "5. Follow 'Control Room' dense grid guidelines for the analytics view.",
    "6. Do not use generic placeholders (via.placeholder.com). Use the provided Unsplash/Pexels URLs in the media section.",
    "7. Include `data-testid` on ALL buttons, inputs, links, and forms."
  ]
}