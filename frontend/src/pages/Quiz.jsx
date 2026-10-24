import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api';

const TIME_PER_QUESTION = 15; // seconds

export default function Quiz() {
  const { categoryId } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [index, setIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(TIME_PER_QUESTION);
  const [error, setError] = useState('');

  // Refs hold values that must stay up to date inside timers
  const answersRef = useRef({});
  const finishedRef = useRef(false);

  // 1. Load questions once
  useEffect(() => {
    api.get(`questions/?category=${categoryId}&limit=10`)
      .then((res) => setQuestions(res.data))
      .catch(() => setError('Could not load questions. Is the backend running?'));
  }, [categoryId]);

  // 2. Send answers to the backend (runs only once)
  const finish = useCallback(async (finalAnswers, qs) => {
    if (finishedRef.current) return;
    finishedRef.current = true;
    try {
      const res = await api.post('submit/', {
        category: Number(categoryId),
        answers: finalAnswers,
        question_ids: qs.map((q) => q.id),
      });
      navigate('/result', { state: res.data, replace: true });
    } catch {
      setError('Could not submit your answers. Please try again.');
      finishedRef.current = false;
    }
  }, [categoryId, navigate]);

  // 3. Save the answer (or skip) and go to the next question
  const advance = useCallback((chosen) => {
    if (finishedRef.current || questions.length === 0) return;
    const q = questions[index];
    if (chosen) answersRef.current = { ...answersRef.current, [q.id]: chosen };

    if (index + 1 < questions.length) {
      setIndex(index + 1);
      setTimeLeft(TIME_PER_QUESTION);
    } else {
      finish(answersRef.current, questions);
    }
  }, [index, questions, finish]);

  // 4. Countdown timer: tick every second, auto-skip at zero
  useEffect(() => {
    if (questions.length === 0 || finishedRef.current) return;
    if (timeLeft <= 0) { advance(null); return; }
    const timer = setTimeout(() => setTimeLeft((t) => t - 1), 1000);
    return () => clearTimeout(timer);
  }, [timeLeft, questions, advance]);

  if (error) return <p className="error center">{error}</p>;
  if (questions.length === 0) return <p className="muted center">Loading questions...</p>;

  const q = questions[index];
  const progress = ((index + 1) / questions.length) * 100;
  const urgent = timeLeft <= 5;

  return (
    <div className="card">
      <div className="quiz-header">
        <span>Question {index + 1} / {questions.length}</span>
        <span className={`timer ${urgent ? 'urgent' : ''}`}>⏱ {timeLeft}s</span>
      </div>
      <div className="progress"><div className="bar" style={{ width: `${progress}%` }} /></div>

      <h3 className="question">{q.text}</h3>
      <div className="options">
        {['a', 'b', 'c', 'd'].map((o) => (
          <button key={o} className="option" onClick={() => advance(o)}>
            <b>{o.toUpperCase()}.</b> {q[`option_${o}`]}
          </button>
        ))}
      </div>
      <p className="muted small">Difficulty: {q.difficulty}</p>
    </div>
  );
}
