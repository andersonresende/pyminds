#! coding: utf-8

from model_mommy.recipe import Recipe

from .models import Review, Question


review_recipe = Recipe(Review)
question_recipe = Recipe(Question)

