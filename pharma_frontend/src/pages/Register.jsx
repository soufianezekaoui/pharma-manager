/**
 * Register page — create a new user account.
 */
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../api/authApi';
import { Cross } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '', password2: '', role: 'client' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.password2) {
      setError('Les mots de passe ne correspondent pas.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      await register(form);
      toast.success('Compte créé ! Connectez-vous.');
      navigate('/login');
    } catch (err) {
      const data = err.response?.data?.errors || {};
      const msg = Object.values(data).flat()[0] || err.response?.data?.message || 'Erreur lors de l\'inscription.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4"
      style={{ background: 'linear-gradient(135deg, #0a817b 0%, #0d9e96 50%, #effcfa 100%)' }}>
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8 animate-slide-up">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center">
            <Cross size={18} className="text-white" fill="white" />
          </div>
          <h1 className="font-display font-bold text-teal-800 text-xl">Créer un compte</h1>
        </div>

        {error && (
          <div className="mb-4 px-4 py-3 rounded-xl bg-red-50 border border-red-100 text-red-600 text-sm">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Nom d'utilisateur</label>
            <input name="username" value={form.username} onChange={handleChange} className="input-field" required />
          </div>
          <div>
            <label className="label">Email</label>
            <input name="email" type="email" value={form.email} onChange={handleChange} className="input-field" required />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Mot de passe</label>
              <input name="password" type="password" value={form.password} onChange={handleChange} className="input-field" required />
            </div>
            <div>
              <label className="label">Confirmer</label>
              <input name="password2" type="password" value={form.password2} onChange={handleChange} className="input-field" required />
            </div>
          </div>
          <div>
            <label className="label">Rôle</label>
            <select name="role" value={form.role} onChange={handleChange} className="input-field">
              <option value="client">Client</option>
              <option value="pharmacist">Pharmacien</option>
            </select>
          </div>
          <button type="submit" className="btn-primary w-full justify-center" disabled={loading}>
            {loading ? 'Création...' : 'Créer le compte'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-400 mt-4">
          Déjà un compte ? <Link to="/login" className="text-teal-600 font-medium hover:underline">Se connecter</Link>
        </p>
      </div>
    </div>
  );
}
