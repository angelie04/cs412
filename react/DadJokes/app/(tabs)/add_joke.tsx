// file: add_joke.tsx
// Angelie Darbouze (angelie@bu.edu)
// Description: Add Joke screen for the Dad Jokes app 
import { styles } from '../../assets/my_styles';

import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';

export default function add_joke() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Add Joke Screen</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <EditScreenInfo path="app/(tabs)/add_joke.tsx" />
    </View>
  );
}

