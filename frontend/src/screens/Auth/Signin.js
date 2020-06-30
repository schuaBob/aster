import * as React from 'react'
import { Text, View } from 'react-native'
import { AuthContext } from '../../contexts/AuthContext'
import { GoogleSigninButton} from '@react-native-community/google-signin'
export function SigninScreen(props) {
    const { auth } = React.useContext(AuthContext)
    let _signIn = async ()=>{
        await auth.signIn((token) =>{
            if(token) {
                console.log("Hello Token")
                props.navigation.replace('Pages')
            }
        })
    }
    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text>Signin Screen</Text>
            <GoogleSigninButton style={{ width: 240, height: 68 }}
                size={GoogleSigninButton.Size.Wide}
                color={GoogleSigninButton.Color.Dark}
                onPress={()=>{_signIn()}}
            />
        </View>
    )
}