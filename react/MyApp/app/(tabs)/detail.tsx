import { styles } from '../../assets/my_styles';
import { ScrollView, Image } from 'react-native';
import { Text, View } from '@/components/Themed';

export default function DetailScreen() {
  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.contentContainer}
      scrollEnabled={true}
      keyboardShouldPersistTaps="handled"
    >

      <Text style={styles.title}>Detail Screen</Text>
      <View style={styles.separator} lightColor="#e6bbd5ff" darkColor="rgba(255,255,255,0.1)" />
      <Text style={styles.textstyle}> This is the detail screen! Below are pics of some things I like to do. </Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/angelie/images/books.jpg' }}
        style={styles.pic}
      />
      <Text style={styles.textstyle}> I love to read! </Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/angelie/images/cookies.jpg' }}
        style={styles.pic}
      />
      <Text style={styles.textstyle}> I love to bake! </Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/angelie/images/netflix.jpg' }}
        style={styles.pic}
      />
      <Text style={styles.textstyle}> I enjoy relaxing and watching a movie 🍿 </Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/angelie/images/travel.jpg' }}
        style={styles.pic}
      />
      <Text style={styles.textstyle}> Lastly, I love traveling </Text>
    </ScrollView>
  );
}
