// file: jokes_list.tsx
// Angelie Darbouze (angelie@bu.edu)
// Description: Jokes List screen for the Dad Jokes app
import { styles } from '../../assets/my_styles';

import { Text, View } from '@/components/Themed';
import { useEffect, useState } from 'react';
import { FlatList, ActivityIndicator, TouchableOpacity } from 'react-native';

type Joke = { id: number; text: string; contributor?: string };
const API_BASE_URL = 'https://cs-webapps.bu.edu/angelie/dadjokes';

export default function jokes_list() {

  const [jokes, setJokes] = useState<Joke[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchJokes() {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE_URL}/api/jokes/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setJokes(Array.isArray(data) ? data : []);
    } catch (e: any) {
      setError(e.message || 'Failed to load jokes');
      setJokes([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchJokes();
  }, []);
  return (
    <View style={styles.contentContainer}>
      <Text style={styles.title}>Jokes</Text>

      {loading && <ActivityIndicator size="large" />}

      {/* {error && <Text style={styles.textstyle}>Error: {error}</Text>} */}

      {/* When screen is not loading and there is no error, then render ScrollView */}
      {!loading && !error && (
        <FlatList
          data={jokes}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={{ padding: 16 }}
          renderItem={({ item }) => (
            <View>
              <Text style={styles.textstyle}>{item.text}</Text>
              {item.contributor ? <Text style={styles.contributor}>— {item.contributor}</Text> : null}
            </View>
          )}
        />
      )}
    </View>
  );
}


