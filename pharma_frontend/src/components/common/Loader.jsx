/**
 * Loader — full-screen or inline spinner.
 */
import React from 'react';

export default function Loader({ fullScreen = false, size = 'md', text = '' }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' };
  const spinner = (
    <div className="flex flex-col items-center gap-3">
      <div
        className={`${sizes[size]} border-3 border-teal-200 border-t-teal-600 rounded-full animate-spin`}
        style={{ borderWidth: 3 }}
        role="status"
        aria-label="Chargement..."
      />
      {text && <p className="text-sm text-teal-600 font-medium">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50">
        {spinner}
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center py-12">
      {spinner}
    </div>
  );
}
