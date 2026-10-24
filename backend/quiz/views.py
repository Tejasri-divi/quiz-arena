from django.db.models import Max, Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Question, QuizAttempt
from .serializers import CategorySerializer, QuestionSerializer, RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def categories(request):
    data = CategorySerializer(Category.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def questions(request):
    category_id = request.GET.get('category')
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    qs = Question.objects.filter(category_id=category_id).order_by('?')[:limit]
    return Response(QuestionSerializer(qs, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit(request):
    """
    Body: {"category": 1, "answers": {"3": "a", "5": "c"}}
    The score is calculated here on the server, so it cannot be faked.
    """
    answers = request.data.get('answers', {})
    category_id = request.data.get('category')
    if not category_id or not isinstance(answers, dict):
        return Response({'error': 'category and answers are required'}, status=400)

    # Score every question that was served (unanswered ones simply count as wrong)
    question_ids = request.data.get('question_ids', list(answers.keys()))
    questions_qs = Question.objects.filter(id__in=question_ids, category_id=category_id)

    score = 0
    review = []
    for q in questions_qs:
        chosen = answers.get(str(q.id))
        is_correct = chosen == q.correct
        if is_correct:
            score += 1
        review.append({
            'id': q.id,
            'text': q.text,
            'chosen': chosen,
            'correct': q.correct,
            'is_correct': is_correct,
            'options': {'a': q.option_a, 'b': q.option_b, 'c': q.option_c, 'd': q.option_d},
        })

    total = questions_qs.count()
    QuizAttempt.objects.create(user=request.user, category_id=category_id, score=score, total=total)
    return Response({'score': score, 'total': total, 'review': review})


@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    rows = (QuizAttempt.objects
            .values('user__username')
            .annotate(best=Max('score'), attempts=Count('id'))
            .order_by('-best', 'user__username')[:10])
    return Response(list(rows))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    rows = (QuizAttempt.objects.filter(user=request.user)
            .order_by('-created_at')
            .values('category__name', 'score', 'total', 'created_at')[:20])
    return Response(list(rows))
