/**
 * Ventes page — list of sales with filters, create new, view detail.
 */
import React, { useState, useEffect, useCallback } from 'react';
import { AppLayout } from '../layouts/AppLayout';
import Loader from '../components/common/Loader';
import Modal from '../components/common/Modal';
import EmptyState from '../components/common/EmptyState';
import Pagination from '../components/common/Pagination';
import NouvelleVenteForm from './NouvelleVenteForm';
import VenteDetail from './VenteDetail';
import { fetchVentes } from '../api/ventesApi';
import { useAuth } from '../hooks/useAuth';
import { Plus, ShoppingCart, Eye, CheckCircle, XCircle, Clock } from 'lucide-react';
import toast from 'react-hot-toast';

const STATUT_BADGE = {
  en_attente: 'badge-warning',
  confirmee:  'badge-success',
  annulee:    'badge-gray',
};
const STATUT_LABEL = {
  en_attente: 'En attente',
  confirmee:  'Confirmée',
  annulee:    'Annulée',
};

export default function Ventes() {
  const { isPharmacist } = useAuth();
  const [data, setData] = useState({ results: [], count: 0 });
  const [page, setPage] = useState(1);
  const [statut, setStatut] = useState('');
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  const load = useCallback(() => {
    setLoading(true);
    fetchVentes({ page, statut: statut || undefined })
      .then(setData)
      .catch(() => toast.error('Erreur lors du chargement.'))
      .finally(() => setLoading(false));
  }, [page, statut]);

  useEffect(() => { load(); }, [load]);

  const closeModal = () => { setModal(null); setSelectedId(null); };

  return (
    <AppLayout title="Ventes" subtitle="Historique des transactions">
      {/* Toolbar */}
      <div className="flex items-center gap-3 mb-6">
        <select value={statut} onChange={(e) => { setStatut(e.target.value); setPage(1); }}
          className="input-field max-w-[200px]">
          <option value="">Tous les statuts</option>
          <option value="en_attente">En attente</option>
          <option value="confirmee">Confirmée</option>
          <option value="annulee">Annulée</option>
        </select>
        <button className="btn-primary ml-auto" onClick={() => setModal('create')}>
          <Plus size={16} /> Nouvelle vente
        </button>
      </div>

      {loading ? <Loader /> : data.results.length === 0 ? (
        <EmptyState icon={ShoppingCart} title="Aucune vente" description="Créez votre première vente." />
      ) : (
        <div className="card">
          <div className="overflow-x-auto rounded-xl border border-gray-100">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-teal-50/60">
                  {['Référence','Date','Statut','Total','Créé par',''].map((h) => (
                    <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50 bg-white">
                {data.results.map((v) => (
                  <tr key={v.id} className="table-row-hover">
                    <td className="px-4 py-3 font-mono text-xs text-gray-700">{v.reference}</td>
                    <td className="px-4 py-3 text-gray-600 text-xs">
                      {new Date(v.date_vente).toLocaleString('fr-FR')}
                    </td>
                    <td className="px-4 py-3">
                      <span className={STATUT_BADGE[v.statut] || 'badge-gray'}>
                        {STATUT_LABEL[v.statut] || v.statut}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-semibold text-teal-700">{v.total_ttc} MAD</td>
                    <td className="px-4 py-3 text-gray-500">{v.created_by_username || '—'}</td>
                    <td className="px-4 py-3">
                      <button onClick={() => { setSelectedId(v.id); setModal('detail'); }}
                        className="p-1.5 rounded-lg hover:bg-teal-50 text-teal-500 hover:text-teal-700 transition-colors">
                        <Eye size={15} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pagination count={data.count} page={page} onChange={setPage} />
        </div>
      )}

      <Modal open={modal === 'create'} onClose={closeModal} title="Nouvelle vente" size="lg">
        <NouvelleVenteForm onSuccess={() => { closeModal(); load(); }} onCancel={closeModal} />
      </Modal>

      <Modal open={modal === 'detail'} onClose={closeModal} title="Détail de la vente" size="lg">
        <VenteDetail venteId={selectedId} isPharmacist={isPharmacist}
          onClose={() => { closeModal(); load(); }} />
      </Modal>
    </AppLayout>
  );
}
