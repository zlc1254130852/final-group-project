import React, {useEffect, useState} from 'react';
import { View, Text, Image, TextInput, TouchableOpacity } from 'react-native';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useNavigation } from '@react-navigation/native';
import CustomButton from '../components/CustomButton';
import Field from '../components/Field';
import { signInWithEmailAndPassword } from '../../firebase';
import { auth } from '../../firebase';


export default function Login() {
  const navigation = useNavigation();
   const [email, setEmail] = useState('');
   const [password, setPassword] = useState('');

   

   useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(user => {
      if (user) {
        navigation.navigate("Dashboard")
      }
     })
      return unsubscribe
   }, [])

   const handleLogin = () => {
    signInWithEmailAndPassword(auth, email, password)
      .then(userCredentials => {
        const user = userCredentials.user;
        console.log('Logged in with:', user.email);
        navigation.navigate('Dashboard');
      })
      .catch(error => alert(error.message));
  };
  

   




  const goToRegister = () => {
    navigation.navigate('Register');
  };


  return (
    <View style={{ paddingHorizontal: 25 }}>
      <Image
        source={require('../../App/Assets/Images/login.png')}
        style={styles.loginImage}
      />
      <Text style={styles.loginText}>Login</Text>


      <Field label={'Email ID'} icon={<MaterialIcons
        name="alternate-email"
        size={20}
        color="#666"
        style={{ marginRight: 5 }}
        />}
        value={email}
        onChangeText={text => setEmail(text)}
        keyboardType="email-address"
        />


        <Field label={'Password'} icon={<Ionicons
          name="ios-lock-closed-outline"
          size={20}
          color="#666"
          style={{ marginRight: 5 }}
          />}
          inputType="password"
           value={password}
          onChangeText={text => setPassword(text)}      
          fieldButtonLabel={"Forgot?"}
          fieldButtonFunction={() => {}}
          />


      <CustomButton label={"Login"} onPress={handleLogin} />


      <Text style={{ textAlign: 'center', color: '#666', marginBottom: 30 }}>Or, login with ...</Text>


      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 30 }}>
        <TouchableOpacity
          onPress={() => {}}
          style={{ borderColor: '#ddd', borderWidth: 2, borderRadius: 10, paddingHorizontal: 30, paddingVertical: 10 }}
        >
          <Image source={require('../../App/Assets/Images/google.png')} style={{ height: 24, width: 24 }} />
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => {}}
          style={{ borderColor: '#ddd', borderWidth: 2, borderRadius: 10, paddingHorizontal: 30, paddingVertical: 10 }}
        >
          <Image source={require('../../App/Assets/Images/facebook.png')} style={{ height: 24, width: 24 }} />
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => {}}
          style={{ borderColor: '#ddd', borderWidth: 2, borderRadius: 10, paddingHorizontal: 30, paddingVertical: 10 }}
        >
          <Image source={require('../../App/Assets/Images/twitter.png')} style={{ height: 24, width: 24 }} />
        </TouchableOpacity>
      </View>


      <View style={{ flexDirection: 'row', justifyContent: 'center', marginBottom: 30 }}>
        <Text>New to the app?</Text>
        <TouchableOpacity onPress={goToRegister}>
          <Text style={{ color: '#AD40AF', fontWeight: '700' }}> Register </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}


const styles = {
  loginImage: {
    width: 300,
    height: 300,
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
  loginText1: {
    textAlign: 'center',
    fontWeight: '700',
    fontSize: 16,
    color: '#fff',
    paddingHorizontal: 25,
  },
  // Add any other styles you need here
};
