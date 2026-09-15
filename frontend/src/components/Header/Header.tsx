import { useAuth } from '../../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export function Header() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="header">
      <div className="header-inner">
        <h1 className="header-title" onClick={() => navigate('/products')}>
          Game Store
        </h1>
        <nav className="header-nav">
          <button className="header-link" onClick={() => navigate('/products')}>
            Products
          </button>
          <button className="header-logout" onClick={handleLogout}>
            Logout
          </button>
        </nav>
      </div>
    </header>
  )
}
