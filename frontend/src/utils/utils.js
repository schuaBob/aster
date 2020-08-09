export function checkEmotion(eState, want) {
	let eCopy = eState
	let now = eCopy.indexOf(true)
	if(now === -1) {
		// not set yet
		eCopy[want] = true
	} else {
		// something is set
		if(now === want) {
			// unlike
			eCopy[want] = false
		} else {
			eCopy[now] = false
			eCopy[want] = true
		}
	}
	return eCopy

}