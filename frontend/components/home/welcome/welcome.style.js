import { StyleSheet } from "react-native";

import { COLORS, FONT, SIZES } from "../../../constants";
// import { SimultaneousGesture } from "react-native-gesture-handler/lib/typescript/handlers/gestures/gestureComposition";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row', 
  },
  lcontainer: {
    flex: 1, // Take 50% of the screen width
    justifyContent: 'center',
    alignItems: 'center',
  },
  rcontainer: {
    width: "5%",
    height: "100%",
    flex: 1, // Take 50% of the screen width
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: SIZES.medium,
  },
  userName: {
    fontFamily: FONT.regular,
    fontSize: SIZES.large,
    color: COLORS.secondary,
  },
  welcomeMessage: {
    fontFamily: FONT.bold,
    fontSize: SIZES.xLarge,
    color: COLORS.primary,
    marginTop: 2,
  },
  searchContainer: {
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
    marginTop: SIZES.large,
    height: 50,
  },
  searchWrapper: {
    flex: 1,
    backgroundColor: COLORS.white,
    marginRight: SIZES.small,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: SIZES.medium,
    height: "100%",
  },
  searchInput: {
    fontFamily: FONT.regular,
    marginLeft:8,
    width: "96%",
    height: "30%",
    borderColor: COLORS.gray ,
    backgroundColor: COLORS.white,
    paddingHorizontal: SIZES.medium,
    borderWidth: 3,
    borderRadius: 10,
    verticalAlign:"top",
    flexWrap: "wrap",
    overflow:"scroll"   
  },
  searchBtn: {

    width: SIZES.small,
    height: "100%",
    backgroundColor: COLORS.tertiary,
    borderRadius: SIZES.medium,
    justifyContent: "center",
    fontSize: SIZES.small,

  },
  searchBtnImage: {
    width: "50%",
    height: "50%",
    tintColor: COLORS.white,
  },
  tabsContainer: {
    width: "100%",
    marginTop: SIZES.medium,
  },
  featureButton:{
    width: "80%",
    height: "6%",
    borderColor: COLORS.gray ,
    backgroundColor: COLORS.white,
    paddingHorizontal: SIZES.xSmall,
    borderWidth: 3,
    borderRadius: SIZES.xSmall,
    justifyContent: "center",
    margin:10,
    textAlign:"center",
    marginLeft: "10%",
  },
  tab: (activeJobType, item) => ({
    paddingVertical: SIZES.small / 2,
    paddingHorizontal: SIZES.small,
    borderRadius: SIZES.medium,
    borderWidth: 1,
    borderColor: activeJobType === item ? COLORS.secondary : COLORS.gray2,
  }),
  tabText: (activeJobType, item) => ({
    fontFamily: FONT.medium,
    color: activeJobType === item ? COLORS.secondary : COLORS.gray2,
  }),


  image: {
    flex: 1,
    justifyContent: 'center',
  },
  text: {
    color: 'white',
    fontSize: SIZES.medium,
    lineHeight: SIZES.xLarge,
    fontWeight: 'bold',
    textAlign: 'center',
    backgroundColor: '#000000c0',
    margin:4
  },
});

export default styles;
