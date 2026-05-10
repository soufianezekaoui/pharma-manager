/**
 * VenteDetail — detailed view of a single sale with its line items.
 */
import React, { useState, useEffect } from 'react';
import { fetchVente, updateVenteStatut } from '../api/ventesApi';
import Loader from '../components/common/Loader';
import { CheckCircle, XCircle, Clock, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const STATUT_CONFIG = {
  en_attente: { label: 'En attente',  icon: Clock,        cls: 'badge-warning' },
  confirmee:  { label: 'Confirmée',   icon: CheckCircle,  cls: 'badge-success' },
  annulee:    { label: 'Annulée',     icon: XCircle,      cls: 'badge-danger'  },
};

export default function VenteDetail({ venteId, onClose, isPharmacist }) {
  const [vente, setVente] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!venteId) return;
    setLoading(true);
    fetchVente(venteId)
      .then((r) => setVente(r.data))
      .catch(() => toast.error('Impossible de charger la vente.'))
      .finally(() => setLoading(false));
  }, [venteId]);

  const changeStatut = async (statut) => {
    setUpdating(true);
    try {
      const r = await updateVenteStatut(venteId, statut);
      setVente(r.data);
      toast.success('Statut mis à jour.');
    } catch (err) {
      toast.error(err.response?.data?.message || 'Erreur lors de la mise à jour.');
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <Loader />;
  if (!vente) return null;

  const cfg = STATUT_CONFIG[vente.statut] || {};
  const Icon = cfg.icon || Clock;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-gray-400 font-mono">{vente.reference}</p>
          <p className="text-sm text-gray-500 mt-0.5">
            {new Date(vente.date_vente).toLocaleString('fr-FR')}
            {' · '}{vente.created_by_detail?.username}
          </p>
        </div>
        <span className={`${cfg.cls} flex items-center gap-1`}>
          <Icon size={12} />{cfg.label}
        </span>
      </div>

      {/* Lines */}
      <div className="rounded-xl border border-gray-100 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-teal-50/60">
            <tr>
              <th className="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Médicament</th>
              <th className="px-4 py-2.5 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider">Qté</th>
              <th className="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">PU</th>
              <th className="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Sous-total</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50 bg-white">
            {vente.lignes?.map((l) => (
              <tr key={l.id}>
                <td className="px-4 py-3 font-medium text-gray-800">{l.medicament_detail?.nom}</td>
                <td className="px-4 py-3 text-center text-gray-600">{l.quantite}</td>
                <td className="px-4 py-3 text-right text-gray-600">{l.prix_unitaire} MAD</td>
                <td className="px-4 py-3 text-right font-semibold text-teal-700">{l.sous_total} MAD</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Total */}
      <div className="flex justify-end">
        <div className="text-right">
          <p className="text-xs text-gray-400 uppercase tracking-wider">Total TTC</p>
          <p className="text-2xl font-display font-bold text-teal-700">{vente.total_ttc} MAD</p>
        </div>
      </div>

      {vente.notes && (
        <div className="px-4 py-3 bg-gray-50 rounded-xl text-sm text-gray-600">
          <span className="font-medium text-gray-500">Notes :</span> {vente.notes}
        </div>
      )}

      {/* Actions for pharmacist */}
      {isPharmacist && vente.statut === 'en_attente' && (
        <div className="flex gap-3 pt-2 border-t border-gray-100">
          <button onClick={() => changeStatut('confirmee')} className="btn-primary" disabled={updating}>
            <CheckCircle size={15} /> Confirmer
          </button>
          <button onClick={() => changeStatut('annulee')} className="btn-danger" disabled={updating}>
            <XCircle size={15} /> Annuler la vente
          </button>
        </div>
      )}
    </div>
  );
}
