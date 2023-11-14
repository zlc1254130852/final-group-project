import { Text,TouchableOpacity } from 'react-native'
import React from 'react'


export default function CustomButton({label,onPress}) {
  return (
    <TouchableOpacity onPress={onPress} style ={{backgroundColor:'#AD40AF',padding:20,borderRadius:10,marginBottom:30}}>
        <Text style={styles.loginText1}>
        {label}
        </Text>
      </TouchableOpacity>
  )
}


const styles = {
 
    loginText1: {
      textAlign: 'center',
      fontWeight: '700',
      fontSize: 16,
      color: '#fff',
      paddingHorizontal: 25,
    }
    // Add any other styles you need here
  };
 


