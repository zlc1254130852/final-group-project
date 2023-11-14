
import React from 'react';
import { View, Text, TextInput, TouchableOpacity,value, onChangeText  } from 'react-native';

export default function Field({ label, icon, inputType, keyboardType, fieldButtonLabel, fieldButtonFunction, onChangeText,value }) {
  return (
    <View style={styles.inputValue}>
      {icon}
      <TextInput
        placeholder={label}
        keyboardType={keyboardType}
        style={{ flex: 1, paddingVertical: 0 }}
        secureTextEntry={inputType === 'password'}
        value={value}  // Pass the 'value' prop to TextInput
        onChangeText={onChangeText} 
       
        
        
      />
      <TouchableOpacity onPress={fieldButtonFunction}>
        <Text style={{ color: '#AD40AF', fontWeight: '700' }}>{fieldButtonLabel}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = {
  inputValue: {
    flexDirection: 'row',
    borderBottomColor: '#ccc',
    borderBottomWidth: 1,
    paddingBottom: 8,
    marginBottom: 25,
  },
};
