/**
 * NouvelleVenteForm — add line items and submit a new sale.
 */
import React, { useState, useEffect } from 'react';
import { fetchMedicaments } from '../api/medicamentsApi';
import { createVente } from '../api/ventesApi';
import { Plus, Trash2, ShoppingCart } from 'lucide-react';
import toast from 'react-hot-toast';

export default function NouvelleVenteForm({ onSuccess, onCancel }) {
  const [medicaments, setMedicaments] = useState([]);
  const [lignes, setLignes] = useState([{ medicament: '', quantite: 1 }]);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMedicaments({ est_actif: true, page_size: 100 })
      .then((r) => setMedicaments(r.results || []))
      .catch(() => {});
  }, []);

  const updateLigne = (i, key, val) =>
    setLignes((ls) => ls.map((l, idx) => idx === i ? { ...l, [key]: val } : l));

  const addLigne = () => setLignes((ls) => [...ls, { medicament: '', quantite: 1 }]);

  const removeLigne = (i) => setLignes((ls) => ls.filter((_, idx) => idx !== i));

  const total = lignes.reduce((sum, l) => {
    const med = medicaments.find((m) => String(m.id) === String(l.medicament));
    return sum + (med ? med.prix_vente * (parseInt(l.quantite, 10) || 0) : 0);
  }, 0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const filled = lignes.filter((l) => l.medicament && l.quantite > 0);
    if (!filled.length) { setError('Ajoutez au moins un médicament.'); return; }
    const ids = filled.map((l) => l.medicament);
    if (new Set(ids).size !== ids.length) { setError('Chaque médicament ne peut apparaître qu\'une seule fois.'); return; }
    setLoading(true);
    try {
      await createVente({
        notes,
        lignes: filled.map((l) => ({ medicament: parseInt(l.medicament, 10), quantite: parseInt(l.quantite, 10) })),
      });
      toast.success('Vente enregistrée avec succès.');
      onSuccess();
    } catch (err) {
      setError(err.response?.data?.message || 'Erreur lors de la création de la vente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="px-4 py-3 rounded-xl bg-red-50 border border-red-100 text-red-600 text-sm">{error}</div>}

      <div className="space-y-2">
        {lignes.map((l, i) => {
          const med = medicaments.find((m) => String(m.id) === String(l.medicament));
          return (
            <div key={i} className="flex items-center gap-2">
              <select value={l.medicament} onChange={(e) => updateLigne(i, 'medicament', e.target.value)}
                className="input-field flex-1">
                <option value="">— Médicament —</option>
                {medicaments.map((m) => (
                  <option key={m.id} value={m.id}>{m.nom} ({m.stock_actuel} dispo)</option>
                ))}
              </select>
              <input type="number" min="1" max={med?.stock_actuel || 9999}
                value={l.quantite} onChange={(e) => updateLigne(i, 'quantite', e.target.value)}
                className="input-field w-20 text-center" />
              <span className="text-sm text-gray-500 w-24 text-right whitespace-nowrap">
                {med ? `${(med.prix_vente * (parseInt(l.quantite, 10) || 0)).toFixed(2)} MAD` : '—'}
              </span>
              {lignes.length > 1 && (
                <button type="button" onClick={() => removeLigne(i)}
                  className="p-1.5 rounded-lg hover:bg-red-50 text-red-400 hover:text-red-600 transition-colors">
                  <Trash2 size={15} />
                </button>
              )}
            </div>
          );
        })}
      </div>

      <button type="button" onClick={addLigne} className="btn-ghost text-sm">
        <Plus size={15} /> Ajouter un médicament
      </button>

      <div>
        <label className="label">Notes (optionnel)</label>
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)}
          className="input-field resize-none" rows={2} placeholder="Remarques sur la vente…" />
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-gray-100">
        <div className="flex items-center gap-2 text-teal-700 font-display font-bold text-lg">
          <ShoppingCart size={18} />
          Total : {total.toFixed(2)} MAD
        </div>
        <div className="flex gap-3">
          <button type="button" onClick={onCancel} className="btn-secondary" disabled={loading}>Annuler</button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Enregistrement...' : 'Valider la vente'}
          </button>
        </div>
      </div>
    </form>
  );
}
