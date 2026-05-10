/**
 * EmptyState — shown when a list has no results.
 */
import React from 'react';
import { Inbox } from 'lucide-react';

export default function EmptyState({
  icon: Icon = Inbox,
  title = 'Aucun résultat',
  description = '',
  action = null,
}) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-6 text-center">
      <div className="w-16 h-16 rounded-2xl bg-teal-50 flex items-center justify-center mb-4">
        <Icon size={28} className="text-teal-400" />
      </div>
      <h3 className="font-display font-semibold text-gray-700 text-lg mb-1">{title}</h3>
      {description && (
        <p className="text-sm text-gray-400 max-w-xs mb-5">{description}</p>
      )}
      {action}
    </div>
  );
}
