import React, { useState } from 'react';
import { View, Text, Image, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useNavigation } from '@react-navigation/native';
import Field from '../components/Field';
import CustomButton from '../components/CustomButton';
import DateTimePicker from '@react-native-community/datetimepicker';
import { createUserWithEmailAndPassword } from '../../firebase';
import { auth } from '../../firebase';



export default function Register() {
  const navigation = useNavigation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = () => {
    createUserWithEmailAndPassword(auth,email, password)
      .then(userCredentials => {
        const user = userCredentials.user;
        console.log('Registered with:',user.email);
        navigation.navigate('Login');
      })
      .catch(error => alert(error.message));
  };
  


  const goToLogin = () => {
    navigation.navigate('Login');
  };


  const [selectedDate, setSelectedDate] = useState(null);
  const [showDatePicker, setShowDatePicker] = useState(false);


  const onChange = (event, selected) => {
    const currentDate = selected || selectedDate;
    setShowDatePicker(false);
    setSelectedDate(currentDate);
  };


  return (
    <ScrollView showsVerticalScrollIndicator={false} style={{ paddingHorizontal: 25 }}>
      <Image source={require('../../App/Assets/Images/register.png')} style={styles.loginImage} />
      <Text style={styles.loginText}>Register</Text>


      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 30 }}>
        <TouchableOpacity onPress={() => {}} style={{ borderColor: '#ddd', borderWidth: 2, borderRadius: 10, paddingHorizontal: 30, paddingVertical: 10 }}>
          <Image source={require('../../App/Assets/Images/google.png')} style={{ height: 24, width: 24 }} />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => {}} style={{ borderColor: '#ddd', borderWidth: 2, borderRadius: 10, paddingHorizontal: 30, paddingVertical: 10 }}>
          <Image source={require('../../App/Assets/Images/facebook.png')} style={{ height: 24, width: 24 }} />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => {}} style={{ borderColor: '#ddd', borderWidth: 2, borderRadius: 10, paddingHorizontal: 30, paddingVertical: 10 }}>
          <Image source={require('../../App/Assets/Images/twitter.png')} style={{ height: 24, width: 24 }} />
        </TouchableOpacity>
      </View>


      <Text style={{ textAlign: 'center', color: '#666', marginBottom: 30 }}>Or, register with email ...</Text>


      <Field label={'Full Name'} icon={<Ionicons name="person-outline" size={20} color="#666" style={{ marginRight: 5 }} />} />
      <Field
        label={'Email ID'}
        icon={<MaterialIcons name="alternate-email" size={20} color="#666" style={{ marginRight: 5 }} />}
        keyboardType="email-address"
        value={email}
        onChangeText={text => setEmail(text)}
      />
      <Field
        label={'Password'}
        icon={<Ionicons name="ios-lock-closed-outline" size={20} color="#666" style={{ marginRight: 5 }} />}
        inputType="password"
        value={password}
        onChangeText={text => setPassword(text)}     
        
      />
      <Field
        label={'Confirm Password'}
        icon={<Ionicons name="ios-lock-closed-outline" size={20} color="#666" style={{ marginRight: 5 }} />}
        inputType="password"
      />


      <View style={{ flexDirection: 'row', borderBottomColor: '#ccc', borderBottomWidth: 1, paddingBottom: 8, marginBottom: 30 }}>
        <Ionicons name="calendar-outline" size={20} color="#666" style={{ marginRight: 5 }} />
        <TouchableOpacity onPress={() => setShowDatePicker(true)}>
          {selectedDate ? (
            <Text style={{ color: '#666', marginLeft: 5, marginTop: 5 }}>{selectedDate.toDateString()}</Text>
          ) : (
            <Text style={{ color: '#666', marginLeft: 5, marginTop: 5 }}>Date of Birth</Text>
          )}
        </TouchableOpacity>
      </View>


      {showDatePicker && (
        <DateTimePicker
          testID="dateTimePicker"
          value={selectedDate || new Date()}
          mode="date"
          is24Hour={true}
          display="default"
          onChange={onChange}
        />
      )}


     
      <CustomButton label={'Register'} onPress= {handleSignup} />


      <View style={{ flexDirection: 'row', justifyContent: 'center', marginBottom: 30 }}>
        <Text>Already registered?</Text>
        <TouchableOpacity onPress={goToLogin}>
          <Text style={{ color: '#AD40AF', fontWeight: '700' }}> Login </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}




const styles = {
  loginImage: {
    width: 280,
    height: 280,
    resizeMode: 'contain',
    alignSelf: 'center',
  },
  loginText: {
    fontFamily: 'Arial',
    fontSize: 28,
    fontWeight: '500',
    color: '#333',
    marginBottom: 30,
  },
  inputValue: {
    flexDirection: 'row',
    borderBottomColor: '#ccc',
    borderBottomWidth: 1,
    paddingBottom: 8,
    marginBottom: 25,
  },
};
