from django.urls import path
from . import views

urlpatterns = [

    # 增添新文章
    path('new_note/', views.new_note_view, name='new_note'),

    # 修改文章
    path('update_note/<int:id>', views.update_note_view, name='update_note'),

    # 删除文章
    path('delete_note/<int:id>', views.delete_note_view, name='delete_note'),

    # 查看文章
    path('note_detail/<int:id>', views.note_detail_view, name='note_detail'),
]
