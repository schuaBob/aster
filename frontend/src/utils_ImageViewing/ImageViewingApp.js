import React, { useState } from "react";
import {
  Alert,
  Platform,
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from "react-native";
import get from "lodash/get";
import memoize from "lodash/memoize";

//import ImageViewing from "../src/ImageViewing";
import ImageViewing from "react-native-image-viewing";
import ImageList from "./components/ImageList";
import { ImageHeader, renderDetail } from "./components/ImageHeader";
import ImageFooter from "./components/ImageFooter";

import { architecture } from "./data/architecture";
import { travel } from "./data/travel";
import { city } from "./data/city";
import { food } from "./data/food";

// import { ImageSource } from "./@types";

export default function App() {
  const [currentImageIndex, setImageIndex] = useState(0);
  const [images, setImages] = useState(architecture);
  //const [setImages] = useState(architecture);
  const [isVisible, setIsVisible] = useState(false);

  const onSelect = (images, index) => {
    setImageIndex(index);
    setImages(images);
    setIsVisible(true);
  };

  const onRequestClose = () => setIsVisible(false);
  const getImageSource = memoize((images) =>
    images.map((image, index) =>
      typeof image.original === "number"
        ? image.original
        : { uri: image.original }
    )
  );
  // const images = [
  //   {
  //     uri: "https://images.unsplash.com/photo-1571501679680-de32f1e7aad4",
  //   },
  //   {
  //     uri: "https://images.unsplash.com/photo-1573273787173-0eb81a833b34",
  //   },
  //   {
  //     uri: "https://images.unsplash.com/photo-1569569970363-df7b6160d111",
  //   },
  // ];
  const onLongPress = (image) => {
    Alert.alert("Long Pressed", image.uri);
  };

  return (
    <SafeAreaView style={styles.root}>
      <ImageList
        images={travel.map((image) => image.thumbnail)}
        onPress={(index) => onSelect(travel, index)}
        shift={0.25}
      />
      <ImageList
        images={architecture.map((image) => image.thumbnail)}
        onPress={(index) => onSelect(architecture, index)}
        shift={0.75}
      />
      <View style={styles.about}>
        <Text style={styles.name}>[ react-native-image-viewing ]</Text>
      </View>
      <ImageViewing
        images={getImageSource(images)}
        //images={images}
        backgroundColor="transparent"
        imageIndex={currentImageIndex}
        presentationStyle="overFullScreen"
        visible={isVisible}
        onRequestClose={onRequestClose}
        onLongPress={onLongPress}
        HeaderComponent={
          images === travel
            ? ({ imageIndex }) => {
              const title = get(images, `${imageIndex}.title`);
              return (
                <ImageHeader title={title} onRequestClose={onRequestClose} />
              );
            }
            : undefined
        }
        FooterComponent={({ imageIndex }) => (
          <ImageFooter imageIndex={imageIndex} imagesCount={images.length} />
        )}
      />
      <ImageList
        images={food.map((image) => image.thumbnail)}
        onPress={(index) => onSelect(food, index)}
        shift={0.5}
      />
      <ImageList
        images={city.map((image) => image.thumbnail)}
        onPress={(index) => onSelect(city, index)}
        shift={0.75}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: "transparent",
    ...Platform.select({
      android: { paddingTop: StatusBar.currentHeight },
      default: null,
    }),
  },
  about: {
    flex: 1,
    marginTop: -12,
    alignItems: "center",
    justifyContent: "center",
  },
  name: {
    textAlign: "center",
    fontSize: 24,
    fontWeight: "200",
    color: "#FFFFFFEE",
  },
});
