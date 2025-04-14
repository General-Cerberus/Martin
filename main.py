"""
// AttemptFinal.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

static int Contig(int* a, int* b);
static string Contig(string apple[], int n);

int main()
{
        string Switcher;
        cout << "Type 'S' to scan a Assession code database or type 'O' to combine overlapping sequences:";
        cin >> Switcher;

        if (Switcher == "S") {

        ifstream inStream;
        ofstream myFile;
        int data;
        string filename;
        string filename2;
        string outFile;
        string tarray[10000];
        int tarrayTest[10000];
        int tarraySize = 0;
        string FullArray[1000];
        string LengthArray[1000];
        string LabelArray[1000];
        int total;


        //setup
        cout << "Enter filename to be sorted:";
        cin >> filename;
        cout << "Enter filename containg FASTA numbers to be collected:";
        cin >> filename2;
        cout << "Enter filename to place collected info:";
        cin >> outFile;


        cout << filename + "\n";
        cout << filename2 + "\n";
        //setup
        //open Trinity numbers
        inStream.open((char*)filename2.c_str());
        bool valid_file_2 = inStream.good();

        //terminates program if file isn't good
        if (!valid_file_2) {
            cout << "Error: Invalid filename\n";
            cout << endl;
            assert(inStream.good()); //geeksforgeeks
        }




        //starts moving numbers
        int i = 0;
        while (!inStream.eof()) {
            getline(inStream, tarray[i]);
            i++;
            tarraySize++;
        }

        //cout << tarray[2];
        inStream.close();

        //cout << filename2 + "\n"; // remove later
        //cout << filename2 + "\n";
        //open stream for full file
        inStream.open((char*)filename.c_str());
        bool valid_file_1 = inStream.good();

        //terminates program if file isn't good
        if (!valid_file_1) {
            cout << "Error: Invalid filename\n";
            cout << endl;
            assert(inStream.good()); //geeksforgeeks
        }
        for (int p = 0; p < 10000; p++) {
            tarrayTest[p] = 0;
        }
        //create arrays for total data
        string TempString = "";
        string Tester = "";
        int LabelArrayInt = 0;
        int k = 0;
        total = 0;
        char ch;
        char al;
        char ai = 'A';

        char ti = 'T';

        char gi = 'G';

        char ci = 'C';

        char wh = ' ';

        inStream.get(al); // set al equal to >

        //outFile = "Testy.txt";
        myFile.open(outFile);
        //myFile << "Writing this to a file.\n";


        while (!inStream.eof()) {
            while ((!inStream.eof()) && (LabelArrayInt < 1000)) {
                TempString = ""; //reset TempString at start
                inStream.get(ch);
                //cout << "loop1\n";
                if (ch == al) {
                    inStream.get(ch);
                }
                //cout << "loop2\n";
                while (ch != ' ') {
                    TempString = TempString + ch;
                    inStream.get(ch);
                }
                LabelArray[LabelArrayInt] = TempString;
                //LabelArrayInt++;
                TempString = "";

                inStream.get(ch);
                //turned off cause messing up
                if (1 == 1) {   // save or remove extra data
                    while (!((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C'))) {

                        TempString = TempString + ch;
                        inStream.get(ch);
                    }
                    LengthArray[LabelArrayInt] = TempString;
                    TempString = "";
                }


                TempString = "";
                //inStream.get(ch);
                //cout << "loop3\n";
                while ((ch != al) && (!inStream.eof())) {
                    //inStream.get(ch);
                    if ((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C')) {
                        TempString = TempString + ch;

                    }
                    inStream.get(ch);
                }
                FullArray[LabelArrayInt] = TempString;
                LabelArrayInt++;



            }

            for (int i = 0; i <= tarraySize; i++) {
                for (int j = 0; j <= LabelArrayInt; j++) {
                    if (tarray[i] == LabelArray[j]) {
                        cout << ">" + LabelArray[j];
                        cout << " " + LengthArray[j];
                        cout << FullArray[j] + "\n\n";
                        myFile << ">" + LabelArray[j];
                        myFile << " " + LengthArray[j];
                        myFile << FullArray[j] + "\n";
                        total++;
                        tarrayTest[i] = tarrayTest[i] + 1;



                    }

                }
                // cout << "itman\n";
            }
            LabelArrayInt = 0;
        }

        string ttital = to_string(total);
        myFile << "Total Inputs:" + ttital;
        cout << "Total Inputs : " + ttital;

        for (int i = 0; i <= tarraySize; i++) {
            if (tarrayTest[i] > 1) {
                cout << "\nRepeat at " + to_string(i);
            }

            if (tarrayTest == 0) {
                cout << "\nMiss at " + to_string(i);
            }

        }
        if (0 == 1) { //for testing purposes
            cout << "0";
            cout << LabelArray[0] + "\n";
            cout << FullArray[0] + "\n";
            cout << "1";
            cout << LabelArray[1] + "\n";
            cout << FullArray[1] + "\n";
            cout << "2";
            cout << LabelArray[2] + "\n";
            cout << FullArray[2] + "\n";
            cout << "3";
            cout << LabelArray[3] + "\n";
            cout << FullArray[3] + "\n";


            cout << "annna";
            cout << tarray[0] + "\n";
            cout << tarray[1] + "\n";
            cout << tarray[2] + "\n";
            cout << tarray[3] + "\n";
        }



        //std::cout << "Hello World!\n";



        }
        else if (Switcher == "O") {
          int click = 0;
          int sitch = 0;
          string clunk = "N";
          string pear[20];
          while (sitch == 0) {
          cout << "Insert sequence: ";
          cin >> pear[click];
          cout << "Add another?(Y/N):";
          cin >> clunk;
          click++;
          if (clunk != "Y") {
             sitch = 1;
          }
        }
         Contig(pear, click);




        }
        else {
                cout << "Invalid Input";
        }
}

static string Contig(string apple[], int n) {
    string fat[] = { "GTAGATCGGAAGAGCACCGTCTGAACTCCAGTCACAACCTACGATCTCGtatgccgtcatc",
         "tatgccgtcatcTATGCCGTCATCGTGTGtctttaa",
         "tctttaaACTTTAAGGGGGG",
     "GGGGGAAAAAAAAAA" };
    vector<string> strFrag(apple, apple + n);

    string gege = "";


    for (size_t repeat = 0; repeat < strFrag.size() - 1; ++repeat) {
        std::vector<std::string> bestMatch = { std::to_string(2), "", "" }; // overlap score (minimum value 3), otherStr index, assembled str portion
        for (size_t j = 1; j < strFrag.size(); ++j) {
            std::string otherStr = strFrag[j];
            for (size_t x = 0; x < otherStr.length(); ++x) {
                if (otherStr.substr(x) == strFrag[0].substr(0, otherStr.length() - x)) {
                    if (otherStr.length() - x > std::stoi(bestMatch[0])) {
                        bestMatch = { std::to_string(otherStr.length() - x), std::to_string(j), otherStr.substr(0, x) + strFrag[0] };
                    }
                }
                if (otherStr.substr(0, otherStr.length() - x) == strFrag[0].substr(strFrag[0].length() - otherStr.length() + x)) {
                    if (x > std::stoi(bestMatch[0])) {
                        bestMatch = { std::to_string(x), std::to_string(j), strFrag[0] + otherStr.substr(otherStr.length() - x) };
                    }
                }
            }
        }
        if (std::stoi(bestMatch[0]) > 2) {
            strFrag[0] = bestMatch[2];
            strFrag.erase(strFrag.begin() + std::stoi(bestMatch[1]));
        }
    }

    for (const auto& str : strFrag) {
        gege = gege + str;
        std::cout << str << std::endl;
    }
    std::cout << strFrag[0] << std::endl;

    return gege;
}
"""


