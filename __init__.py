import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, fmtBRL, fmtPct, fmtNum } from "@/lib/api";
import PageHeader from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import {
    Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { FaBookOpen, FaArrowLeft, FaFloppyDisk, FaPlus, FaTrash, FaFilePdf } from "react-icons/fa6";
import { toast } from "sonner";
import jsPDF from "jspdf";

const computeIngCustoUnit = (ing, sel) => {
    if (!sel) return 0;
    if (ing.tipo === "ficha") {
        const rend = Number(sel.rendimento_liquido) || 1;
        return Number(sel.custo_total) / rend;
    }
    return Number(sel.custo_por_unidade_uso);
};

const empty = {
    nome: "", categoria: "Prato", eh_sub_receita: false,
    ingredientes: [],
    rendimento_bruto: 1, rendimento_liquido: 1, unidade_rendimento: "porcao",
    porcoes: 1, tempo_preparo_min: 0, modo_preparo: "",
    impostos_pct: 6, cartao_pct: 3.5, delivery_pct: 0, outras_taxas_pct: 0, lucro_desejado_pct: 30,
    foto_url: "",
};

const FichaEditor = () => {
    const { id } = useParams();
    const nav = useNavigate();
    const [form, setForm] = useState(empty);
    const [insumos, setInsumos] = useState([]);
    const [fichas, setFichas] = useState([]);
    const [computed, setComputed] = useState({ custo_total: 0, custo_por_porcao: 0, preco_venda: 0, margem_contribuicao_rs: 0, margem_contribuicao_pct: 0 });
    const printRef = useRef(null);

    const loadOptions = useCallback(async () => {
        const [ri, rf] = await Promise.all([api.get("/insumos"), api.get("/fichas")]);
        setInsumos(ri.data);
        setFichas(rf.data.filter((f) => f.id !== id));
    }, [id]);

    const loadFicha = useCallback(async () => {
        if (!id) return;
        const r = await api.get(`/fichas/${id}`);
        setForm({ ...empty, ...r.data });
        setComputed(r.data);
    }, [id]);

    useEffect(() => { loadOptions(); loadFicha(); }, [loadOptions, loadFicha]);

    const addIngrediente = () => {
        setForm({
            ...form,
            ingredientes: [
                ...form.ingredientes,
                { _key: `ing-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`, tipo: "insumo", ref_id: "", quantidade: 0, unidade: "g", nome: "" },
            ],
        });
    };

    const updateIng = (idx, patch) => {
        const arr = [...form.ingredientes];
        arr[idx] = { ...arr[idx], ...patch };
        setForm({ ...form, ingredientes: arr });
    };

    const removeIng = (idx) => {
        const arr = [...form.ingredientes];
        arr.splice(idx, 1);
        setForm({ ...form, ingredientes: arr });
    };

    // Preview cost
    const estimatedCost = form.ingredientes.reduce((acc, ing) => {
        const qtd = Number(ing.quantidade) || 0;
        if (ing.tipo === "ficha") {
            const sub = fichas.find((f) => f.id === ing.ref_id);
            if (!sub) return acc;
            const rend = Number(sub.rendimento_liquido) || 1;
            return acc + (Number(sub.custo_total) / rend) * qtd;
        }
        const ins = insumos.find((i) => i.id === ing.ref_id);
        if (!ins) return acc;
        return acc + Number(ins.custo_por_unidade_uso) * qtd;
    }, 0);

    const porcoes = Number(form.porcoes) || 1;
    const custoPorPorc = estimatedCost / porcoes;
    const taxasSum = Number(form.impostos_pct || 0) + Number(form.cartao_pct || 0) + Number(form.delivery_pct || 0) + Number(form.outras_taxas_pct || 0) + Number(form.lucro_desejado_pct || 0);
    const markupDiv = 1 - taxasSum / 100;
    const precoEst = markupDiv > 0 ? custoPorPorc / markupDiv : custoPorPorc;
    const taxasVar = precoEst * ((Number(form.impostos_pct || 0) + Number(form.cartao_pct || 0) + Number(form.delivery_pct || 0) + Number(form.outras_taxas_pct || 0)) / 100);
    const mcRs = precoEst - custoPorPorc - taxasVar;
    const mcPct = precoEst > 0 ? (mcRs / precoEst) * 100 : 0;

    const save = async () => {
        try {
            const payload = {
                ...form,
                fator_conversao: undefined,
                rendimento_bruto: Number(form.rendimento_bruto),
                rendimento_liquido: Number(form.rendimento_liquido),
                porcoes: Number(form.porcoes),
                tempo_preparo_min: Number(form.tempo_preparo_min),
                impostos_pct: Number(form.impostos_pct),
                cartao_pct: Number(form.cartao_pct),
                delivery_pct: Number(form.delivery_pct),
                outras_taxas_pct: Number(form.outras_taxas_pct),
                lucro_desejado_pct: Number(form.lucro_desejado_pct),
                ingredientes: form.ingredientes
                    .filter((i) => i.ref_id)
                    .map((i) => ({ ...i, quantidade: Number(i.quantidade) })),
            };
            let res;
            if (id) res = await api.put(`/fichas/${id}`, payload);
            else res = await api.post("/fichas", payload);
            setComputed(res.data);
            setForm({ ...empty, ...res.data });
            toast.success(id ? "Ficha atualizada" : "Ficha criada");
            if (!id) nav(`/fichas/${res.data.id}`);
        } catch (e) {
            toast.error(e?.response?.data?.detail || "Erro ao salvar");
        }
    };

    const exportPDF = () => {
        const doc = new jsPDF({ unit: "mm", format: "a4" });
        let y = 15;
        doc.setFontSize(18); doc.setFont("helvetica", "bold");
        doc.text("FICHA TÉCNICA - " + (form.nome || "Sem nome"), 14, y); y += 8;
        doc.setFontSize(10); doc.setFont("helvetica", "normal");
        doc.text(`Categoria: ${form.categoria}  |  Porções: ${form.porcoes}  |  Tempo: ${form.tempo_preparo_min}min`, 14, y); y += 6;
        doc.text(`Rendimento: ${fmtNum(form.rendimento_bruto)} bruto → ${fmtNum(form.rendimento_liquido)} líq. (${form.unidade_rendimento})`, 14, y); y += 8;
        doc.setFont("helvetica", "bold"); doc.text("Ingredientes:", 14, y); y += 5;
        doc.setFont("helvetica", "normal");
        form.ingredientes.forEach((ing) => {
            const item = ing.tipo === "ficha" ? fichas.find((f) => f.id === ing.ref_id) : insumos.find((i) => i.id === ing.ref_id);
            const nome = item?.nome || ing.nome || "?";
            const line = `• ${nome}  —  ${fmtNum(ing.quantidade)} ${ing.unidade}`;
            doc.text(line, 16, y); y += 5;
            if (y > 275) { doc.addPage(); y = 15; }
        });
        y += 4;
        doc.setFont("helvetica", "bold"); doc.text("Modo de Preparo:", 14, y); y += 5;
        doc.setFont("helvetica", "normal");
        const lines = doc.splitTextToSize(form.modo_preparo || "—", 180);
        lines.forEach((l) => { doc.text(l, 14, y); y += 5; if (y > 275) { doc.addPage(); y = 15; } });
        y += 4;
        doc.setFont("helvetica", "bold"); doc.text("Custos e Precificação:", 14, y); y += 5;
        doc.setFont("helvetica", "normal");
        doc.text(`Custo total: ${fmtBRL(computed.custo_total || estimatedCost)}`, 14, y); y += 5;
        doc.text(`Custo por porção: ${fmtBRL(computed.custo_por_porcao || custoPorPorc)}`, 14, y); y += 5;
        doc.text(`Preço de venda sugerido: ${fmtBRL(computed.preco_venda || precoEst)}`, 14, y); y += 5;
        doc.text(`Margem de Contribuição: ${fmtBRL(computed.margem_contribuicao_rs || mcRs)} (${fmtPct(computed.margem_contribuicao_pct || mcPct)})`, 14, y);
        doc.save(`ficha-${(form.nome || "sem-nome").replace(/\s+/g, "-").toLowerCase()}.pdf`);
    };

    return (
        <div className="p-4 sm:p-6 lg:p-10 max-w-[1400px] mx-auto" ref={printRef}>
            <PageHeader
                title={id ? "Editar Ficha Técnica" : "Nova Ficha Técnica"}
                subtitle="Ingredientes, rendimento, custos e precificação"
                icon={FaBookOpen}
                actions={
                    <>
                        <Button variant="outline" onClick={() => nav("/fichas")} data-testid="back-fichas-btn">
                            <FaArrowLeft className="w-3 h-3 mr-2" /> Voltar
                        </Button>
                        {id && (
                            <Button variant="outline" onClick={exportPDF} data-testid="export-pdf-btn">
                                <FaFilePdf className="w-3 h-3 mr-2" /> PDF
                            </Button>
                        )}
                        <Button onClick={save} className="bg-slate-900 hover:bg-slate-800" data-testid="save-ficha-btn">
                            <FaFloppyDisk className="w-3 h-3 mr-2" /> Salvar
                        </Button>
                    </>
                }
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                    {/* Dados principais */}
                    <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-4">
                        <h3 className="font-display font-bold text-slate-900">Dados Gerais</h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div className="sm:col-span-2">
                                <Label>Nome da Ficha*</Label>
                                <Input value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} data-testid="ficha-nome" />
                            </div>
                            <div>
                                <Label>Categoria</Label>
                                <Input value={form.categoria} onChange={(e) => setForm({ ...form, categoria: e.target.value })} />
                            </div>
                            <div>
                                <Label>Porções</Label>
                                <Input type="number" value={form.porcoes} onChange={(e) => setForm({ ...form, porcoes: e.target.value })} data-testid="ficha-porcoes" />
                            </div>
                            <div>
                                <Label>Rend. Bruto</Label>
                                <Input type="number" step="0.01" value={form.rendimento_bruto} onChange={(e) => setForm({ ...form, rendimento_bruto: e.target.value })} />
                            </div>
                            <div>
                                <Label>Rend. Líquido (cocção)</Label>
                                <Input type="number" step="0.01" value={form.rendimento_liquido} onChange={(e) => setForm({ ...form, rendimento_liquido: e.target.value })} />
                            </div>
                            <div>
                                <Label>Unidade Rend.</Label>
                                <Select value={form.unidade_rendimento} onValueChange={(v) => setForm({ ...form, unidade_rendimento: v })}>
                                    <SelectTrigger><SelectValue /></SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="porcao">porção</SelectItem>
                                        <SelectItem value="g">g</SelectItem>
                                        <SelectItem value="kg">kg</SelectItem>
                                        <SelectItem value="ml">ml</SelectItem>
                                        <SelectItem value="l">L</SelectItem>
                                        <SelectItem value="un">un</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div>
                                <Label>Tempo (min)</Label>
                                <Input type="number" value={form.tempo_preparo_min} onChange={(e) => setForm({ ...form, tempo_preparo_min: e.target.value })} />
                            </div>
                            <div className="sm:col-span-2 flex items-center gap-3 pt-2">
                                <Switch
                                    id="sub-receita"
                                    checked={form.eh_sub_receita}
                                    onCheckedChange={(v) => setForm({ ...form, eh_sub_receita: v })}
                                    data-testid="ficha-sub-receita"
                                />
                                <Label htmlFor="sub-receita" className="cursor-pointer">É uma sub-receita (base/molho/massa)</Label>
                            </div>
                        </div>
                    </div>

                    {/* Ingredientes */}
                    <div className="bg-white border border-slate-200 rounded-lg p-5">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-display font-bold text-slate-900">Ingredientes</h3>
                            <Button size="sm" variant="outline" onClick={addIngrediente} data-testid="add-ingrediente-btn">
                                <FaPlus className="w-3 h-3 mr-2" /> Adicionar
                            </Button>
                        </div>
                        <div className="space-y-3">
                            {form.ingredientes.length === 0 && (
                                <div className="text-sm text-slate-400 text-center py-6">Nenhum ingrediente. Clique em "Adicionar".</div>
                            )}
                            {form.ingredientes.map((ing, idx) => {
                                const options = ing.tipo === "ficha" ? fichas : insumos;
                                const sel = options.find((o) => o.id === ing.ref_id);
                                const custoUnit = ing.tipo === "ficha"
                                    ? (sel ? (Number(sel.custo_total) / (Number(sel.rendimento_liquido) || 1)) : 0)
                                    : (sel ? Number(sel.custo_por_unidade_uso) : 0);
                                const custoItem = custoUnit * (Number(ing.quantidade) || 0);
                                return (
                                    <div key={idx} className="grid grid-cols-12 gap-2 items-end p-3 rounded-md bg-slate-50 border border-slate-100">
                                        <div className="col-span-12 sm:col-span-2">
                                            <Label className="text-xs">Tipo</Label>
                                            <Select value={ing.tipo} onValueChange={(v) => updateIng(idx, { tipo: v, ref_id: "" })}>
                                                <SelectTrigger><SelectValue /></SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="insumo">Insumo</SelectItem>
                                                    <SelectItem value="ficha">Sub-receita</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>
                                        <div className="col-span-12 sm:col-span-5">
                                            <Label className="text-xs">{ing.tipo === "ficha" ? "Sub-receita" : "Insumo"}</Label>
                                            <Select value={ing.ref_id} onValueChange={(v) => {
                                                const opt = options.find((o) => o.id === v);
                                                updateIng(idx, { ref_id: v, nome: opt?.nome || "", unidade: ing.tipo === "insumo" ? (opt?.unidade_uso || "g") : (opt?.unidade_rendimento || "porcao") });
                                            }}>
                                                <SelectTrigger data-testid={`ing-select-${idx}`}><SelectValue placeholder="Selecione..." /></SelectTrigger>
                                                <SelectContent>
                                                    {options.length === 0 && <div className="p-2 text-xs text-slate-400">Nenhum disponível</div>}
                                                    {options.map((o) => (
                                                        <SelectItem key={o.id} value={o.id}>{o.nome}</SelectItem>
                                                    ))}
                                                </SelectContent>
                                            </Select>
                                        </div>
                                        <div className="col-span-6 sm:col-span-2">
                                            <Label className="text-xs">Qtd</Label>
                                            <Input type="number" step="0.01" value={ing.quantidade} onChange={(e) => updateIng(idx, { quantidade: e.target.value })} data-testid={`ing-qtd-${idx}`} />
                                        </div>
                                        <div className="col-span-4 sm:col-span-2">
                                            <Label className="text-xs">Unid.</Label>
                                            <Input value={ing.unidade} onChange={(e) => updateIng(idx, { unidade: e.target.value })} />
                                        </div>
                                        <div className="col-span-2 sm:col-span-1 flex items-center justify-end">
                                            <Button size="icon" variant="ghost" onClick={() => removeIng(idx)}>
                                                <FaTrash className="w-3 h-3 text-red-500" />
                                            </Button>
                                        </div>
                                        <div className="col-span-12 text-xs text-slate-500 -mt-1">
                                            Custo estimado: <span className="font-mono text-slate-900">{fmtBRL(custoItem)}</span>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Modo de preparo */}
                    <div className="bg-white border border-slate-200 rounded-lg p-5">
                        <h3 className="font-display font-bold text-slate-900 mb-3">Modo de Preparo</h3>
                        <Textarea
                            rows={6}
                            value={form.modo_preparo}
                            onChange={(e) => setForm({ ...form, modo_preparo: e.target.value })}
                            placeholder="Descreva o passo-a-passo..."
                        />
                    </div>
                </div>

                {/* Lateral: precificação e resumo */}
                <div className="space-y-6">
                    <div className="bg-slate-900 text-white rounded-lg p-5 sticky top-4">
                        <div className="text-xs uppercase tracking-[0.2em] text-slate-400 font-semibold">Resumo Financeiro</div>
                        <div className="mt-4 space-y-3">
                            <div className="flex items-baseline justify-between">
                                <span className="text-sm text-slate-400">Custo Total</span>
                                <span className="font-mono">{fmtBRL(estimatedCost)}</span>
                            </div>
                            <div className="flex items-baseline justify-between">
                                <span className="text-sm text-slate-400">Custo/porção</span>
                                <span className="font-mono font-bold">{fmtBRL(custoPorPorc)}</span>
                            </div>
                            <div className="flex items-baseline justify-between pt-3 border-t border-slate-800">
                                <span className="text-sm text-slate-400">Preço Sugerido</span>
                                <span className="font-display font-bold text-2xl text-blue-300">{fmtBRL(precoEst)}</span>
                            </div>
                            <div className="flex items-baseline justify-between">
                                <span className="text-sm text-slate-400">Margem R$</span>
                                <span className="font-mono text-emerald-400">{fmtBRL(mcRs)}</span>
                            </div>
                            <div className="flex items-baseline justify-between">
                                <span className="text-sm text-slate-400">Margem %</span>
                                <span className="font-mono text-emerald-400">{fmtPct(mcPct)}</span>
                            </div>
                        </div>
                    </div>

                    <Tabs defaultValue="markup" className="bg-white border border-slate-200 rounded-lg">
                        <TabsList className="w-full rounded-none border-b border-slate-200 bg-transparent">
                            <TabsTrigger value="markup" className="flex-1">Markup</TabsTrigger>
                            <TabsTrigger value="info" className="flex-1">Info</TabsTrigger>
                        </TabsList>
                        <TabsContent value="markup" className="p-5 space-y-3">
                            <div>
                                <Label className="text-xs">Impostos (Simples) %</Label>
                                <Input type="number" step="0.1" value={form.impostos_pct} onChange={(e) => setForm({ ...form, impostos_pct: e.target.value })} data-testid="pct-impostos" />
                            </div>
                            <div>
                                <Label className="text-xs">Taxa Cartão %</Label>
                                <Input type="number" step="0.1" value={form.cartao_pct} onChange={(e) => setForm({ ...form, cartao_pct: e.target.value })} data-testid="pct-cartao" />
                            </div>
                            <div>
                                <Label className="text-xs">Comissão Delivery %</Label>
                                <Input type="number" step="0.1" value={form.delivery_pct} onChange={(e) => setForm({ ...form, delivery_pct: e.target.value })} data-testid="pct-delivery" />
                            </div>
                            <div>
                                <Label className="text-xs">Outras Taxas %</Label>
                                <Input type="number" step="0.1" value={form.outras_taxas_pct} onChange={(e) => setForm({ ...form, outras_taxas_pct: e.target.value })} />
                            </div>
                            <div>
                                <Label className="text-xs">Lucro Desejado %</Label>
                                <Input type="number" step="0.1" value={form.lucro_desejado_pct} onChange={(e) => setForm({ ...form, lucro_desejado_pct: e.target.value })} data-testid="pct-lucro" />
                            </div>
                            <div className="text-xs text-slate-500 pt-2 border-t border-slate-100">
                                Markup Divisor: <span className="font-mono font-bold text-slate-900">{markupDiv.toFixed(4)}</span>
                            </div>
                        </TabsContent>
                        <TabsContent value="info" className="p-5 text-xs text-slate-600 space-y-2">
                            <p><strong>Índice de Rendimento:</strong> {form.rendimento_bruto > 0 ? (Number(form.rendimento_liquido) / Number(form.rendimento_bruto)).toFixed(3) : "—"}</p>
                            <p className="text-slate-500">Calculado como rendimento líquido ÷ rendimento bruto.</p>
                            <p className="text-slate-500">As alterações no preço de insumos se propagam automaticamente para esta ficha ao salvar.</p>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
        </div>
    );
};

export default FichaEditor;
