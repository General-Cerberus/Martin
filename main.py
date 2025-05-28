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

        print(f"Processing files {filename}, {filename2}, and {out_file}...")

        # Read IDs to be collected.
        tarray = [""] * 10
        tarray_size = 0

        with open(filename2, "r") as in_stream:
            i = 0
            for line in in_stream:
                tarray_size += 1
                if len(tarray) <= i:
                    # Resize tarray if necessary.
                    tarray.extend([""] * 10)
                tarray[i] = line.strip()
                i += 1

        # Initialize arrays.
        tarray_test = [0] * 10000
        full_array = [""] * 1000
        length_array = [""] * 1000
        label_array = [""] * 1000
        total = 0

        try:
            with open(filename, "r") as in_stream, open(out_file, "w") as my_file:
                content = in_stream.read()

                # Initialize variables.
                label_array_int = 0

                # Start parsing at the first '>'.
                pos = 0
                while pos < len(content) and content[pos] != ">":
                    pos += 1

                if pos >= len(content):
                    print("Invalid FASTA format: No '>' found")
                    return

                # Main parsing loop.
                while pos < len(content) and label_array_int < 1000:
                    # Skip the '>'.
                    pos += 1

                    # Parse label.
                    temp_string = ""
                    while pos < len(content) and content[pos] != " ":
                        temp_string += content[pos]
                        pos += 1
                    label_array[label_array_int] = temp_string
                    temp_string = ""

                    # Skip space.
                    if pos < len(content):
                        pos += 1

                    # Parse description/length.
                    while pos < len(content) and content[pos] not in "ATGC":
                        temp_string += content[pos]
                        pos += 1
                    length_array[label_array_int] = temp_string
                    temp_string = ""

                    # Parse sequence.
                    while pos < len(content) and content[pos] != ">":
                        if content[pos] in "ATGC":
                            temp_string += content[pos]
                        pos += 1
                    full_array[label_array_int] = temp_string

                    # Increment counter.
                    label_array_int += 1

                    # Check if we've reached the end.
                    if pos >= len(content):
                        break

                # Match and write entries.
                for i in range(tarray_size):
                    for j in range(label_array_int):
                        if tarray[i] == label_array[j]:
                            my_file.write(f">{label_array[j]}")
                            my_file.write(f" {length_array[j]}")
                            my_file.write(f"{full_array[j]}\n")
                            total += 1
                            tarray_test[i] += 1

                # Write total.
                my_file.write(f"Total Inputs:{total}")

            # Report repeats and misses.
            for i in range(tarray_size):
                if tarray_test[i] > 1:
                    print(f"\nRepeat at {i}")
                if tarray_test[i] == 0:
                    print(f"\nMiss at {i}")

        except FileNotFoundError:
            print("Error: One of the files could not be found.")
        except Exception as e:
            print(f"An error occurred: {e}")

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
    # Make a copy of the input list to modify.
    sequences = str_input.copy()

    # Continue until no more merges are possible.
    merged = True
    while merged and len(sequences) > 1:
        merged = False

        for i in range(len(sequences)):
            best_match = (2, -1, "")  # (overlap size, index, merged sequence)

            for j in range(len(sequences)):
                if i == j:  # Skip comparing sequence to itself.
                    continue

                other_str = sequences[j]
                curr_str = sequences[i]

                # Check for suffix of other matching prefix of current.
                for x in range(len(other_str)):
                    # other_str[x:] matches beginning of curr_str.
                    if other_str[x:] == curr_str[: len(other_str) - x]:
                        overlap_size = len(other_str) - x
                        if overlap_size > best_match[0]:
                            best_match = (overlap_size, j, other_str[:x] + curr_str)

                # Check for prefix of other matching suffix of current.
                for x in range(len(other_str)):
                    # other_str[:len(other_str)-x] matches end of curr_str.
                    suffix_start = len(curr_str) - (len(other_str) - x)
                    if (
                        suffix_start >= 0
                        and curr_str[suffix_start:] == other_str[: len(other_str) - x]
                    ):
                        overlap_size = len(other_str) - x
                        if overlap_size > best_match[0]:
                            best_match = (
                                overlap_size,
                                j,
                                curr_str + other_str[len(other_str) - x :],
                            )

            # If we found a good match, merge the sequences.
            if best_match[1] != -1:
                print(f"Merging sequences {i} and {best_match[1]}")
                print(f"New sequence: {best_match[2]}")

                # Replace current sequence with merged sequence.
                sequences[i] = best_match[2]

                # Remove the other sequence (adjust index if needed).
                sequences.pop(best_match[1] if best_match[1] < i else best_match[1] - 1)

                merged = True
                break

    # Return the final merged sequence (should be the only one left).
    if sequences:
        return sequences[0]
    return ""


if __name__ == "__main__":
    main()
