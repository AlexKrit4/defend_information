#include <iostream>
#include <fstream>
using namespace std;

int main(){
    string filename;
    cout << "Enter the path to the file:\n";
    cin >> filename;
    
    ifstream file(filename, ios::binary);
    if (!file) {
        cout << "Cannot open file.\n";
        return 1;
    }
    
    // Array to store frequency of each byte
    int freq[256];
    for (int i = 0; i < 256; i++) {
        freq[i] = 0;
    }
    
    // Read file and count frequencies
    char ch;
    int total = 0;
    while (file.read(&ch, 1)) {
        freq[(unsigned char)ch]++;
        total++;
    }
    
    file.close();
    
    cout << "\n=== BYTE FREQUENCY ANALYSIS ===\n";
    cout << "File: " << filename << "\n";
    cout << "Total bytes: " << total << "\n\n";
    cout << "Byte | Count | Frequency | Character\n";
    cout << "-----+-------+-----------+-----------\n";
    
    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0) {
            double percent = (double)freq[i] / total * 100.0;
            cout << i << " | " << freq[i] << " | " << percent << "% | ";
            
            // Print character representation
            if (ch >= 32 && ch < 127) {
                cout << (char)i;
            } else {
                cout << "[non-printable]";
            }
            cout << "\n";
        }
    }
    
    return 0;
}
