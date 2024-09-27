function myFunction() {
  let X = 4
  let Y = 1
  let sheet = SpreadsheetApp.getActiveSheet()
  let data = sheet.getDataRange().getValues()
  let num_rows = data.length

  for (let i = Y; i <= data.length; i++) {
    let value = String(sheet.getRange(i, X).getValue())
    if (value.slice(0,7) == "/9j/4AA") {
      let base64 = value
      let blob = Utilities.newBlob(Utilities.base64Decode(base64), 'image/jpg', 'sample')
      Logger.log(sheet.insertImage(blob, X+1, i).setHeight(96).setWidth(196))
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
