import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import Layout from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import Inventario from "@/pages/Inventario";
import FichasTecnicas from "@/pages/FichasTecnicas";
import FichaEditor from "@/pages/FichaEditor";
import Precificacao from "@/pages/Precificacao";
import CMV from "@/pages/CMV";
import EngenhariaCardapio from "@/pages/EngenhariaCardapio";
import Perdas from "@/pages/Perdas";
import Vendas from "@/pages/Vendas";

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route element={<Layout />}>
                        <Route path="/" element={<Navigate to="/dashboard" replace />} />
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/inventario" element={<Inventario />} />
                        <Route path="/fichas" element={<FichasTecnicas />} />
                        <Route path="/fichas/novo" element={<FichaEditor />} />
                        <Route path="/fichas/:id" element={<FichaEditor />} />
                        <Route path="/precificacao" element={<Precificacao />} />
                        <Route path="/cmv" element={<CMV />} />
                        <Route path="/engenharia" element={<EngenhariaCardapio />} />
                        <Route path="/perdas" element={<Perdas />} />
                        <Route path="/vendas" element={<Vendas />} />
                    </Route>
                </Routes>
            </BrowserRouter>
            <Toaster position="top-right" richColors />
        </div>
    );
}

export default App;
