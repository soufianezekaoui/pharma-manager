/**
 * Medicaments page — list, search, add, edit, delete, restock.
 */
import React, { useState, useEffect, useCallback } from 'react';
import { AppLayout } from '../layouts/AppLayout';
import Loader from '../components/common/Loader';
import Modal from '../components/common/Modal';
import ConfirmDialog from '../components/common/ConfirmDialog';
import MedicamentTable from './MedicamentTable';
import MedicamentForm from './MedicamentForm';
import Restock from './Restock';
import { fetchMedicaments, deleteMedicament } from '../api/medicamentsApi';
import { useAuth } from '../hooks/useAuth';
import { Plus, Search } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Medicaments() {
  const { isPharmacist } = useAuth();
  const [data, setData] = useState({ results: [], count: 0 });
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(null); // null | 'create' | 'edit' | 'delete' | 'restock'
  const [selected, setSelected] = useState(null);

  const load = useCallback(() => {
    setLoading(true);
    fetchMedicaments({ page, search: search || undefined })
      .then(setData)
      .catch(() => toast.error('Erreur lors du chargement.'))
      .finally(() => setLoading(false));
  }, [page, search]);

  useEffect(() => { load(); }, [load]);

  const closeModal = () => { setModal(null); setSelected(null); };
  const onSuccess = () => { closeModal(); load(); };

  const handleDelete = async () => {
    try {
      await deleteMedicament(selected.id);
      toast.success('Médicament désactivé.');
      onSuccess();
    } catch { toast.error('Impossible de supprimer.'); }
  };

  return (
    <AppLayout title="Médicaments" subtitle="Gestion du catalogue">
      {/* Toolbar */}
      <div className="flex items-center gap-3 mb-6">
        <div className="relative flex-1 max-w-xs">
          <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            className="input-field pl-9" placeholder="Rechercher…"
            value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          />
        </div>
        {isPharmacist && (
          <button className="btn-primary" onClick={() => setModal('create')}>
            <Plus size={16} /> Ajouter
          </button>
        )}
      </div>

      {loading ? <Loader /> : (
        <div className="card">
          <MedicamentTable
            medicaments={data.results} count={data.count} page={page}
            onPageChange={setPage} isPharmacist={isPharmacist}
            onEdit={(m) => { setSelected(m); setModal('edit'); }}
            onDelete={(m) => { setSelected(m); setModal('delete'); }}
            onRestock={(m) => { setSelected(m); setModal('restock'); }}
          />
        </div>
      )}

      <Modal open={modal === 'create'} onClose={closeModal} title="Nouveau médicament" size="lg">
        <MedicamentForm onSuccess={onSuccess} onCancel={closeModal} />
      </Modal>

      <Modal open={modal === 'edit'} onClose={closeModal} title="Modifier le médicament" size="lg">
        <MedicamentForm initial={selected} onSuccess={onSuccess} onCancel={closeModal} />
      </Modal>

      <Modal open={modal === 'restock'} onClose={closeModal} title="Réapprovisionner" size="sm">
        <Restock medicament={selected} onSuccess={onSuccess} onCancel={closeModal} />
      </Modal>

      <ConfirmDialog
        open={modal === 'delete'} onClose={closeModal} onConfirm={handleDelete}
        title="Désactiver le médicament"
        message={`Désactiver "${selected?.nom}" ? Il ne sera plus visible dans le catalogue.`}
        confirmLabel="Désactiver"
      />
    </AppLayout>
  );
}
