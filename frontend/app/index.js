
import { useState } from "react";
import { View, ScrollView, SafeAreaView, TouchableOpacity } from "react-native";
import { Stack, useNavigation, useRouter } from "expo-router";

import { COLORS, icons, images, SIZES } from '../constants'
import { ScreenHeaderBtn } from "../components";
// import { Textbox, Myprogress, ScreenHeaderBtn, Welcome } from "../components";
import { NavigationContainer } from "@react-navigation/native";
import HomeNavigation from "./Page-navigation/[id]";




const Home = () =>{
    const router = useRouter()

    
    return(
        <>
        <SafeAreaView style={{ flex:1, backgroundColor: COLORS.lightWhite }}>
            <Stack.Screen 
                options={{
                    headerStyle: { backgroundColor: COLORS.lightWhite },
                    headerShadowVisible: false,
                    headerLeft: ()=> ( 
                        <ScreenHeaderBtn iconUrl={icons.menu} dimension = "60%" />
                    ),
                    headerRight: ()=> (
                        <ScreenHeaderBtn iconUrl={images.profile} dimension = "100%" />
                        ),
                        headerTitle: ""
                }}
            />

            <NavigationContainer independent={true} >
                <HomeNavigation />
            </NavigationContainer>
        </SafeAreaView>


        </>
    )
}

export default Home;