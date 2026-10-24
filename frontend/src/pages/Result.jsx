import { Link, Navigate, useLocation } from 'react-router-dom';

export default function Result() {
  const { state } = useLocation();
  // If the page was refreshed there is no result data, go home
  if (!state) return <Navigate to="/" replace />;

  const { score, total, review } = state;
  const percent = total ? Math.round((score / total) * 100) : 0;
  const message = percent >= 80 ? '🎉 Excellent!' : percent >= 50 ? '👍 Good job!' : '💪 Keep practising!';

  return (
    <div>
      <div className="card center">
        <h2>{message}</h2>
        <h1 className="big-score">{score} / {total}</h1>
        <p className="muted">{percent}% correct</p>
        <div className="row">
          <Link to="/" className="btn-link">Play again</Link>
          <Link to="/leaderboard" className="btn-link">Leaderboard</Link>
        </div>
      </div>

      <h3>Review your answers</h3>
      {review.map((r, i) => (
        <div key={r.id} className={`card review ${r.is_correct ? 'right' : 'wrong'}`}>
          <p><b>{i + 1}. {r.text}</b></p>
          <p>
            Your answer:{' '}
            {r.chosen ? `${r.chosen.toUpperCase()}. ${r.options[r.chosen]}` : <i>Not answered (time up)</i>}
            {r.is_correct ? ' ✅' : ' ❌'}
          </p>
          {!r.is_correct && (
            <p>Correct answer: <b>{r.correct.toUpperCase()}. {r.options[r.correct]}</b></p>
          )}
        </div>
      ))}
    </div>
  );
}
