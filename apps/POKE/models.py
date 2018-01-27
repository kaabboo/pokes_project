# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.db import models
from ..log_reg.models import User

class PokeManager(models.Manager):
	def poke(self, postData):
		poker = User.objects.get(id = postData['poker_id'])
		poked = User.objects.get(id = postData['poked_id'])
		self.create(poker = poker, poked = poked)
		
	def kedirs_pokes(self, id):
		kedir_in = User.objects.get(id = id)
		all_pokes = self.filter(poked = kedir_in)
		count = all_pokes.values('poker').distinct().count()
		return count
	
	def who_poked_kedir(self, id):
		kedir_in = User.objects.get(id = id)
		others = []
		pokers = self.filter(poked = kedir_in).values('poker__alias').distinct()
		for each in pokers:
			others.append(each)
		return others


class Poke(models.Model):
	poker=models.ForeignKey(User,related_name='user_poker',null=True)
	poked=models.ForeignKey(User,related_name='user_poked',null=True)
	created_at=models.DateField(auto_now_add=True)
	updated_at=models.DateField(auto_now=True)
	objects = PokeManager()
