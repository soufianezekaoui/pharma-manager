/**
 * Restock — form to add units to a medication's stock.
 */
import React, { useState } from 'react';
import { restockMedicament } from '../api/medicamentsApi';
import { PackagePlus } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Restock({ medicament, onSuccess, onCancel }) {
  const [quantite, setQuantite] = useState('');
  const [loading, setLoading] = useState(false);

  if (!medicament) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const qty = parseInt(quantite, 10);
    if (!qty || qty <= 0) {
      toast.error('La quantité doit être un entier positif.');
      return;
    }
    setLoading(true);
    try {
      await restockMedicament(medicament.id, qty);
      toast.success(`+${qty} unités ajoutées à "${medicament.nom}".`);
      onSuccess();
    } catch (err) {
      toast.error(err.response?.data?.message || 'Erreur lors du réapprovisionnement.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Current stock info */}
      <div className="flex items-center gap-3 p-4 bg-teal-50 rounded-xl mb-5">
        <div className="w-9 h-9 rounded-xl bg-teal-100 flex items-center justify-center">
          <PackagePlus size={18} className="text-teal-600" />
        </div>
        <div>
          <p className="font-semibold text-gray-800 text-sm">{medicament.nom}</p>
          <p className="text-xs text-gray-500">
            Stock actuel :{' '}
            <span className={`font-bold ${medicament.is_low_stock ? 'text-amber-600' : 'text-teal-700'}`}>
              {medicament.stock_actuel}
            </span>
            {' '}/ min {medicament.stock_minimum}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="label">Quantité à ajouter</label>
          <input
            type="number"
            min="1"
            value={quantite}
            onChange={(e) => setQuantite(e.target.value)}
            className="input-field"
            placeholder="Ex: 50"
            required
            autoFocus
          />
          {quantite && parseInt(quantite, 10) > 0 && (
            <p className="text-xs text-teal-600 mt-1.5">
              Nouveau stock estimé : <strong>{medicament.stock_actuel + parseInt(quantite, 10)}</strong> unités
            </p>
          )}
        </div>

        <div className="flex justify-end gap-3 pt-1">
          <button type="button" onClick={onCancel} className="btn-secondary" disabled={loading}>
            Annuler
          </button>
          <button type="submit" className="btn-primary" disabled={loading || !quantite}>
            {loading ? 'Enregistrement...' : 'Valider le réapprovisionnement'}
          </button>
        </div>
      </form>
    </div>
  );
}
