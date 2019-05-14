from .models import Company

import numpy as np
import pandas as pd
import pickle 
import surprise
from surprise import BaselineOnly



pickle_in = open('final_CF_model',"rb")
algo = pickle.load(pickle_in)


def recomend_places(user,num,companies_set):
	top = int(num)
	map_user_to_companies=[(user,i) for i in companies_set]
	predictions = [(algo.predict(pair[0],pair[1])[3],pair) for pair in map_user_to_companies]
	results = [i[1][1] for i in sorted(predictions,key=lambda tupe: tupe[0], reverse=True)[:top]]
	return results