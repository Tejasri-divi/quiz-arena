import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setErrors([]);
    setLoading(true);
    try {
      await api.post('register/', { username, password });
      navigate('/login');
    } catch (err) {
      // Turn Django's error object into a simple list of messages
      const data = err.response?.data || {};
      const messages = Object.values(data).flat();
      setErrors(messages.length ? messages : ['Registration failed. Try again.']);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card narrow">
      <h2>Create your account</h2>
      <p className="muted">Use a strong password (8+ characters, not only numbers).</p>
      <form onSubmit={handleRegister}>
        <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Register'}</button>
      </form>
      {errors.map((m, i) => <p key={i} className="error">{m}</p>)}
      <p className="muted">Already registered? <Link to="/login">Login</Link></p>
    </div>
  );
}