def main():
    switcher = (
        input(
            "Type 'S' to scan an accession code database or type 'O' to combine overlapping sequences: "
        )
        .strip()
        .upper()
    )

    if switcher == "S":
        filename = input("Enter file name to be sorted: ").strip()
        filename2 = input(
            "Enter file name containing FASTA numbers to be collected: "
        ).strip()
        out_file = input("Enter file name to place collected info: ").strip()

        # Placeholder for file processing logic.
        print(f"Processing files {filename}, {filename2}, and {out_file}…")

    elif switcher == "O" or switcher == "0":
        sequences = []
        while True:
            sequence = input("Insert sequence: ").strip()
            sequences.append(sequence)
            cont = input("Add another? (Y/N): ").strip().upper()
            if cont != "Y":
                break
        contig(sequences)

    else:
        print("Invalid Input")


def contig(str_input: list[str]) -> str:
    for i in range(len(str_input) - 1):
        best_match = (2, "", "")
        for j in range(1, len(str_input)):
            other_str = str_input[j]
            for x in range(len(other_str)):
                if other_str[x:] == str_input[i][: len(other_str) - x]:
                    if len(other_str) - x > best_match[0]:
                        best_match = (
                            len(other_str) - x,
                            str(j),
                            other_str[:x] + str_input[i],
                        )
                if (
                    other_str[: len(other_str) - x]
                    == str_input[i][len(str_input[i]) - len(other_str) + x :]
                ):
                    if x > best_match[0]:
                        best_match = (
                            x,
                            str(j),
                            str_input[i] + other_str[len(other_str) - x :],
                        )
