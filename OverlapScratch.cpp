// OverlapScratch.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started:
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
// Lab-July-1-2024.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <vector>
#include <string>#include <stdio.h>
#include <stdio.h>
// #include <pthread.h>
#include <iostream>
#include <algorithm>
#include <utility>
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <assert.h>
#include <string>
#include <fstream>
using namespace std;
// static int Contig(int* a, int* b);
static string Contig(string apple[], int n);

void main()
{
    ifstream inStream;
    ofstream myFile;
    int data;
    string filename;
    string filename2;
    string comFile;
    string outFile;
    string tarray[10000];
    string sendup[1000];
    int sendInt = 0;
    int tarrayTest[10000];
    int tarraySize = 0;
    string FullArray[1000];
    string LengthArray[1000];
    string LabelArray[1000];
    int total;

    // setup
    cout << "Enter filename to be sorted:";
    cin >> filename;
    // cout << "Enter filename containg FASTA numbers to be collected:";
    // cin >> filename2;
    cout << "Enter filename to place collected info:";
    cin >> outFile;
    // cout << "Enter filename to place combined info:";
    // cin >> comFile;

    cout << filename + "\n";
    cout << filename2 + "\n";
    // setup
    // open Trinity numbers
    // inStream.open((char*)filename2.c_str());
    // bool valid_file_2 = inStream.good();

    // terminates program if file isn't good

    // starts moving numbers
    int i = 0;
    // while (!inStream.eof()) {
    //     getline(inStream, tarray[i]);
    //    i++;
    //    tarraySize++;
    //}

    // cout << tarray[2];
    // inStream.close();

    // cout << filename2 + "\n"; // remove later
    // cout << filename2 + "\n";
    // open stream for full file
    inStream.open((char *)filename.c_str());
    bool valid_file_1 = inStream.good();

    // terminates program if file isn't good
    if (!valid_file_1)
    {
        cout << "Error: Invalid filename\n";
        cout << endl;
        assert(inStream.good()); // geeksforgeeks
    }
    for (int p = 0; p < 10000; p++)
    {
        tarrayTest[p] = 0;
    }
    // create arrays for total data
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

    // outFile = "Testy.txt";
    myFile.open(outFile);
    // myFile << "Writing this to a file.\n";

    while (!inStream.eof())
    {
        while (LabelArrayInt < 1000 && !inStream.eof())
        {
            cout << "H";
            TempString = ""; // reset TempString at start
            inStream.get(ch);
            // cout << "loop1\n";
            if (ch == al)
            {
                inStream.get(ch);
            }
            // get accention number and add to label array
            while (ch != ' ')
            {
                TempString = TempString + ch;
                inStream.get(ch);
            }
            LabelArray[LabelArrayInt] = TempString;
            // LabelArrayInt++;
            TempString = "";
            cout << "k";
            inStream.get(ch);
            if (1 == 1)
            { // save or remove extra data
                while (!((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C')))
                {

                    TempString = TempString + ch;
                    inStream.get(ch);
                }
                LengthArray[LabelArrayInt] = TempString;
                TempString = "";
            }

            TempString = "";
            // inStream.get(ch);
            // cout << "loop3\n";
            while ((ch != al) && (!inStream.eof()))
            {
                // inStream.get(ch);
                if ((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C'))
                {
                    TempString = TempString + ch;
                }
                inStream.get(ch);
            }
            FullArray[LabelArrayInt] = TempString;
            LabelArrayInt++;
            cout << "l";
        }
        if (0 == 1)
        {
            for (int i = 0; i <= tarraySize; i++)
            {
                for (int j = 0; j <= LabelArrayInt; j++)
                {
                    if (tarray[i] == LabelArray[j])
                    {
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
        }

        // contig combine zone
        if (1 == 0)
        {
            for (int i = 0; i <= tarraySize; i++)
            {
                cout << 'i';
                for (int j = 0; j <= LabelArrayInt; j++)
                {
                    if (tarray[i] == LabelArray[j])
                    {
                        sendup[sendInt] = FullArray[j];
                        sendup[sendInt + 1] = LabelArray[j];
                        sendInt++;
                        cout << "hit\n";
                    }
                }
                if (sendInt >= 1)
                {
                    myFile << ">" + sendup[sendInt];

                    myFile << Contig(sendup, sendInt - 1) + "\n";
                }
                else if (sendInt == 1)
                {
                    myFile << ">" + sendup[sendInt];
                    myFile << sendup[sendInt - 1];
                }
                sendInt = 0;
            }
        }
        // LabelArrayInt = 0;
    }
    cout << LabelArrayInt;
    ;
    int thinInt = 1;
    string CombArray[100];
    for (int i = 0; i <= 99; i++)
    {
        CombArray[i] = "";
    }

    for (int i = 0; i <= LabelArrayInt; i++)
    {

        CombArray[0] = FullArray[i];
        for (int j = i; j <= LabelArrayInt; j++)
        {
            if (LabelArray[i] == LabelArray[j])
            {
                CombArray[thinInt] = FullArray[j];
                thinInt++;
            }
        }
        myFile << ">" + LabelArray[i];
        string ge = Contig(CombArray, thinInt);
        myFile << ge;
    }

    std::cout << "Hello World!\n";
}

static string Contig(string apple[], int n)
{
    string fat[] = {"GTAGATCGGAAGAGCACCGTCTGAACTCCAGTCACAACCTACGATCTCGtatgccgtcatc",
                    "tatgccgtcatcTATGCCGTCATCGTGTGtctttaa",
                    "tctttaaACTTTAAGGGGGG",
                    "GGGGGAAAAAAAAAA"};
    // std::vector<std::string> strFrag = { fat[1], fat[2], fat[3] };
    vector<string> strFrag(apple, apple + n);

    string gege = "";

    // std::vector<std::string> strFrag = fat[3];

    for (size_t repeat = 0; repeat < strFrag.size() - 1; ++repeat)
    {
        std::vector<std::string> bestMatch = {std::to_string(2), "", ""}; // overlap score (minimum value 3), otherStr index, assembled str portion
        for (size_t j = 1; j < strFrag.size(); ++j)
        {
            std::string otherStr = strFrag[j];
            for (size_t x = 0; x < otherStr.length(); ++x)
            {
                if (otherStr.substr(x) == strFrag[0].substr(0, otherStr.length() - x))
                {
                    if (otherStr.length() - x > std::stoi(bestMatch[0]))
                    {
                        bestMatch = {std::to_string(otherStr.length() - x), std::to_string(j), otherStr.substr(0, x) + strFrag[0]};
                    }
                }
                if (otherStr.substr(0, otherStr.length() - x) == strFrag[0].substr(strFrag[0].length() - otherStr.length() + x))
                {
                    if (x > std::stoi(bestMatch[0]))
                    {
                        bestMatch = {std::to_string(x), std::to_string(j), strFrag[0] + otherStr.substr(otherStr.length() - x)};
                    }
                }
            }
        }
        if (std::stoi(bestMatch[0]) > 2)
        {
            strFrag[0] = bestMatch[2];
            strFrag.erase(strFrag.begin() + std::stoi(bestMatch[1]));
        }
    }

    for (const auto &str : strFrag)
    {
        gege = gege + str;
        // std::cout << str << std::endl;
    }
    // std::cout << strFrag[0] << std::endl;

    return gege;
}
