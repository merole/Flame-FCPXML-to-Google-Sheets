function myFunction() {

  SpreadsheetApp.getActive().getActiveSheet().getRange('A10').setValue(image);
}

function myFunction() {
  let X = "D"
  let Y = 8
  let sheet = SpreadsheetApp.getActiveSheet()
  let data = sheet.getDataRange().getValues()
  let num_rows = data.length

  for (let i = Y; i <= data.length; i++) {
    let value = String(sheet.getRange(X + i).getValue())
    if (value.slice(0,7) == "/9j/4AA") {
      let base64 = value
      let image = SpreadsheetApp
        .newCellImage()
        .setSourceUrl('data:image/png;base64,'+value)
        .setAltTextDescription('Shot first frame')
        .toBuilder()
        .build()
      SpreadsheetApp.getActive().getActiveSheet().getRange(String.fromCharCode(X.charCodeAt(0) + 1)+i).setValue(image);
      Logger.log("New image at: " + String.fromCharCode(X.charCodeAt(0) + 1)+i + "From: " + value)
    }
  }
}

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  // Or DocumentApp, SlidesApp or FormApp.
  ui.createMenu('Base64 to jpg')
      .addItem('Execute', 'myFunction')
      .addSeparator()
      .addToUi();
}

function menuItem1() {
  SpreadsheetApp.getUi() // Or DocumentApp, SlidesApp or FormApp.
     .alert('You clicked the first menu item!');
}
