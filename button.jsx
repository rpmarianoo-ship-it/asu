import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { FaBars, FaUtensils } from "react-icons/fa";

const Layout = () => {
    const [collapsed, setCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);
    useLocation();

    return (
        <div className="min-h-screen flex bg-slate-50">
            {/* Desktop sidebar */}
            <aside
                className={`hidden lg:flex transition-all duration-300 ${
                    collapsed ? "w-20" : "w-64"
                } flex-shrink-0`}
                data-testid="desktop-sidebar"
            >
                <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
            </aside>

            {/* Mobile sidebar */}
            <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
                <SheetContent side="left" className="p-0 w-72 bg-slate-900 border-slate-800">
                    <Sidebar collapsed={false} onNavigate={() => setMobileOpen(false)} />
                </SheetContent>
            </Sheet>

            {/* Main */}
            <main className="flex-1 min-w-0 flex flex-col">
                {/* Top bar mobile */}
                <header className="lg:hidden bg-white border-b border-slate-200 px-4 py-3 flex items-center justify-between sticky top-0 z-30">
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => setMobileOpen(true)}
                        data-testid="mobile-menu-btn"
                    >
                        <FaBars className="w-5 h-5" />
                    </Button>
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-md bg-slate-900 flex items-center justify-center">
                            <FaUtensils className="text-white w-4 h-4" />
                        </div>
                        <span className="font-display font-bold text-slate-900">MISE</span>
                    </div>
                    <div className="w-10" />
                </header>
                <div className="flex-1 overflow-x-hidden">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
