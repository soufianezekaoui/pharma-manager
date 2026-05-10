/**
 * MedicamentTable — sortable, filterable table of medications.
 */
import React from 'react';
import { Pencil, Trash2, PackagePlus } from 'lucide-react';
import EmptyState from '../components/common/EmptyState';
import Pagination from '../components/common/Pagination';
import { Pill } from 'lucide-react';

export default function MedicamentTable({
  medicaments = [], count = 0, page = 1, onPageChange,
  onEdit, onDelete, onRestock, isPharmacist,
}) {
  if (!medicaments.length) {
    return <EmptyState icon={Pill} title="Aucun médicament" description="Ajoutez votre premier médicament pour commencer." />;
  }

  return (
    <div>
      <div className="overflow-x-auto rounded-xl border border-gray-100">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-teal-50/60 text-left">
              <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Médicament</th>
              <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Catégorie</th>
              <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Stock</th>
              <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Prix vente</th>
              <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Expiration</th>
              <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Statut</th>
              {isPharmacist && <th className="px-4 py-3 font-semibold text-gray-600 text-xs uppercase tracking-wider">Actions</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {medicaments.map((m) => (
              <tr key={m.id} className="table-row-hover bg-white">
                <td className="px-4 py-3">
                  <p className="font-medium text-gray-800">{m.nom}</p>
                  <p className="text-xs text-gray-400">{m.dci || '—'} · {m.forme || '—'} {m.dosage || ''}</p>
                </td>
                <td className="px-4 py-3 text-gray-600">{m.categorie_detail?.nom || '—'}</td>
                <td className="px-4 py-3">
                  <span className={`font-semibold ${m.is_low_stock ? 'text-amber-600' : 'text-teal-700'}`}>
                    {m.stock_actuel}
                  </span>
                  <span className="text-gray-400 text-xs"> / {m.stock_minimum} min</span>
                  {m.is_low_stock && <span className="badge-warning ml-1">Bas</span>}
                </td>
                <td className="px-4 py-3 font-medium text-gray-700">{m.prix_vente} MAD</td>
                <td className="px-4 py-3 text-gray-500 text-xs">
                  {m.date_expiration
                    ? <span className={m.is_expired ? 'text-red-500 font-medium' : ''}>{m.date_expiration}</span>
                    : '—'}
                </td>
                <td className="px-4 py-3">
                  {m.est_actif
                    ? <span className="badge-success">Actif</span>
                    : <span className="badge-gray">Inactif</span>}
                  {m.ordonnance_requise && <span className="badge-blue ml-1">Ordo</span>}
                </td>
                {isPharmacist && (
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1">
                      <button onClick={() => onRestock(m)} title="Réapprovisionner"
                        className="p-1.5 rounded-lg hover:bg-teal-50 text-teal-500 hover:text-teal-700 transition-colors">
                        <PackagePlus size={15} />
                      </button>
                      <button onClick={() => onEdit(m)} title="Modifier"
                        className="p-1.5 rounded-lg hover:bg-blue-50 text-blue-400 hover:text-blue-600 transition-colors">
                        <Pencil size={15} />
                      </button>
                      <button onClick={() => onDelete(m)} title="Désactiver"
                        className="p-1.5 rounded-lg hover:bg-red-50 text-red-400 hover:text-red-600 transition-colors">
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Pagination count={count} page={page} onChange={onPageChange} />
    </div>
  );
}
