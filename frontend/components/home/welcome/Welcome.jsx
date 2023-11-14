import React from 'react'
import { View, ImageBackground, Button, Text, TouchableOpacity, TextInput, LogBox } from 'react-native'

import styles from './welcome.style'
const image = {uri: 'https://d1t11jpd823i7r.cloudfront.net/roleplay/thumbnail-elsa-ai.png'};

const Welcome = ({navigation}) => {
  return (
    <>
      <ImageBackground source={image} resizeMode="stretch" style={styles.image}>
        <View style={styles.container}>

        <View style={styles.lcontainer}>
          <Text>
            Hello World
          </Text>
        </View>
        
        <View style={styles.rcontainer} >

          <Text style={styles.text}>
            Welcome to AI English Language Learning Academy        
          </Text>
    
          <TouchableOpacity  
          style={styles.featureButton}
          >
            <Text
              style={styles.tabText} 
              // title="My Dashboard" 
              onPress = {()=> {navigation.navigate("My Progress")}}
            >My Dashboard</Text>
          </TouchableOpacity>
    
          <TouchableOpacity  style={styles.featureButton} >
            <Text style={styles.tabText} 
            // title="Let's Communicate" 
              onPress = {()=> {navigation.navigate("Text Box")}} 
            > Let's Communicate</Text>
          </TouchableOpacity>
          
          <TouchableOpacity  style={styles.featureButton} >
            <Text style={styles.tabText}  
              title='Test Screen'
              onPress = {()=> {navigation.navigate("Test Page")}} 
            > 
            Test Screen 
            </Text>
          </TouchableOpacity>
    
          </View>
        </View>
      </ImageBackground>
    
          
    </>
  )
}

export default Welcome