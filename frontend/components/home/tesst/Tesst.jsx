import React from 'react'
import {ImageBackground, StyleSheet} from 'react-native';
import { View, Button, Text, TouchableOpacity, TextInput, LogBox } from 'react-native'

import styles from './test.style'
const image = {uri: 'https://d1t11jpd823i7r.cloudfront.net/roleplay/thumbnail-elsa-ai.png'};

const Tesst = ({navigation}) => {
  return (
  
      <ImageBackground source={image} resizeMode="stretch" style={styles.image}>
        <Text style={styles.text}> TEST PAGE</Text>
      </ImageBackground>
  
  )
}

export default Tesst


