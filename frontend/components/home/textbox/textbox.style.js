import { StyleSheet } from "react-native";

import { COLORS, FONT, SIZES } from "../../../constants";

const styles = StyleSheet.create({
  container: {
    marginTop: SIZES.xLarge,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: SIZES.small,
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
    margin: SIZES.medium,  
  },
  cardsContainer: {
    marginTop: SIZES.medium,
    gap: SIZES.small,
  },
  // ==============================================
    image: {
    flex: 1,
    justifyContent: 'center',
  },
  text: {
    color: 'white',
    fontSize: 42,
    lineHeight: 84,
    fontWeight: 'bold',
    textAlign: 'center',
    backgroundColor: '#000000c0',
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
    overflow:"scroll",   
    margin: 5,
    alignSelf: "center",
  },
  featureButton:{
    width: "50%",
    height: "8%",
    borderColor: COLORS.gray ,
    backgroundColor: COLORS.white,
    paddingHorizontal: SIZES.medium,
    borderWidth: 3,
    borderRadius: SIZES.medium,
    justifyContent: "center",
    alignSelf: "center",
    // margin:10,
    // marginLeft: 800,
  },
});

export default styles;
