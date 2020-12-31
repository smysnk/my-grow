import unittest
from lib.redux import create_store, combine_reducers
from unittest.mock import MagicMock

# print(dir(old.strobe))


def test_canCreateBasicStore():

  ADD_TODO = 'ADD_TODO'

  def todos(state=None, action={}):
    if state is None:
      state = []
    if action.get('type') == ADD_TODO:
      return list(state) + [{
        'id': id(state),
        'text': action['text']
      }]
    else:
      return state

  store = create_store(combine_reducers({
    'todos': todos
  }))

  store['dispatch'](dict(type='ADD_TODO', text='Hello'))
  print(store['get_state']().get('todos')) # ['Hello']

def test_canHandleNoneActions():

  ADD_TODO = 'ADD_TODO'

  def todos(state=None, action={}):
    if state is None:
      state = []
    if action.get('type') == ADD_TODO:
      return list(state) + [{
        'id': id(state),
        'text': action['text']
      }]
    else:
      return state

  store = create_store(combine_reducers({
    'todos': todos
  }))

  store['dispatch']()

