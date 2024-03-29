from django.urls import path
from . import views

app_name = 'polls'
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
#     path('<int:question_id>/comments/', views.comment, name='comments')
# ]

urlpatterns = [
    #generic views
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/comments/', views.CommentsView.as_view(), name='comments'),
    #non-generic views
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/leave_comment/', views.leave_comment, name='leave_comment'),
]