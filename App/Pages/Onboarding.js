import React, { useEffect, useState } from 'react';
import { SafeAreaView, View, Text, TouchableOpacity, Image } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { MaterialIcons } from '@expo/vector-icons';

const Onboarding = () => {
  const navigation = useNavigation();
  const [displayText, setDisplayText] = useState('');
  const onboardingText = "Unlock Your Multilingual Journey with LinguaBuddy - Speak the World, One Language at a Time!";
  
  useEffect(() => {
    const animateText = async () => {
      for (let i = 0; i <= onboardingText.length; i++) {
        setDisplayText(onboardingText.substring(0, i));
        await new Promise(resolve => setTimeout(resolve, 50)); // Adjust the timeout for typing speed
      }
    };

    animateText();
  }, []);

  return (
    <SafeAreaView
      style={{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
      }}>
      <View style={{ marginTop: 20 }}>
        <Text
          style={{
            fontFamily: 'System',
            fontWeight: 'bold',
            fontSize: 30,
            color: '#20315f',
            textAlign: 'center',
          }}>
          {displayText}
        </Text>
      </View>

      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Image
          source={require('../../App/Assets/Images/Welcome1.png')}
          style={{
            width: 400,
            height: 300,
            resizeMode: 'cover',
          }}
        />
      </View>

      <TouchableOpacity
        style={{
          backgroundColor: '#AD40AF',
          padding: 20,
          width: '90%',
          borderRadius: 10,
          marginBottom: 50,
          flexDirection: 'row',
          justifyContent: 'space-between',
        }}
        onPress={() => navigation.navigate('Login')}>
        <Text
          style={{
            color: 'white',
            fontSize: 18,
            textAlign: 'center',
            fontWeight: 'bold',
            fontFamily: 'sans-serif-medium',
          }}>
          Let's Begin
        </Text>
        <MaterialIcons name="arrow-forward-ios" size={22} color="#fff" />
      </TouchableOpacity>
    </SafeAreaView>
  );
};

export default Onboarding;
