import { View, Text ,StyleSheet } from 'react-native'
import React from 'react'
import { Ionicons } from '@expo/vector-icons'; 
import { TextInput } from 'react-native';

export default function SearchBar() {
  return (
    <View style={styles.container}>
    <Ionicons name="search" size={24} 
    color="#979191" style={{marginRight:10}} /> 
    <TextInput placeholder='Search' />
</View>

  )
}

const styles = StyleSheet.create({
    container:{
        display:'flex',
        flexDirection:'row',
        backgroundColor:'#fff',
        padding:10,
    borderRadius:10,
    elevation:2,
    marginTop:10,
    marginBottom: 15,
    alignItems:'center'
    }
})
