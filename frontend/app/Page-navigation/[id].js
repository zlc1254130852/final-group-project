import {View, Text} from 'react-native'
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Tesst  from "../../components/home/tesst/Tesst"
import Textbox  from "../../components/home/textbox/Textbox"
import Myprogress  from "../../components/home/myprogress/Myprogress"
import Welcome from "../../components/home/welcome/Welcome"

const HomeNavigation = () => {

  const Stack = createNativeStackNavigator();
  

  return (
  
    <Stack.Navigator screenOptions={false}>
      <Stack.Screen name='Home' component={Welcome}></Stack.Screen>
      <Stack.Screen name='Text Box' component={Textbox} ></Stack.Screen>   
      <Stack.Screen name='My Progress' component={Myprogress} ></Stack.Screen>
      
      <Stack.Screen name='Test Page' component={Tesst} ></Stack.Screen>
    </Stack.Navigator>

  
  )
}

export default HomeNavigation