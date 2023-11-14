import { StyleSheet } from "react-native";

import { FONT, SIZES, COLORS } from "../../../constants";

const styles = StyleSheet.create({
  // container: {
  //   marginTop: SIZES.xLarge,
  // },
  container: {
    flex: 1,
    flexDirection: 'row',
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  headerTitle: {
    fontSize: SIZES.large,
    fontFamily: FONT.medium,
    color: COLORS.primary,
  },
  headerBtn: {
    fontSize: SIZES.medium,
    fontFamily: FONT.medium,
    color: COLORS.gray,
    margin: 10,  
  },
  cardsContainer: {
    marginTop: SIZES.medium,
    marginBottom: SIZES.medium
    
  },

  // ====================================
  featureButton:{
    width: "50%",
    height: "6%",
    borderColor: COLORS.gray ,
    backgroundColor: COLORS.white,
    paddingHorizontal: SIZES.xSmall,
    borderWidth: 3,
    borderRadius: SIZES.xSmall,
    justifyContent: "center",
    margin:10,
    marginLeft: "30%",
  },
  searchBtn: {
    width: 25,
    height: "100%",
    backgroundColor: COLORS.tertiary,
    borderRadius: SIZES.medium,
    justifyContent: "center",
    alignItems: "Right",
  },
  image: {
    flex: 1,
    justifyContent: 'center',
  },
  text: {
    color: 'white',
    fontSize: SIZES.large,
    lineHeight: SIZES.xLarge,
    fontWeight: 'bold',
    textAlign: 'center',
    marginRight: "20%",
    marginLeft: "30%",
    backgroundColor: '#000000c0',
    margin:"0.5%"
  },


});

export default styles;
