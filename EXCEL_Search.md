1. Make a copy of the wroksheet you want to sort
2. Search for 'Customize Ribbon' in the search bar, then click the 'Developer' box
3. Go to 'Deloper' tab in excel
4. Open 'Virtual Basic'
5. Go to 'Insert' -> 'Module'
6. Copy Paste code bellow
7. Replace phrases as instructed
8. Hit run


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
			Set sourceWs = ThisWorkbook.Sheets("virus") ' Change "Sheet1" to your source sheet name
			Set destinationWs = ThisWorkbook.Sheets("Sheet1") ' Change "Sheet2" to your destination sheet name
	    
			' Set the phrase to search for
			searchPhrase = "virus" ' Change "YourPhraseHere" to the phrase you're looking for
	    
			' Find the last row with data in the source sheet
			lastRow = sourceWs.Cells(sourceWs.Rows.Count, 1).End(xlUp).Row
	    
			' Set the destination row counter
			destRow = 1
	    
			' Loop through each cell in the source column (Column A in this case)
			For Each cell In sourceWs.Range("Y1:Y" & lastRow)
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
