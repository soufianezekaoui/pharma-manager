import { Sidebar } from './Sidebar'
import { Header } from './Header'

export function AppLayout({ children, title, subtitle }) {
  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-[260px]">
        <Header title={title} subtitle={subtitle} />
        <main className="flex-1 p-6 animate-fade-in">
          {children}
        </main>
      </div>
    </div>
  )
}
