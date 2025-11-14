// file: my_styles.ts
// Angelie Darbouze (angelie@bu.edu)
// Description: Defining a style sheet for all my pages to call
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    title: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    separator: {
        marginVertical: 30,
        height: 1,
        width: '80%',
    },
    textstyle: {
        fontWeight: "bold",
        textAlign: "center",
        color: "#000000ff"
    },
    contentContainer: {
        alignItems: 'center',
        justifyContent: 'flex-start',
        padding: 16,
        minHeight: '100%',
    },
    contributor: {
        fontSize: 13,
        color: "#666",
        fontStyle: "italic",
    },
    pic: {
        marginTop: 20,
        width: 200,
        height: 200,
        borderRadius: 8,
        marginVertical: 12,
    },
    button: {
        backgroundColor: "#ddc1eeff",
        paddingVertical: 12,
        paddingHorizontal: 24,
        borderRadius: 8,
    },
    buttonText: {
        color: "#0a0909ff",
        fontWeight: "600",
    },
});
