import React from 'react'
import { View, Text, TouchableOpacity, Button, ImageBackground } from 'react-native'
import { useRouter } from 'expo-router'


import styles from './myprogress.style'
const image = {uri: 'https://d1t11jpd823i7r.cloudfront.net/roleplay/thumbnail-elsa-ai.png'};

const Myprogress = ({ navigation  }) => {
  const router = useRouter()

  return (
  <>
    <ImageBackground source={image} resizeMode="stretch" style={styles.image}>

        <Text style={styles.text}>
          Activity Traking
        </Text>

        <TouchableOpacity style={styles.featureButton}>
          <Button title="Let's Check"></Button>
        </TouchableOpacity>

        <Text style={styles.text}>
          Future Tasks
        </Text>
        
        <View style={styles.featureButton}>
          <Button style={styles.headerBtn} title='Task 1' />
        </View>
        
        <View style={styles.featureButton}>
          <Button  title='Task 2' />
        </View>
        
        <View style={styles.featureButton}>
          <Button  title='Task 3' />
        </View>
   </ImageBackground>
  </>
)
}

export default Myprogress