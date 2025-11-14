// file: mystylesq.ts
// Angelie Darbouze (angelie@bu.edu)
// Description: Defining a style sheet for all my pages to call
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
        flex: 1,
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
    pic: {
        marginTop: 20,
        width: 200,
        height: 200,
        borderRadius: 8,
        marginVertical: 12,
    },
    textstyle: {
        fontWeight: "bold",
        textAlign: "center",
        color: "#d53796ff"
    },
    contentContainer: {
        alignItems: 'center',
        justifyContent: 'flex-start',
        padding: 16,
        minHeight: '100%',
    }
});