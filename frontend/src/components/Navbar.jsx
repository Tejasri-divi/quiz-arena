import { Link, useNavigate, useLocation } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  useLocation(); // re-render the navbar whenever the page changes
  const token = localStorage.getItem('token');
  const username = localStorage.getItem('username');

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="brand">🏆 Quiz Arena</Link>
      <div className="nav-links">
        <Link to="/leaderboard">Leaderboard</Link>
        {token ? (
          <>
            <Link to="/history">My History</Link>
            <span className="user-chip">👤 {username}</span>
            <button className="btn-small" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
