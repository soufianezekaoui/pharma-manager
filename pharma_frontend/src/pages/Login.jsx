/**
 * Login page — JWT authentication form.
 */
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Cross } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(form);
      toast.success(`Bienvenue, ${user.username} !`);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Identifiants incorrects.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-grid-teal bg-[size:40px_40px]"
      style={{ background: 'linear-gradient(135deg, #0a817b 0%, #0d9e96 50%, #effcfa 100%)' }}>
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8 animate-slide-up mx-4">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center">
            <Cross size={18} className="text-white" fill="white" />
          </div>
          <div>
            <h1 className="font-display font-bold text-teal-800 text-xl leading-none">PharmaManager</h1>
            <p className="text-xs text-teal-500 mt-0.5">Connexion à votre espace</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 px-4 py-3 rounded-xl bg-red-50 border border-red-100 text-red-600 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Nom d'utilisateur</label>
            <input name="username" value={form.username} onChange={handleChange}
              className="input-field" placeholder="jean.dupont" required autoFocus />
          </div>
          <div>
            <label className="label">Mot de passe</label>
            <input name="password" type="password" value={form.password} onChange={handleChange}
              className="input-field" placeholder="••••••••" required />
          </div>
          <button type="submit" className="btn-primary w-full justify-center mt-2" disabled={loading}>
            {loading ? 'Connexion...' : 'Se connecter'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-400 mt-6">
          Pas de compte ?{' '}
          <Link to="/register" className="text-teal-600 font-medium hover:underline">S'inscrire</Link>
        </p>
      </div>
    </div>
  );
}
