import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import {
  LayoutDashboard, Pill, ShoppingCart, Tags, Users,
  LogOut, ChevronRight, Activity, Cross,
} from 'lucide-react'
import toast from 'react-hot-toast'

const pharmacistLinks = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Tableau de bord' },
  { to: '/medicaments', icon: Pill, label: 'Médicaments' },
  { to: '/categories', icon: Tags, label: 'Catégories' },
  { to: '/ventes', icon: ShoppingCart, label: 'Ventes' },
  { to: '/users', icon: Users, label: 'Utilisateurs' },
]

const clientLinks = [
  { to: '/dashboard', icon: Activity, label: 'Mon espace' },
  { to: '/medicaments', icon: Pill, label: 'Catalogue' },
  { to: '/ventes', icon: ShoppingCart, label: 'Mes achats' },
]

export function Sidebar() {
  const { user, logout, isPharmacist } = useAuth()
  const navigate = useNavigate()
  const links = isPharmacist ? pharmacistLinks : clientLinks

  const handleLogout = async () => {
    await logout()
    toast.success('Déconnexion réussie.')
    navigate('/login')
  }

  return (
    <aside className="fixed top-0 left-0 h-screen w-[260px] flex flex-col z-40"
      style={{ background: 'linear-gradient(160deg, #0a817b 0%, #0d9e96 45%, #22bbb0 100%)' }}>

      {/* Logo */}
      <div className="px-6 py-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center">
            <Cross size={18} className="text-white" fill="white" />
          </div>
          <div>
            <p className="font-display font-bold text-white text-lg leading-none">Pharma</p>
            <p className="text-teal-100/60 text-[10px] font-medium tracking-widest uppercase">Manager</p>
          </div>
        </div>
      </div>

      {/* User card */}
      <div className="mx-4 mt-4 px-4 py-3 rounded-xl bg-white/10 border border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center text-white font-bold text-sm">
            {user?.username?.[0]?.toUpperCase()}
          </div>
          <div className="min-w-0">
            <p className="text-white text-sm font-semibold truncate">{user?.username}</p>
            <p className="text-teal-100/60 text-xs capitalize">{user?.role === 'pharmacist' ? 'Pharmacien' : 'Client'}</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        <p className="px-4 py-2 text-[10px] font-semibold text-teal-100/40 uppercase tracking-widest">
          Navigation
        </p>
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? 'active' : ''}`
            }
          >
            <Icon size={17} />
            <span className="flex-1">{label}</span>
            <ChevronRight size={14} className="opacity-0 group-hover:opacity-100" />
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-white/10">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium text-teal-100/70 hover:text-white hover:bg-white/10 transition-all"
        >
          <LogOut size={16} />
          Se déconnecter
        </button>
      </div>
    </aside>
  )
}
