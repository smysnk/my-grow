ACTION_TYPES = {
	'INIT': '@@redux/INIT'
}

"""
 * Creates a Redux store that holds the state tree.
 * The only way to change the data in the store is to call `dispatch()` on it.
 *
 * There should only be a single store in your app. To specify how different
 * parts of the state tree respond to actions, you may combine several reducers
 * into a single reducer function by using `combineReducers`.
 *
 * @param {Function} reducer A function that returns the next state tree, given
 * the current state tree and the action to handle.
 *
 * @param {any} [preloadedState] The initial state. You may optionally specify it
 * to hydrate the state from the server in universal apps, or to restore a
 * previously serialized user session.
 * If you use `combineReducers` to produce the root reducer function, this must be
 * an object with the same shape as `combineReducers` keys.
 *
 * @param {Function} enhancer The store enhancer. You may optionally specify it
 * to enhance the store with third-party capabilities such as middleware,
 * time travel, persistence, etc. The only store enhancer that ships with Redux
 * is `applyMiddleware()`.
 *
 * @returns {Store} A Redux store that lets you read the state, dispatch actions
 * and subscribe to changes.
"""
def create_store(reducer=None, preloaded_state=None, enhancer=None):
	if hasattr(preloaded_state, '__call__') and enhancer is None:
		enhancer = preloaded_state
		preloaded_state = None
	
	if enhancer is not None:
		if not hasattr(enhancer, '__call__'):
			raise Exception('Expected the enhancer to be a function')
		return enhancer(create_store)(reducer, preloaded_state)
	
	if not hasattr(reducer, '__call__'):
		raise Exception('Expected the reducer to be a function')
		
	current_reducer = reducer
	current_state = preloaded_state
	current_listeners = []
	next_listeners = current_listeners
	is_dispatching = False
	
	def ensure_can_mutate_next_listeners():
		nonlocal next_listeners, current_listeners
		if next_listeners == current_listeners:
			next_listeners = [c for c in current_listeners]
	
	"""
	 * Reads the state tree managed by the store.
	 *
	 * @returns {any} The current state tree of your application.
	"""
	def get_state():
		nonlocal current_state
		return current_state
	
	"""
	 * Adds a change listener. It will be called any time an action is dispatched,
	 * and some part of the state tree may potentially have changed. You may then
	 * call `getState()` to read the current state tree inside the callback.
	 *
	 * You may call `dispatch()` from a change listener, with the following
	 * caveats:
	 *
	 * 1. The subscriptions are snapshotted just before every `dispatch()` call.
	 * If you subscribe or unsubscribe while the listeners are being invoked, this
	 * will not have any effect on the `dispatch()` that is currently in progress.
	 * However, the next `dispatch()` call, whether nested or not, will use a more
	 * recent snapshot of the subscription list.
	 *
	 * 2. The listener should not expect to see all state changes, as the state
	 * might have been updated multiple times during a nested `dispatch()` before
	 * the listener is called. It is, however, guaranteed that all subscribers
	 * registered before the `dispatch()` started will be called with the latest
	 * state by the time it exits.
	 *
	 * @param {Function} listener A callback to be invoked on every dispatch.
	 * @returns {Function} A function to remove this change listener.
	"""
	def subscribe(listener=None):
		nonlocal next_listeners
		if not hasattr(listener, '__call__'):
			raise Exception('Expected listener to be a function')
		
		is_subscribed = True
		ensure_can_mutate_next_listeners()
		next_listeners.append(listener)
		
		def unsubscribe():
			nonlocal is_subscribed
			if not is_subscribed:
				return
			is_subscribed = False
			ensure_can_mutate_next_listeners()
			index = next_listeners.index(listener)
			del next_listeners[index]
		
		return unsubscribe
	
	"""
	 * Dispatches an action. It is the only way to trigger a state change.
	 *
	 * The `reducer` function, used to create the store, will be called with the
	 * current state tree and the given `action`. Its return value will
	 * be considered the **next** state of the tree, and the change listeners
	 * will be notified.
	 *
	 * The base implementation only supports plain object actions. If you want to
	 * dispatch a Promise, an Observable, a thunk, or something else, you need to
	 * wrap your store creating function into the corresponding middleware. For
	 * example, see the documentation for the `redux-thunk` package. Even the
	 * middleware will eventually dispatch plain object actions using this method.
	 *
	 * @param {Object} action A plain object representing what changed. It is
	 * a good idea to keep actions serializable so you can record and replay user
	 * sessions, or use the time travelling `redux-devtools`. An action must have
	 * a `type` property which may not be `undefined`. It is a good idea to use
	 * string constants for action types.
	 *
	 * @returns {Object} For convenience, the same action object you dispatched.
	 *
	 * Note that, if you use a custom middleware, it may wrap `dispatch()` to
	 * return something else (for example, a Promise you can await).
	"""
	def dispatch(action=None):
		nonlocal is_dispatching, current_state, current_listeners, next_listeners
		if action is None: 
			return action
		if type(action) == dict and action.get('type') is None:
			raise Exception('Actions must have a type')
		if is_dispatching:
			raise Exception('Reducers may not dispatch actions')
		
		try:
			is_dispatching = True
			current_state = current_reducer(current_state, action)
		finally:
			is_dispatching = False
		
		listeners = current_listeners = next_listeners
		for l in listeners:
			l()
		return action	
	
	"""
	 * Replaces the reducer currently used by the store to calculate the state.
	 *
	 * You might need this if your app implements code splitting and you want to
	 * load some of the reducers dynamically. You might also need this if you
	 * implement a hot reloading mechanism for Redux.
	 *
	 * @param {Function} nextReducer The reducer for the store to use instead.
	 * @returns {void}
	"""
	def replace_reducer(next_reducer=None):
		nonlocal current_reducer
		if not hasattr(next_reducer, '__call__'):
			raise Exception('Expected next_reducer to be a function')
		current_reducer = next_reducer
		dispatch({ 'type': ACTION_TYPES['INIT'] })
	
	# TODO: Figure out how to add the observables
	
	# When a store is created, an "INIT" action is dispatched so that every
	# reducer returns their initial state. This effectively populates
	# the initial state tree.
	dispatch({ 'type': ACTION_TYPES['INIT'] })
	
	return {
		'dispatch': dispatch,
		'subscribe': subscribe,
		'get_state': get_state,
		'replace_reducer': replace_reducer
	}