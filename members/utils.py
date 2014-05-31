# -*- coding: utf8 -*-
import  datetime

def generate_initial_number_by_year(type):
    year=datetime.date.today().year
    return year*1000000+type*100000