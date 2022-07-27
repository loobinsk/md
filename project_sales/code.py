	def get_interest_expenses(self):
		'''получить словарь с процентными расходами по кредитам'''
		credits = {}
		for count, credit in enumerate(self.credits.all()):
			interest_expenses_list = {}
			date_in = credit.date_in
			for month in range(credit.grace_period_interest,credit.tenor+1):
				date = date_in+relativedelta(months=+month)
				interest_expense=None
				if credit.calculation_type==0:
					interest_expense = (credit.sum_in_currancy-credit.sum_in_currancy/credit.tenor*month)*credit.interest_rate/100/12
				else:
					interest_expense = npf.ipmt(rate=credit.interest_rate/100/12, 
												per=credit.tenor, 
												nper=month,
												pv=credit.sum_in_currancy)

				# interest_expenses_list[str(date)]=round(interest_expense,2)
				credits[f'credit{count}'] = interest_expenses_list

		return credits
