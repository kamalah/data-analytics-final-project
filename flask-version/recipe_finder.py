# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:10:39 2021

@author: k
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ast import literal_eval
from scipy import stats

import squarify
from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords  
from gensim.parsing.preprocessing import STOPWORDS
from sklearn import preprocessing


# recipes= pd.DataFrame()
# ingredient_freq = pd.DataFrame()
# interactions = pd.DataFrame()
recipes = pd.read_csv('../data/large_data/recipes.csv')
ingredient_freq = pd.read_csv('../data/recipes/ingredient_freq.csv')
interactions = pd.read_csv('../data/large_data/RAW_interactions.csv')

# def load_dfs():
#     global recipes
#     recipes = pd.read_csv('../data/large_data/recipes.csv')
#     global ingredient_freq
#     ingredient_freq = pd.read_csv('../data/recipes/ingredient_freq.csv')
#     global interactions 
#     interactions = pd.read_csv('../data/large_data/RAW_interactions.csv')

def calc_ingredient_ratings(ingredient_list, ingredient_freq = ingredient_freq):
    #print(ingredient_list) 
    rating = 0
    for ingredient in ingredient_list:
        try:
            freq = ingredient_freq.loc[ingredient]
        except:
            freq = 0
        rating += freq
    return rating

def calc_overall_score(recipe_list, priority):
    recipe_list['rating_score'] = recipe_list['avg_rating']*recipe_list['n_ratings']
    overall_score = stats.zscore(recipe_list['minutes'])*priority['E'] + \
                recipe_list['rating_score']*priority['C'] + \
                recipe_list['ingredient_score']*100*priority['D'] + \
                stats.zscore(recipe_list['n_steps'])*priority['A'] + \
                stats.zscore(recipe_list['n_ingredients'])*priority['B'] 
    return overall_score

def get_recipes(search_phrase, recipes, priority):
    recipe_list = recipes.loc[recipes['name'].str.contains(search_phrase, case=False)].copy()
    recipe_list['ingredient_score'] = recipe_list['mod_ingredients'].apply(calc_ingredient_ratings)
    recipe_list['overall_score'] = calc_overall_score(recipe_list, priority)
    return recipe_list

def make_wordmap(recipe_list):
    fig = plt.figure()
    common_ingredients = recipe_list['mod_ingredients'].apply(literal_eval).explode().value_counts()
    squarify.plot(sizes=common_ingredients[:10], label=common_ingredients.index[:10], alpha=.5, text_kwargs={"wrap": True})
    plt.axis('off')
    fig.savefig('/images/wordmap.png')

def show_top_recipes(recipe_list):
    top_5 = recipe_list.nlargest(5, 'overall_score').copy()
    top_5['recipe_link'] = [f'https://www.food.com/recipe/{ing_id}' for ing_id in top_5['id']]
    return top_5[['name','id','overall_score','recipe_link']]

def make_wordcloud(recipe_list):
    fig = plt.figure()
    stop_words = stopwords.words('english')
    stop_words.extend(['i','ive',"i've",'didnt','them', 'little','use','added','good','great', 'think', 'taste',\
                       'recipe', 'used','made','make','still','also','baked','bake','thank','thanks','cup'])
    stop_words = STOPWORDS.union(set(stop_words))
    review_list = interactions[interactions['recipe_id'].isin(recipe_list.id)]['review']
    text = " ".join(str(review) for review in review_list)
    wordcloud = WordCloud(stopwords=stop_words, background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig.savefig('/images/wordcloud.png')

def get_priority(priorities):
    priority_key = {"Number of Steps": "A", "Number of Ingredients":"B", "Ratings":"C",\
                    "Exoticness of Ingredients":"D", "Time to Prepare":"E"}
    priority_map = {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1}
    priority = [priority_key[p] for p in priorities]
    priority_map[priority[0]] = .4
    priority_map[priority[1]] = .3
    priority_map[priority[2]] = .2
    non_priority = list(set(priority_map.keys()) - set(priority))
    for key in non_priority:
        priority_map[key] = .05
    return priority_map  
    
def get_top_5(search_phrase, priorities):
    #load_dfs()
    priority = get_priority(priorities)
    recipe_list = get_recipes(search_phrase, recipes, priority)
    make_wordcloud(recipe_list)
    make_wordmap(recipe_list)
    return show_top_recipes(recipe_list)