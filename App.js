import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import Login from './App/Pages/Login';
import Register from './App/Pages/Register';
import Home from './App/Pages/Home';
import Onboarding from './App/Pages/Onboarding';
import { useFonts } from 'expo-font';



const Stack = createNativeStackNavigator();


export default function App() {

  

  console.log('App Rendered'); 
  return (
    
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Onboarding">
       <Stack.Screen name="Onboarding" component={Onboarding} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Register" component={Register} />
        <Stack.Screen name="Home" component={Home} />

      </Stack.Navigator>
    </NavigationContainer>
    
  );
}
