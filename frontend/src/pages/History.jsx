import { useEffect, useState } from 'react';
import api from '../api';

export default function History() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('history/')
      .then((r) => setRows(r.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted center">Loading...</p>;

  return (
    <div className="card">
      <h2>My attempts</h2>
      {rows.length === 0 ? (
        <p className="muted">You haven't played yet.</p>
      ) : (
        <table>
          <thead><tr><th>Category</th><th>Score</th><th>Date</th></tr></thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                <td>{r.category__name}</td>
                <td>{r.score} / {r.total}</td>
                <td>{new Date(r.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
