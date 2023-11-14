import React from 'react'
import { View, TextInput, TouchableOpacity, Button, ImageBackground } from 'react-native'

import styles from './textbox.style'
const image = {uri: 'https://d1t11jpd823i7r.cloudfront.net/roleplay/thumbnail-elsa-ai.png'};

const Textbox = ({navigation}) => {
  return (
    <>
      <TextInput style={styles.searchInput} multiline
        numberOfLines={10} // Set the number of lines you want to display initially
        placeholder="Type here..."
      />
      
      <TouchableOpacity style={styles.featureButton}>
        <Button title='Submit' /> 
      </TouchableOpacity>

    </>
  )
}

export default Textbox