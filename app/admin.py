
from django.contrib import admin
from .models import Category, Question

# Category register karna
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    search_fields = ('name',)      

# Question register karna
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'correct_option', 'level')  
    list_filter = ('category', 'level') 
    search_fields = ('question',)        

