/* 
 * AttemptFinal.cpp : This file contains the 'main' function. Program execution begins and ends there.
 * Purpose: This program is designed to take in a file of sequences and Trinity numbers, and output the sequences that match the Trinity numbers.
 *          The program can also take in a series of sequences and output the combined sequence.
 * Developed by Cale Johnson
 * Copyright 2025
 * Developed for Kathleen Martin's lab at Auburn University
 */

#include <algorithm>
#include <assert.h>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <string>
#include <utility>
#include <vector>
using namespace std;

static int fetchAndValidateFilenames(string filenameForSorting, string filenameFASTANums);
static void overlapSearch();
static string contig(string apple[], int n);

int main()
{
    string Switcher;
    cout << "Type 'S' to scan a Assession code database, or type 'O' to combine overlapping sequences:";
    cin >> Switcher;

    if (Switcher == "S")
    {
        ifstream inStream;
        ofstream myFile;
        int data;
        string filenameFASTANums;
        string filenameForSorting;
        string outFile;
        string tarray[10000];
        int tarrayTest[10000];
        int tarraySize = 0;
        string FullArray[1000];
        string LengthArray[1000];
        string LabelArray[1000];
        int total;

        // Validate filenames.
        fetchAndValidateFilenames(filenameForSorting, filenameFASTANums);

        // Open Trinity numbers.
        inStream.open((char *)filenameFASTANums.c_str());

        // Start moving numbers.
        int i = 0;
        while (!inStream.eof())
        {
            // Get numbers from file.
            getline(inStream, tarray[i]);
            i++;
            tarraySize++;
        }
        inStream.close();

        // Open stream for full file.
        inStream.open((char *)filenameForSorting.c_str());
        for (int p = 0; p < 10000; p++)
        {
            tarrayTest[p] = 0;
        }

        // Create arrays for total data.
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

        inStream.get(al); // Set al equal to >

        // Open file to write to.
        myFile.open(outFile);
        while (!inStream.eof())
        {
            while ((!inStream.eof()) && (LabelArrayInt < 1000))
            {
                TempString = ""; // Reset TempString at start.
                inStream.get(ch);
                if (ch == al)
                {
                    inStream.get(ch);
                }
                while (ch != ' ')
                {
                    TempString = TempString + ch;
                    inStream.get(ch);
                }
                LabelArray[LabelArrayInt] = TempString;
                TempString = "";

                inStream.get(ch);
                // Save or remove extra data.
                while (!((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C')))
                {

                    TempString = TempString + ch;
                    inStream.get(ch);
                }
                LengthArray[LabelArrayInt] = TempString;

                TempString = "";
                while ((ch != al) && (!inStream.eof()))
                {
                    if ((ch == 'T') || (ch == 'A') || (ch == 'G') || (ch == 'C'))
                    {
                        TempString = TempString + ch;
                    }
                    inStream.get(ch);
                }
                FullArray[LabelArrayInt] = TempString;
                LabelArrayInt++;
            }

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
            }
            LabelArrayInt = 0;
        }

        // Close files.
        inStream.close();
        myFile.close();

        string ttital = to_string(total);
        myFile << "Total Inputs: " + ttital;
        cout << "Total Inputs: " + ttital;

        for (int i = 0; i <= tarraySize; i++)
        {
            if (tarrayTest[i] > 1)
            {
                cout << "\nRepeat at " + to_string(i);
            }

            if (tarrayTest == 0)
            {
                cout << "\nMiss at " + to_string(i);
            }
        }
    }
    else if (Switcher == "O")
    {
        overlapSearch();
    }
    else
    {
        cout << "Invalid input.";
    }
}

static int fetchAndValidateFilenames(string filenameForSorting, string filenameFASTANums)
{
    // Get file names from user.
    cout << "Enter filename to be sorted: ";
    cin >> filenameForSorting;
    cout << "Enter filename containg FASTA numbers to be collected: ";
    cin >> filenameFASTANums;
    cout << "Enter filename to place collected info: ";
    cin >> outFile;

    // Open Trinity numbers.
    inStream.open((char *)filenameFASTANums.c_str());

    // Terminates program if file is invalid.
    if (!inStream.good())
    {
        cout << "Error: Invalid filename.\n";
        cout << endl;
        assert(inStream.good());
    }

    // Close file.
    inStream.close();

    // Open file to be sorted.
    inStream.open((char *)filenameForSorting.c_str());

    // Terminate program if file is invalid.
    if (!inStream.good())
    {
        cout << "Error: Invalid filename.\n";
        cout << endl;
        assert(inStream.good());
    }

    return 0;
}

static void overlapSearch()
{
    int click = 0, sitch = 0;
    string clunk = "N";
    string pear[20];
    while (sitch == 0)
    {
        cout << "Insert sequence: ";
        cin >> pear[click];
        cout << "Add another? (Y/N): ";
        cin >> clunk;
        click++;
        if (clunk != "Y")
        {
            sitch = 1;
        }
    }
    contig(pear, click);
}

static string contig(string apple[], int n)
{
    string fat[] = {"GTAGATCGGAAGAGCACCGTCTGAACTCCAGTCACAACCTACGATCTCGtatgccgtcatc",
                    "tatgccgtcatcTATGCCGTCATCGTGTGtctttaa",
                    "tctttaaACTTTAAGGGGGG",
                    "GGGGGAAAAAAAAAA"};
    vector<string> strFrag(apple, apple + n);

    string gege = "";

    for (size_t repeat = 0; repeat < strFrag.size() - 1; ++repeat)
    {
        std::vector<std::string> bestMatch = {std::to_string(2), "", ""}; // Overlap score (minimum value 3), otherStr index, assembled str portion
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
        gege = +str;
        std::cout << str << std::endl;
    }
    std::cout << strFrag[0] << std::endl;

    return gege;
}
