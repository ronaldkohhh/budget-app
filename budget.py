class Category:

  #Constructor of this class
  def __init__(self, budget_name):
    self.ledger = []
    self.funds = 0
    self.name = budget_name
    self.total_withdrawn = 0

  #Deposit method
  def deposit(self, amount_added, description=False):
    if description == False:
      description = ''
    deposited = {'amount': amount_added, 'description': description}
    self.ledger.append(deposited)
    self.funds += amount_added

  #Withdraw method
  def withdraw(self, amount_substracted, description=False):
    if description == False:
      description = ''
    if self.check_funds(amount_substracted):
      withdrawn = {'amount': -amount_substracted, 'description': description}
      self.ledger.append(withdrawn)
      self.funds -= amount_substracted
      self.total_withdrawn += amount_substracted
      return True
    else:
      return False

  #Get the balance method
  def get_balance(self):
    return self.funds

  #Transfer method
  def transfer(self, amount_transferred, destination_budget):
    if self.check_funds(amount_transferred):

      withdrawn = {
          'amount': -amount_transferred,
          'description': 'Transfer to ' + destination_budget.name
      }
      self.ledger.append(withdrawn)
      self.funds -= amount_transferred
      self.total_withdrawn += amount_transferred

      deposited = {
          'amount': amount_transferred,
          'description': 'Transfer from ' + self.name
      }
      destination_budget.ledger.append(deposited)
      destination_budget.funds += amount_transferred
      return True
    else:
      return False

  #Check Funds method
  def check_funds(self, amount):
    return amount <= self.funds

  #Defining the way the budget is printed when called
  def __str__(self):

    # This block creates the first line. Eg: ****Food****
    half_asteriks = (30 - len(self.name)) // 2
    name_and_asteriks_line = half_asteriks * '*' + self.name + half_asteriks * '*'
    if len(name_and_asteriks_line) > 30:
      name_and_asteriks_line -= '*'
    string = name_and_asteriks_line + '\n'

    # This blocks create a string that prints the content of the ledger
    for item in self.ledger:
      formatted_description = str(item['description'][:23])
      formatted_amount = "{:.2f}".format(
          item['amount']).rjust(30 - len(formatted_description))
      item_as_string = formatted_description + formatted_amount
      string += item_as_string + '\n'

    total_formatted = 'Total: ' + "{:.2f}".format(self.funds)
    string += total_formatted

    return string


def create_spend_chart(list_of_budgets):
  #list_of_budgets = sorted(list_of_budgets, key=lambda budget: -budget.total_withdrawn) #Uncomment this line if you want to sort the list of budgets from largest withdrawal to smallest

  #Determine the total withdrawn amount
  total_withdrawn = 0
  for budget in list_of_budgets:
    for item in budget.ledger:
      if item['amount'] < 0:
        total_withdrawn += -item['amount']

  #Determine the withdrawn percent of each budget respect to all withdraws and add it to a list
  percents_list = []
  for budget in list_of_budgets:
    budget_percent = int((budget.total_withdrawn / total_withdrawn) * 10) * 10
    percents_list.append(budget_percent)

  #Create the chart

  #Create the numbers like '100|' and the proper amount of 'o' characters
  chart = 'Percentage spent by category\n'
  for number in range(100, -10, -10):
    chart += f"{number:3d}| "
    for budget_percent in percents_list:
      if budget_percent >= number:
        chart += 'o  '
      else:
        chart += '   '
    chart += '\n'

  # Create the horizontal bar
  chart += '    '
  for budget_percent in percents_list:
    if budget_percent >= 0:
      chart += '---'
  chart += '-'
  chart += '\n'

  # Create the vertical lines of budget's names
  max_len_of_budgets = 0
  for budget in list_of_budgets:
    if len(budget.name) > max_len_of_budgets:
      max_len_of_budgets = len(budget.name)

  for index in range(max_len_of_budgets):
    chart += '     '
    for budget in list_of_budgets:
      if index < len(budget.name):
        chart += budget.name[index] + '  '
      else:
        chart += '   '
    chart += '\n'
  chart = chart[:len(chart) - 1]

  return chart
