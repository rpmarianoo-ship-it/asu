export const KpiCard = ({ label, value, hint, icon: Icon, accent = "slate", testid }) => {
    const accents = {
        slate: "bg-slate-900 text-white",
        blue: "bg-blue-600 text-white",
        green: "bg-emerald-500 text-white",
        amber: "bg-amber-500 text-white",
        red: "bg-red-500 text-white",
    };
    return (
        <div
            className="bg-white border border-slate-200 rounded-lg p-5 hover:border-slate-300 hover:shadow-sm transition-all duration-200"
            data-testid={testid}
        >
            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                    <div className="text-[11px] font-semibold uppercase tracking-[0.15em] text-slate-500 truncate">
                        {label}
                    </div>
                    <div className="mt-2 font-display text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight truncate">
                        {value}
                    </div>
                    {hint && <div className="text-xs text-slate-500 mt-1.5 truncate">{hint}</div>}
                </div>
                {Icon && (
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${accents[accent]}`}>
                        <Icon className="w-4 h-4" />
                    </div>
                )}
            </div>
        </div>
    );
};

export default KpiCard;
