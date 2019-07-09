from django.contrib import admin
from .models import Question, Choice, Comment

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
    
class CommentInLine(admin.TabularInline):
    model = Comment

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {
            'fields': ['pub_date']
            }
        )
    ]
    inlines = [ChoiceInLine, CommentInLine]
    #NOTE: calculated fields are not sortable. There are tricks to make
    #it work by overriding get_queryset tho
    list_display = (
        'question_text',
        'pub_date',
        'was_published_recently',
        'count_comments',
        'count_comments_positive',
        'count_comments_negative'
        )
    list_filter = ['pub_date']
    search_fields = ['question_text']