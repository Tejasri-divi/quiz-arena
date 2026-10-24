import { useEffect, useState } from 'react';
import api from '../api';

export default function Leaderboard() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const me = localStorage.getItem('username');

  useEffect(() => {
    api.get('leaderboard/')
      .then((r) => setRows(r.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted center">Loading...</p>;

  const medal = (i) => ['🥇', '🥈', '🥉'][i] || i + 1;

  return (
    <div className="card">
      <h2>Top Players</h2>
      {rows.length === 0 ? (
        <p className="muted">No attempts yet. Be the first to play!</p>
      ) : (
        <table>
          <thead><tr><th>Rank</th><th>Player</th><th>Best score</th><th>Attempts</th></tr></thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={r.user__username} className={r.user__username === me ? 'me' : ''}>
                <td>{medal(i)}</td>
                <td>{r.user__username}</td>
                <td>{r.best}</td>
                <td>{r.attempts}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
