import { StatusBar } from 'expo-status-bar';
import { Platform, StyleSheet } from 'react-native';
import { styles } from '../assets/my_styles';
import { Text, View } from '@/components/Themed';

export default function ModalScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Modal Page</Text>
      <View style={styles.separator} lightColor="#e6bbd5ff" darkColor="rgba(255,255,255,0.1)" />
      <Text style={styles.textstyle}> This is the modal screen! Please close this modal to go back to the Index screen. </Text>
      {/* Use a light status bar on iOS to account for the black space above the modal */}
      <StatusBar style={Platform.OS === 'ios' ? 'light' : 'auto'} />
    </View>
  );
}

