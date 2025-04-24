1. Download .tabular file
2. Convert .tabular file to .xlsx
3. Open .xlsx file in Excel
4. Optional: Make a copy of the worksheet you want to sort and make a new Excel
5. Make at least one, empty Excel sheet for the output
6. Search for 'Customize Ribbon' in the search bar, then click the 'Developer' box
7. Go to 'Developer' tab in excel
8. Open 'Virtual Basic'
9. Go to 'Insert' -> 'Module'
10. Copy Paste code bellow
11. Replace phrases as instructed (Make sure the sheet names of the one you're sorting and the output sheet, Make sure the search phrase is what your wanting is searching by species name, and make sure it is scanning the column with the species name if doing species search)
12. Hit run
13. This should return your starting sheet unchanged as well as the output sheet now filled with data filtered to your request. If it failed to run, try cutting the original file into 500,000 row sized sheets and running each individually.



	 	Sub SameOldSearch()
	 	Dim sourceWs As Worksheet
			Dim destinationWs As Worksheet
			Dim searchPhrase As String
			Dim sourceRange As Range
			Dim cell As Range
			Dim lastRow As Long
			Dim destRow As Long
			Dim position As Integer
			Dim mainString As String
			Dim searchString As String
	    
			' Set your source and destination worksheets
			Set sourceWs = ThisWorkbook.Sheets("Sheet1") ' Change "Sheet1" to your source sheet name
			Set destinationWs = ThisWorkbook.Sheets("Sheet2") ' Change "Sheet2" to your destination sheet name
	    
			' Set the phrase to search for
			searchPhrase = "virus" ' Change "YourPhraseHere" to the phrase you're looking for
	    
			' Find the last row with data in the source sheet
			lastRow = sourceWs.Cells(sourceWs.Rows.Count, 1).End(xlUp).Row
	    
			' Set the destination row counter
			destRow = 1
	    
			' Loop through each cell in the source column (Column Y in this case)
			For Each cell In sourceWs.Range("Y1:Y" & lastRow)  'Remplace Y with the Collumn that contains species name(or whatever you wanna search through)
	    		mainString = cell.Value
	    		position = InStr(mainString, searchPhrase)
	    		If position > 0 Then
	        		' Copy the entire row to the destination sheet
	        		cell.EntireRow.Copy Destination:=destinationWs.Rows(destRow)
	        		destRow = destRow + 1
	    		End If
			Next cell
	    
			MsgBox "Rows copied1 successfully."
		End Sub
