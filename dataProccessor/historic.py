import pandas as pd
import numpy as np
from datetime import datetime


def date():
    
    now = datetime.now()
    month = now.month
    
    month_name = now.strftime('%B')
    
    print(month)
    print(month_name)
    
    return(month_name)
    
date()


def historic():
    
    
    
    return()