/**
 * MedicamentForm — create or edit a medication.
 * Max: 150 lines
 */
import React, { useState, useEffect } from 'react';
import { fetchCategories, createMedicament, updateMedicament } from '../api/medicamentsApi';
import toast from 'react-hot-toast';

const EMPTY = {
  nom: '', dci: '', forme: '', dosage: '',
  prix_achat: '', prix_vente: '', stock_actuel: '', stock_minimum: '',
  date_expiration: '', categorie: '', ordonnance_requise: false, est_actif: true,
};

export default function MedicamentForm({ initial, onSuccess, onCancel }) {
  const [form, setForm] = useState(initial ? { ...initial } : EMPTY);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const isEdit = !!initial?.id;

  useEffect(() => {
    fetchCategories()
      .then((r) => setCategories(r.results || []))
      .catch(() => {});
  }, []);

  const set = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    try {
      if (isEdit) {
        await updateMedicament(initial.id, form);
        toast.success('Médicament mis à jour.');
      } else {
        await createMedicament(form);
        toast.success('Médicament créé.');
      }
      onSuccess();
    } catch (err) {
      const data = err.response?.data?.errors || {};
      setErrors(data);
      toast.error(err.response?.data?.message || 'Erreur de validation.');
    } finally {
      setLoading(false);
    }
  };

  const field = (name, label, type = 'text', extra = {}) => (
    <div>
      <label className="label">{label}</label>
      <input
        name={name} type={type} value={form[name] ?? ''} onChange={set}
        className={`input-field ${errors[name] ? 'border-red-400 focus:border-red-400 focus:ring-red-100' : ''}`}
        {...extra}
      />
      {errors[name] && <p className="text-xs text-red-500 mt-1">{errors[name]}</p>}
    </div>
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        {field('nom', 'Nom commercial', 'text', { required: true, placeholder: 'Doliprane' })}
        {field('dci', 'DCI', 'text', { placeholder: 'Paracétamol' })}
      </div>
      <div className="grid grid-cols-2 gap-3">
        {field('forme', 'Forme galénique', 'text', { placeholder: 'Comprimé' })}
        {field('dosage', 'Dosage', 'text', { placeholder: '500mg' })}
      </div>
      <div>
        <label className="label">Catégorie</label>
        <select name="categorie" value={form.categorie ?? ''} onChange={set} className="input-field">
          <option value="">— Choisir —</option>
          {categories.map((c) => <option key={c.id} value={c.id}>{c.nom}</option>)}
        </select>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {field('prix_achat', "Prix d'achat (MAD)", 'number', { min: 0, step: '0.01', required: true })}
        {field('prix_vente', 'Prix de vente (MAD)', 'number', { min: 0, step: '0.01', required: true })}
      </div>
      <div className="grid grid-cols-2 gap-3">
        {field('stock_actuel', 'Stock actuel', 'number', { min: 0, required: true })}
        {field('stock_minimum', 'Stock minimum', 'number', { min: 0, required: true })}
      </div>
      {field('date_expiration', "Date d'expiration", 'date')}
      <div className="flex items-center gap-6">
        <label className="flex items-center gap-2 cursor-pointer text-sm text-gray-700">
          <input type="checkbox" name="ordonnance_requise" checked={!!form.ordonnance_requise} onChange={set}
            className="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
          Ordonnance requise
        </label>
        {isEdit && (
          <label className="flex items-center gap-2 cursor-pointer text-sm text-gray-700">
            <input type="checkbox" name="est_actif" checked={!!form.est_actif} onChange={set}
              className="rounded border-gray-300 text-teal-600 focus:ring-teal-500" />
            Actif
          </label>
        )}
      </div>
      <div className="flex justify-end gap-3 pt-2">
        <button type="button" onClick={onCancel} className="btn-secondary" disabled={loading}>Annuler</button>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Enregistrement...' : isEdit ? 'Mettre à jour' : 'Créer'}
        </button>
      </div>
    </form>
  );
}
