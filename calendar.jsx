export const PageHeader = ({ title, subtitle, actions, icon: Icon }) => (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-6 border-b border-slate-200 mb-6">
        <div className="flex items-start gap-4">
            {Icon && (
                <div className="hidden sm:flex w-12 h-12 rounded-lg bg-slate-900 items-center justify-center flex-shrink-0">
                    <Icon className="w-5 h-5 text-white" />
                </div>
            )}
            <div>
                <h1 className="font-display text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                    {title}
                </h1>
                {subtitle && <p className="text-sm text-slate-500 mt-1">{subtitle}</p>}
            </div>
        </div>
        {actions && <div className="flex items-center gap-2 flex-wrap">{actions}</div>}
    </div>
);

export default PageHeader;
