import { actionType } from '../utils/action'
function execSwitch(state, action) {
	console.log(`Action: ${action.type}`)
	switch (action.type) {
	case actionType.SET.USER:
		return {
			...state,
			user: action.payload
		}
	case actionType.SET.CLEAR:
		return {
			...state,
			user: action.payload,
			splash: true
		}
	case actionType.SET.SPLASH:
		return {
			...state,
			splash: action.payload
		}
	case actionType.SET.isFreshing:
		return {
			...state,
			isFreshing:action.payload
		}
	case actionType.SET.isSync:
		return {
			...state,
			isSync: action.payload
		}
	case actionType.SET.useWifi:
		return {
			...state,
			useWifi:action.payload
		}
	case actionType.SET.lancode:
		return {
			...state,
			language:action.payload
		}
	case actionType.SET.dateRange:
		return {
			...state,
			dateRange:action.payload
		}
	default:
		return state
	}
}
export function authReducer(state, actions) {
	let temp = state
	if (Array.isArray(actions)) {
		actions.forEach((action) => {
			temp = execSwitch(temp, action)
		})
	} else {
		temp = execSwitch(temp, actions)
	}
	return temp
}