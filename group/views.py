# views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Groups

class GroupListView(ListView):
    model = Groups
    template_name = 'teacher/group/group_list.html'  # The template for rendering the group list
    context_object_name = 'groups'  # The variable name to access the list of groups in the template

class GroupDetailView(DetailView):
    model = Groups
    template_name = 'teacher/group/group_detail.html'  # The template for rendering the group detail
    context_object_name = 'group'  # The variable name to access the group object in the template
