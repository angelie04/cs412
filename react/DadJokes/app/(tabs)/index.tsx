// file: index.tsx
// Angelie Darbouze (angelie@bu.edu)
// Description: Index screen for the Dad Jokes app
import { styles } from '../../assets/my_styles';
import { useState, useEffect } from 'react';
import { Text, View } from '@/components/Themed';
import { ScrollView, Alert, ActivityIndicator, Image, TouchableOpacity } from 'react-native';

const API_BASE_URL = 'https://cs-webapps.bu.edu/angelie/dadjokes';

type Joke = { id?: number; text: string; contributor?: string };
type Picture = { id?: number; image_url: string; contributor?: string };

export default function IndexScreen() {

  const [joke, setJoke] = useState<Joke | null>(null);
  const [picture, setPicture] = useState<Picture | null>(null);
  const [loading, setLoading] = useState(false);

  // fetches a random joke using api base url and the endpoint /api/random/
  async function fetchJoke() {
    const response = await fetch(`${API_BASE_URL}/api/random/`);
    if (!response.ok) throw new Error("Failed to fetch joke");
    return (await response.json()) as Joke;
  }

  // fetches a random picture using api base url and the endpoint /api/random_picture/
  async function fetchPicture() {
    const response = await fetch(`${API_BASE_URL}/api/random_picture/`);
    if (!response.ok) throw new Error("Failed to fetch picture");
    return (await response.json()) as Picture;
  }
  // loads both joke and picture, puts an error message if either fails
  async function loadAll() {
    try {
      setLoading(true);
      const [j, p] = await Promise.all([fetchJoke(), fetchPicture()]);
      setJoke(j);
      setPicture(p);
    } catch (err: any) {
      Alert.alert("Error", err.message || "Could not load data");
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    loadAll();
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.contentContainer}>
      <View style={styles.container}>
        {/* random joke */}
        {loading && !joke ? (
          <ActivityIndicator size="large" color="#ddc1eeff" />
        ) : joke ? (
          <>
            <Text style={styles.textstyle}>{joke.text}</Text>
            <Text style={styles.contributor}>
              {joke.contributor ? `— ${joke.contributor}` : ""}
            </Text>
          </>
        ) : (
          <Text>No joke available.</Text>
        )}
        {/* random picture  */}
        {loading && !picture ? (
          <ActivityIndicator size="large" color="#ddc1eeff" />
        ) : picture ? (
          <Image
            source={{ uri: picture.image_url }}
            style={styles.pic}
            resizeMode="cover"
          />
        ) : (
          <Text>No picture available.</Text>
        )}
        {/* refresh button */}
        <TouchableOpacity onPress={loadAll} style={styles.button}>
          <Text style={styles.buttonText}>Refresh</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}


