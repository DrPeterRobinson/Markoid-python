let maxIndex=0;

window.addEventListener('pywebviewready', function() {
  var container = document.getElementById('pywebview-status')
  container.innerHTML = '<i>pywebview</i> is ready'
})

$(function(){


  $("#test-open-file").click(function(){
     openFile();
  });

  // This is here so that the user receives a request for permission to access the clipboard
// when the page loads. This is required for Firefox, and is a good idea for other browsers too.
  //alert("Requesting permission to access the clipboard.");
  //navigator.clipboard.readText();
  let text="test";
  $("#table1").append(createRow(text,"item"+maxIndex));
  maxIndex++;  
  text="test2";
  $("#table1").append(createRow(text,"item"+maxIndex));
  maxIndex++;  


});

function clearData(){
  $(".item.bg-success").removeClass("bg-success");
  var summary = "";
  $("#summary").text(summary);
}

function createRow(text,id){
  var row = document.createElement("tr");
  var dataCell=document.createElement("td");
  var node=document.createElement("input");
  $(node).attr("value",text);
  $(node).attr("id",id);
  $(node).addClass("item");
  $(node).addClass("form-control");
  $(node).prop("readonly",true);
  $(dataCell).append(node);
  $(dataCell).prop("width","100%");
  $(row).append(dataCell);

  var buttonCell=document.createElement("td");
  var paraButton='<button type="button" class="btn btn-sm btn-outline-info para" data-bs-toggle="button"><i class="bi bi-paragraph"></i></button>'
  var editButton='<button type="button" class="btn btn-sm btn-outline-warning edit" data-val="'+id+'"><i class="bi bi-pencil"></i></button>'
  var addButton='<button type="button" class="btn btn-sm btn-outline-primary add"><i class="bi bi-plus"></i></button>'
  var deleteButton='<button type="button" class="btn btn-sm btn-outline-danger delete"><i class="bi bi-trash"></i></button>'
  buttonCell.innerHTML='<div class="btn-group">'+editButton+addButton+deleteButton+paraButton+'</div>';
  $(row).append(buttonCell);


  updateInteraction(row);

  return row;
}

function openFile() {
  lines = pywebview.api.openFile().then(function(lines) {
    console.log("Lines from file: "+lines);
    var table = $("#table1");
    table.empty();
    maxIndex=0;
    console.log("Lines: "+lines);
    for (var i=0;i<lines.length;i++){
        table.append(createRow(lines[i],"item"+maxIndex));
        maxIndex++;
    }
    });
}

function saveFile() {
  var items = $(".item");
  var content = "";
  var itemIndex = 0;
  var lines =[];
  items.each(function(){
      var comment = $(this).val().trim();
      lines.push(comment);
  })
  pywebview.api.saveFile(lines).then(function(){
      console.log("Saved file: "+lines);
  });
}

function copyData(){
  var summary = $("#summary").text();
  pywebview.api.copyToClipboard(summary).then(function(){
      console.log("Copied to clipboard: "+summary);
  });
 
}


function updateInteraction(row){
  $(row).find(".item").on('click',function(){
      if($(this).prop("readonly")){
          $(this).toggleClass("bg-success");
          updateSummary();
      }
  })

  $(row).find(".item").keyup(function (e){
      if (e.keyCode === 13) {
          $(this).prop('readonly',true);
          updateSummary();
          saveFile();
      }
  })

  $(row).find(".item").dblclick(function (e){
      $(this).prop('readonly',false);
  })

  $(row).find(".para").on('click',function(){
    updateSummary();
  })

  $(row).find(".edit").on('click',function(){
      var target ="#"+$(this).attr('data-val');
      if($(target).prop("readonly")){
          $(target).prop('readonly',false);
      }
      else
      {
          $(target).prop('readonly',true);
          updateSummary();
          saveFile();
      }
  })

  $(row).find(".add").on('click',function(){
      var currentRow = $(this).closest('tr');
      $(currentRow).after(createRow('Edit this text',maxIndex++));
      updateSummary();
      saveFile();
  });

  $(row).find(".delete").on('click',function(){
      $(this).off();
      var currentRow = $(this).closest('tr');
      $(currentRow).remove();
      updateSummary();
      saveFile();
      })

  updateSummary();
  //saveFile();
}

function updateSummary(){
  var items = $(".item.bg-success");
  var summary = "";
  var itemIndex = 0;
  var previousComment="";
  var addNewLine=false;
  items.each(function(){
    var paraButton = $(this).parent().next().find(".para");
    if (paraButton.hasClass("active")){ 
        // want to add a new line after this item.
        addNewLine=true;
    }

      var comment = $(this).val().trim();
      var separator = '';
      var firstChar = comment.charAt(0);
      if (firstChar == "*"){
          summary+="\n";
          comment = comment.slice(1);
      } else if (firstChar == ","){
          if (summary.endsWith(".")){
              summary=summary.slice(0,-1);
          }
      }
      else if (firstChar == firstChar.toLowerCase()){
          if (summary.endsWith(".")){
              summary=summary.slice(0,-1);
          }
          if (itemIndex>0){
              separator=" ";    
          }
      }
      else
      {
          if (!(comment.endsWith(".")||comment.endsWith("?")||comment.endsWith(","))){
              comment +=".";
          }
          if (itemIndex>0){
              separator="  ";    
          }
      }

      if (summary.endsWith("\n")){
        summary=summary+comment;
      } else {
        summary=summary+separator+comment;
      }
      if (addNewLine){
        summary=summary+'\n';
        addNewLine=false;
      }
      itemIndex++;
  })
  $("#summary").text(summary);
}

function appendToTable(text){
  $("#table1").append('<tr><td width="100%" class="item">'+text+"</td><td><button class='add'>Add</button></td></tr>");
}


function buildTable(){
  $("#table1").append("<tr><td>wibble</td></tr>");
}

$('tbody').sortable({
  update:function(event,ui){
      updateSummary();
      //saveFile(defaultfileName);
  }
});

$('#btn-copy').on('click',function(e){
  copyData();
  var jibbly = open_file();
  loadTable(jibbly);
})
$('#btn-clear').click(function(e){
  clearData();
})
$('#btn-send').on('click',function(e){
  sendData();
})

$('#btn-send-md').on('click',function(e){
  sendDataMarkDown();
})

