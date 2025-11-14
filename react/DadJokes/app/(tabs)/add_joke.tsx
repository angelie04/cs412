// file: add_joke.tsx
// Angelie Darbouze (angelie@bu.edu)
// Description: Add Joke screen for the Dad Jokes app 
import { styles } from '../../assets/my_styles';
import { useState, useEffect } from 'react';
import { Text, View } from '@/components/Themed';
import { Button, TextInput } from 'react-native';

const API_JOKES_URL = 'https://cs-webapps.bu.edu/angelie/dadjokes/api/jokes/';

export default function add_joke() {
  const [text, setText] = useState('');
  const [contributor, setContributor] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function submitJoke() {

    const payload = { text: text.trim(), contributor: contributor.trim() };
    // Debug logging, kept it in
    console.log('POST ->', API_JOKES_URL, 'payload:', payload);

    try {
      setSubmitting(true);
      const response = await fetch(API_JOKES_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      // kept console log in for debugging
      console.log('Response:', data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setSubmitting(false);
    }
  }
  return (
    <>
      <View style={styles.container}>
        <Text style={styles.title}>Add Joke:</Text>

        {/* Joke Text */}
        <Text style={{ marginTop: 12 }}>Type Joke Here</Text>
        <TextInput
          value={text}
          onChangeText={setText}
          placeholder="Type your joke here..."
          multiline
          numberOfLines={4}
          style={styles.textstyle}
        />

        {/* Contributor Name */}
        <Text style={{ marginTop: 12 }}>Contributor</Text>
        <TextInput
          value={contributor}
          onChangeText={setContributor}
          placeholder="Your name..."
          style={styles.textstyle}
        />

        {/* Submit Button */}
        <Button
          onPress={submitJoke}
          title={submitting ? "Posting..." : "Submit Joke"}
          disabled={submitting}
        />
      </View>
    </>
  );
}

