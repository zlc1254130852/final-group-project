import { StyleSheet, Text, View,ScrollView} from 'react-native'
import React from 'react'
import WelcomeHeader from '../components/WelcomeHeader'
import SearchBar from '../components/SearchBar'
import Slider from '../components/Slider';


export default function Home() {

  return (
    <ScrollView style={{padding:20}}>
     <WelcomeHeader/>
     <SearchBar/>    
     <Slider />
    
  </ScrollView> 
  
);
}

