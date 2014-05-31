# -*- coding: utf8 -*-
from .models import LineItem
from rest_framework import serializers


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = ('product', 'unit_price', 'quantity')
