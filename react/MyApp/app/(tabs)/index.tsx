import { Image, Button, Modal, } from 'react-native';
import { useState } from 'react';
import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';


const logoImg = require('../../assets/images/picofme.jpeg');

export default function IndexScreen() {
  const [isModalVisible, setIsModalVisible] = useState(false);
  return (
    <View style={styles.contentContainer}>
      <Text style={styles.title}>Index Page</Text>
      <View style={styles.separator} lightColor="#e6bbd5ff" darkColor="rgba(255,255,255,0.1)" />
      <Text style={styles.textstyle}> Hello my name is Angelie, and this is my Index page!
        A little bit about me... I love to read, bake, and spend time with my family!
        Below is a picture of me. </Text>
      <Image source={logoImg} style={styles.pic} />
    </View>
  );
}
