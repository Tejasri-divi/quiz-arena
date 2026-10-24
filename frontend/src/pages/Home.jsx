import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

export default function Home() {
  const [cats, setCats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('categories/')
      .then((res) => setCats(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted center">Loading categories...</p>;

  return (
    <div>
      <h2>Choose a category</h2>
      <p className="muted">10 random questions, 15 seconds each. Good luck!</p>
      <div className="grid">
        {cats.map((c) => (
          <Link key={c.id} to={`/quiz/${c.id}`} className="card category">
            <h3>{c.name}</h3>
            <p className="muted">{c.question_count} questions</p>
            <span className="btn-link">Start quiz →</span>
          </Link>
        ))}
      </div>
      {cats.length === 0 && (
        <p className="muted">No categories yet. Add some in the Django admin or run <code>python manage.py seed</code>.</p>
      )}
    </div>
  );
}
