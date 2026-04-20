import { NavLink } from "react-router-dom";
import {
    FaChartPie,
    FaBoxesStacked,
    FaBookOpen,
    FaMoneyBillWave,
    FaCalculator,
    FaChessKnight,
    FaTrashCan,
    FaReceipt,
    FaAngleLeft,
    FaAngleRight,
    FaUtensils,
} from "react-icons/fa6";

const items = [
    { to: "/dashboard", label: "Dashboard", icon: FaChartPie, testid: "sidebar-nav-dashboard" },
    { to: "/inventario", label: "Inventário", icon: FaBoxesStacked, testid: "sidebar-nav-inventario" },
    { to: "/fichas", label: "Fichas Técnicas", icon: FaBookOpen, testid: "sidebar-nav-fichas" },
    { to: "/precificacao", label: "Precificação", icon: FaMoneyBillWave, testid: "sidebar-nav-precificacao" },
    { to: "/cmv", label: "CMV", icon: FaCalculator, testid: "sidebar-nav-cmv" },
    { to: "/engenharia", label: "Eng. Cardápio", icon: FaChessKnight, testid: "sidebar-nav-engenharia" },
    { to: "/vendas", label: "Vendas", icon: FaReceipt, testid: "sidebar-nav-vendas" },
    { to: "/perdas", label: "Perdas", icon: FaTrashCan, testid: "sidebar-nav-perdas" },
];

const Sidebar = ({ collapsed = false, onToggle, onNavigate }) => {
    return (
        <div
            className="flex flex-col w-full h-screen bg-slate-900 text-slate-100 sidebar-scroll overflow-y-auto"
            data-testid="sidebar"
        >
            {/* Brand */}
            <div className={`flex items-center gap-3 px-5 py-5 border-b border-slate-800 ${collapsed ? "justify-center" : ""}`}>
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shadow-lg">
                    <FaUtensils className="text-white w-5 h-5" />
                </div>
                {!collapsed && (
                    <div>
                        <div className="font-display text-lg font-bold tracking-tight leading-none">MISE</div>
                        <div className="text-[10px] uppercase tracking-[0.2em] text-slate-400 mt-0.5">Manager</div>
                    </div>
                )}
            </div>

            {/* Nav */}
            <nav className="flex-1 px-3 py-4 space-y-1">
                {items.map((it) => {
                    const Icon = it.icon;
                    return (
                        <NavLink
                            key={it.to}
                            to={it.to}
                            onClick={onNavigate}
                            data-testid={it.testid}
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-all duration-200 ${
                                    isActive
                                        ? "bg-blue-600 text-white shadow-sm"
                                        : "text-slate-300 hover:bg-slate-800 hover:text-white"
                                } ${collapsed ? "justify-center" : ""}`
                            }
                        >
                            <Icon className="w-4 h-4 flex-shrink-0" />
                            {!collapsed && <span>{it.label}</span>}
                        </NavLink>
                    );
                })}
            </nav>

            {/* Toggle */}
            {onToggle && (
                <div className="border-t border-slate-800 p-3">
                    <button
                        onClick={onToggle}
                        className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-md text-xs text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                        data-testid="sidebar-toggle-btn"
                    >
                        {collapsed ? (
                            <FaAngleRight className="w-3 h-3" />
                        ) : (
                            <>
                                <FaAngleLeft className="w-3 h-3" />
                                <span>Recolher</span>
                            </>
                        )}
                    </button>
                </div>
            )}
        </div>
    );
};

export default Sidebar;
