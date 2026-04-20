import { useEffect, useState } from "react";
import { api, fmtBRL, fmtPct } from "@/lib/api";
import PageHeader from "@/components/PageHeader";
import { Badge } from "@/components/ui/badge";
import { FaChessKnight } from "react-icons/fa6";
import {
    Chart as ChartJS, LinearScale, PointElement, Tooltip, Legend,
} from "chart.js";
import { Scatter } from "react-chartjs-2";

ChartJS.register(LinearScale, PointElement, Tooltip, Legend);

const COLORS = {
    "Estrela": "#10b981",
    "Burro de Carga": "#3b82f6",
    "Quebra-cabeça": "#f59e0b",
    "Cão": "#ef4444",
};

const DESCRIPTIONS = {
    "Estrela": "Alta popularidade + alta rentabilidade. Destaque no cardápio.",
    "Burro de Carga": "Alta popularidade + baixa rentabilidade. Reduza custo ou aumente preço.",
    "Quebra-cabeça": "Baixa popularidade + alta rentabilidade. Promova ou relocalize.",
    "Cão": "Baixa popularidade + baixa rentabilidade. Considere remover.",
};

const EngenhariaCardapio = () => {
    const [data, setData] = useState({ items: [], qtd_media: 0, margem_media: 0 });

    useEffect(() => { api.get("/dashboard/bcg").then((r) => setData(r.data?.items ? r.data : { items: [], qtd_media: 0, margem_media: 0 })); }, []);

    const byClass = (cls) => data.items.filter((i) => i.classe === cls);

    const scatterData = {
        datasets: Object.keys(COLORS).map((cls) => ({
            label: cls,
            data: byClass(cls).map((i) => ({ x: i.popularidade, y: i.rentabilidade, nome: i.nome })),
            backgroundColor: COLORS[cls],
            pointRadius: 8,
            pointHoverRadius: 10,
        })),
    };

    const scatterOpts = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: "bottom" },
            tooltip: {
                callbacks: {
                    label: (ctx) => `${ctx.raw.nome}: Vendas ${ctx.raw.x} / Margem ${ctx.raw.y}%`,
                },
            },
        },
        scales: {
            x: { title: { display: true, text: "Popularidade (qtd vendida)" }, grid: { color: "#f1f5f9" } },
            y: { title: { display: true, text: "Rentabilidade (% margem)" }, grid: { color: "#f1f5f9" } },
        },
    };

    return (
        <div className="p-4 sm:p-6 lg:p-10 max-w-[1600px] mx-auto">
            <PageHeader
                title="Engenharia de Cardápio"
                subtitle="Matriz BCG — classificação automática dos pratos"
                icon={FaChessKnight}
            />

            <div className="bg-white border border-slate-200 rounded-lg p-5 mb-6">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <div className="text-xs uppercase tracking-widest font-semibold text-slate-500">Dispersão</div>
                        <h3 className="font-display font-bold text-lg text-slate-900">Popularidade × Rentabilidade</h3>
                    </div>
                    <div className="text-xs text-slate-500 hidden sm:block">
                        Média vendas: <strong>{data.qtd_media}</strong> · Média margem: <strong>{fmtPct(data.margem_media)}</strong>
                    </div>
                </div>
                <div className="h-80">
                    {data.items.length > 0
                        ? <Scatter data={scatterData} options={scatterOpts} />
                        : <div className="h-full flex items-center justify-center text-slate-400 text-sm">Registre vendas para visualizar a matriz BCG.</div>
                    }
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.keys(COLORS).map((cls) => {
                    const list = byClass(cls);
                    return (
                        <div key={cls} className="bg-white border border-slate-200 rounded-lg p-5">
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <span className="w-3 h-3 rounded-full" style={{ background: COLORS[cls] }} />
                                    <h3 className="font-display font-bold text-slate-900">{cls}</h3>
                                </div>
                                <Badge variant="secondary">{list.length} prato(s)</Badge>
                            </div>
                            <p className="text-xs text-slate-500 mb-3">{DESCRIPTIONS[cls]}</p>
                            <div className="space-y-2">
                                {list.length === 0 && <div className="text-xs text-slate-400 italic">Nenhum prato nesta classificação.</div>}
                                {list.map((i) => (
                                    <div key={i.ficha_id} className="flex items-center justify-between text-sm py-2 border-b border-slate-100 last:border-0">
                                        <span className="truncate text-slate-800">{i.nome}</span>
                                        <span className="text-xs text-slate-500 flex gap-3">
                                            <span>{i.popularidade} vendas</span>
                                            <span className="font-mono">{fmtBRL(i.lucro)}</span>
                                            <span className="text-emerald-600">{fmtPct(i.rentabilidade)}</span>
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default EngenhariaCardapio;
