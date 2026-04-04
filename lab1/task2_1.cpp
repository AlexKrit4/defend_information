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
    
    // Count bytes by moving to the end of the file
    file.seekg(0, ios::end);
    int filesize = file.tellg();
    
    cout << "File: " << filename << "\n";
    cout << "File size: " << filesize << " bytes\n";
    
    file.close();
    return 0;
}
