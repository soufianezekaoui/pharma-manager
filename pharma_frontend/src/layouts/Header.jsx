import { Bell, Search, Menu } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'

export function Header({ title, subtitle, onMenuToggle }) {
  const { user } = useAuth()

  return (
    <header className="h-16 flex items-center justify-between px-6 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-30">
      <div className="flex items-center gap-4">
        {onMenuToggle && (
          <button onClick={onMenuToggle} className="p-2 rounded-lg hover:bg-gray-100 lg:hidden">
            <Menu size={20} className="text-gray-500" />
          </button>
        )}
        <div>
          {title && <h1 className="font-display font-semibold text-gray-800 text-lg leading-none">{title}</h1>}
          {subtitle && <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button className="p-2 rounded-xl hover:bg-teal-50 text-gray-400 hover:text-teal-600 transition-colors relative">
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-teal-500 rounded-full" />
        </button>
        <div className="h-8 w-8 rounded-xl bg-teal-600 flex items-center justify-center text-white font-bold text-sm ml-2">
          {user?.username?.[0]?.toUpperCase()}
        </div>
      </div>
    </header>
  )
}
