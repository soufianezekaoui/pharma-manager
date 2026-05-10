/**
 * Dashboard page — summary stats and low-stock alerts.
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AppLayout } from '../layouts/AppLayout';
import Loader from '../components/common/Loader';
import { fetchMedicaments, fetchAlertesStock } from '../api/medicamentsApi';
import { fetchVentes } from '../api/ventesApi';
import { Pill, ShoppingCart, AlertTriangle, TrendingUp } from 'lucide-react';

function StatCard({ icon: Icon, label, value, color = 'teal', sub }) {
  const colors = {
    teal: 'bg-teal-50 text-teal-600',
    amber: 'bg-amber-50 text-amber-600',
    blue: 'bg-blue-50 text-blue-600',
    red: 'bg-red-50 text-red-600',
  };
  return (
    <div className="stat-card">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${colors[color]}`}>
        <Icon size={20} />
      </div>
      <div>
        <p className="text-2xl font-display font-bold text-gray-800">{value ?? '—'}</p>
        <p className="text-sm text-gray-500">{label}</p>
        {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState({ meds: null, ventes: null, alertes: null });
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    Promise.all([fetchMedicaments(), fetchVentes(), fetchAlertesStock()])
      .then(([meds, ventes, alertes]) => {
        setStats({ meds: meds.count, ventes: ventes.count, alertes: alertes.count });
        setAlerts((alertes.results || []).slice(0, 5));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <AppLayout title="Tableau de bord"><Loader /></AppLayout>;

  const today = new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });

  return (
    <AppLayout title="Tableau de bord" subtitle={today}>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard icon={Pill} label="Médicaments" value={stats.meds} color="teal" />
        <StatCard icon={ShoppingCart} label="Ventes totales" value={stats.ventes} color="blue" />
        <StatCard icon={AlertTriangle} label="Stock bas" value={stats.alertes} color="amber" />
        <StatCard icon={TrendingUp} label="Actifs" value={stats.meds} color="teal" sub="catalogue actif" />
      </div>

      {alerts.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-gray-800 flex items-center gap-2">
              <AlertTriangle size={18} className="text-amber-500" /> Alertes de stock
            </h2>
            <Link to="/medicaments" className="text-xs text-teal-600 hover:underline">Voir tout</Link>
          </div>
          <div className="space-y-2">
            {alerts.map((m) => (
              <div key={m.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-700">{m.nom}</p>
                  <p className="text-xs text-gray-400">{m.forme} · {m.dosage}</p>
                </div>
                <div className="text-right">
                  <span className="badge-warning">{m.stock_actuel} / {m.stock_minimum} min</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </AppLayout>
  );
}
