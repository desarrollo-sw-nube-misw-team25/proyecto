from abc import ABC, abstractmethod


class BaseCommand(ABC):
  @abstractmethod
  def execute(self):
    raise NotImplementedError('')
  
  def verify_if_none_empty(self, data):
    if isinstance(data, str) and len(data) == 0:
      return True
    if data == None:
      return True
    return False