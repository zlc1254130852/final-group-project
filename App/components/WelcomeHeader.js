import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import React, { useState } from 'react';
import { auth } from '../../firebase';
import { useNavigation } from '@react-navigation/core';

export default function WelcomeHeader() {
  const navigation = useNavigation();
  const username = auth.currentUser?.email.split('@')[0];
  const [showSignOutButton, setShowSignOutButton] = useState(false);

  const handleSignOut = () => {
    auth
      .signOut()
      .then(() => {
        navigation.replace('Login');
      })
      .catch(error => alert(error.message));
  };

  const toggleSignOutButton = () => {
    setShowSignOutButton(!showSignOutButton);
  };

  return (
    <View style={styles.container}>
      <View>
        <Text style={{ fontSize: 20, fontWeight: 'bold' }}>Hi, {username}</Text>
      </View>
      <TouchableOpacity onPress={toggleSignOutButton} style={styles.profileContainer}>
        <Image
          source={require('../../App/Assets/Images/profile.png')}
          style={{ width: 40, height: 40, borderRadius: 100 }}
        />
        {showSignOutButton && (
          <TouchableOpacity onPress={handleSignOut} style={styles.button}>
            <Text style={styles.buttonText}>Sign out</Text>
          </TouchableOpacity>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  button: {
    backgroundColor: '#0782F9',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: '700',
    fontSize: 16,
  },
});


















// import { StyleSheet, Text, View,Image,TouchableOpacity} from 'react-native'
// import React from 'react'
// import { auth } from '../../firebase'
// import { useNavigation } from '@react-navigation/core'


// export default function WelcomeHeader() {

//   const navigation = useNavigation()

//   const username = auth.currentUser?.email.split('@')[0];

//   const handleSignOut = () => {
//     auth
//       .signOut()
//       .then(() => {
//         navigation.replace("Login")
        
//       })
//       .catch(error => alert(error.message))
//   }

//   return (
//     <View style={styles.container}>
//     <View>
//       <Text  style={{fontSize:20,fontWeight:'bold'}}>Hi, {username}</Text>
//       </View>
//       <Image
//         source={require('../../App/Assets/Images/profile.png')}
//         style={{width:40,height:40,borderRadius:100}}
//       />
      
      
//    <TouchableOpacity onPress={handleSignOut} style={styles.button}>
//     <Text style={styles.buttonText}>Sign out</Text>
//   </TouchableOpacity> 


//     </View>
   

//   )
// }

// const styles = StyleSheet.create({
//         container:{
//             display:'flex',
//             flexDirection:'row',
//             justifyContent:'space-between',
//             alignItems:'center',

            
//         },
//         button: {
//             backgroundColor: '#0782F9',
//             width:100, // Make the button take full width
//             padding: 15,
//             borderRadius: 10,
//             alignItems: 'center',
//           },
//           buttonText: {
//             color: 'white',
//             fontWeight: '700',
//             fontSize: 16,
//           },
// })
