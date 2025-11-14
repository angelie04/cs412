import { styles } from '../../assets/my_styles';

import { Text, View } from '@/components/Themed';
import { Image } from 'react-native';

const logoImg = require('../../assets/images/favicon.png');

export default function AboutScreen() {
  return (
    <View style={styles.contentContainer}>
      <Text style={styles.title}>About This App</Text>
      <View style={styles.separator} lightColor="#e6bbd5ff" darkColor="rgba(255,255,255,0.1)" />
      <Text style={styles.textstyle}>
        This is the about page for the React Native App I have created.
        I have now successfully created three react native tabs and inputed
        different content for each one. For this page, it will display some text and an extra image.
      </Text>
      <Image source={logoImg} style={styles.pic} />
    </View>
  );
}
