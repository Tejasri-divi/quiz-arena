from django.contrib import admin
from .models import Category, Question, QuizAttempt


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'difficulty', 'correct')
    list_filter = ('category', 'difficulty')
    search_fields = ('text',)


admin.site.register(Category)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score', 'total', 'created_at')
    list_filter = ('category',)
