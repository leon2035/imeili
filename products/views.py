#coding=utf8
from django.shortcuts import render
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView)
from rest_framework import generics
from rest_framework.response import Response
from .models import ProductCategory, ProductBrand, Product
ITEMS_PER_PAGE = 10




class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'