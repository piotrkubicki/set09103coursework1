import math

class Paginator():
  # initialise paginator
  def __init__(self, items, items_per_page, current_page):
    self.items_per_page = items_per_page
    self.pages = int(math.ceil(float(len(items)) / items_per_page))
    self.current_page = current_page
    self.items = items[items_per_page * (current_page - 1):items_per_page * current_page]

