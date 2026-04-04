#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

int main(){
    // Read key from file
    int key[5];
    ifstream keyfile("key.txt");
    if (!keyfile) {
        cout << "Cannot open key.txt\n";
        return 1;
    }
    
    for (int i = 0; i < 5; i++) {
        keyfile >> key[i];
        // Convert to 0-based indexing
        key[i]--;
    }
    keyfile.close();
    
    int mode;
    string filename;
    
    cout << "==== Vertical Permutation Cipher ====\n";
    cout << "1 - Encryption\n";
    cout << "2 - Decryption\n";
    cout << "Select mode: ";
    cin >> mode;
    
    cout << "Enter the filename: ";
    cin >> filename;
    
    if (mode == 1) {
        // ENCRYPTION
        ifstream infile(filename, ios::binary);
        if (!infile) {
            cout << "Cannot open input file.\n";
            return 1;
        }
        
        // Read all bytes
        string content = "";
        char ch;
        while (infile.read(&ch, 1)) {
            content += ch;
        }
        infile.close();
        
        // Pad with 'z' if needed
        while (content.length() % 5 != 0) {
            content += 'z';
        }
        
        int rows = content.length() / 5;
        cout << "File size before padding: " << content.length() << " bytes\n";
        cout << "Grid: " << rows << " rows x 5 columns\n";
        
        // Create grid
        vector<vector<char>> grid(rows, vector<char>(5));
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < 5; j++) {
                grid[i][j] = content[i*5 + j];
            }
        }
        
        // Write encrypted file (reordered columns)
        ofstream outfile("encrypted.bin", ios::binary);
        if (!outfile) {
            cout << "Cannot open output file.\n";
            return 1;
        }
        
        // Read columns in order specified by key
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < 5; j++) {
                outfile.put(grid[i][key[j]]);
            }
        }
        outfile.close();
        
        cout << "Encryption completed. Output: encrypted.bin\n";
        
    } else if (mode == 2) {
        // DECRYPTION
        ifstream infile(filename, ios::binary);
        if (!infile) {
            cout << "Cannot open input file.\n";
            return 1;
        }
        
        // Read all bytes
        string content = "";
        char ch;
        while (infile.read(&ch, 1)) {
            content += ch;
        }
        infile.close();
        
        if (content.length() % 5 != 0) {
            cout << "Error: File size is not multiple of 5\n";
            return 1;
        }
        
        int rows = content.length() / 5;
        cout << "Grid: " << rows << " rows x 5 columns\n";
        
        // Create grid to hold encrypted data
        vector<vector<char>> encrypted(rows, vector<char>(5));
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < 5; j++) {
                encrypted[i][j] = content[i*5 + j];
            }
        }
        
        // Create grid for decrypted data
        vector<vector<char>> decrypted(rows, vector<char>(5));
        
        // Reverse the column reordering
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < 5; j++) {
                decrypted[i][key[j]] = encrypted[i][j];
            }
        }
        
        // Write decrypted file
        ofstream outfile("decrypted.bin", ios::binary);
        if (!outfile) {
            cout << "Cannot open output file.\n";
            return 1;
        }
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < 5; j++) {
                outfile.put(decrypted[i][j]);
            }
        }
        outfile.close();
        
        cout << "Decryption completed. Output: decrypted.bin\n";
        
    } else {
        cout << "Invalid mode.\n";
        return 1;
    }
    
    return 0;
}
