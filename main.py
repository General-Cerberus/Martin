"""
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

        //setup
        //open Trinity numbers
        inStream.open((char*)filename2.c_str());

        //starts moving numbers
        int i = 0;
        while (!inStream.eof()) {
            getline(inStream, tarray[i]);
            i++;
            tarraySize++;
        }

        inStream.close();

        //open stream for full file
        inStream.open((char*)filename.c_str());
        bool valid_file_1 = inStream.good();

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

        myFile.open(outFile);

        while (!inStream.eof()) {
            while ((!inStream.eof()) && (LabelArrayInt < 1000)) {
                TempString = ""; //reset TempString at start
                inStream.get(ch);
                if (ch == al) {
                    inStream.get(ch);
                }
                while (ch != ' ') {
                    TempString = TempString + ch;
                    inStream.get(ch);
                }
                LabelArray[LabelArrayInt] = TempString;
                TempString = "";

                inStream.get(ch);
                if (1 == 1) {   // save or remove extra data
                    while (!((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C'))) {

                        TempString = TempString + ch;
                        inStream.get(ch);
                    }
                    LengthArray[LabelArrayInt] = TempString;
                    TempString = "";
                }


                TempString = "";
                while ((ch != al) && (!inStream.eof())) {
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
            }
            LabelArrayInt = 0;
        }

        string ttital = to_string(total);
        myFile << "Total Inputs:" + ttital;

        for (int i = 0; i <= tarraySize; i++) {
            if (tarrayTest[i] > 1) {
                cout << "\nRepeat at " + to_string(i);
            }

            if (tarrayTest == 0) {
                cout << "\nMiss at " + to_string(i);
            }
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

        print(f"Processing files {filename}, {filename2}, and {out_file}…")

        tarray = []
        tarray_size = 0
        tarray_test = []
        with open(filename2, "r") as in_stream:
            tarray = in_stream.readlines()
            tarray = [line.strip() for line in tarray]
            tarray_size = len(tarray)
            tarray_test = [0] * tarray_size

        in_stream = open(filename, "r")
        
        for i in range(in_stream):
            for j in range(tarray_size):
                temp_string = ""
                
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
        print("Invalid input.")


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
