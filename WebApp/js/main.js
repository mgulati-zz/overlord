
$(document).ready(function() {
  //$("body").css("height", window.innerHeight);
  $("#nav").css("height", window.innerHeight);

  $("#nav li").click(function(){
    var id = $(this).attr("id");
    $("li").removeClass("selected");
    $(this).addClass("selected"); 
    $(".content").css("display", "none");
    $("#" + id + "Content").css("display", "block");

    $(".specific").css("display", "none");
    $(".tiles").css("display", "block");

  })

  $(".circle").on('click', '.redButton', function(){
    disable($(this).parents('.circle').attr('id').slice(6));
  })

});

function getData(type, userName){
    $("#" + type).css("display", "block");
    $("#" + type + " h2").html(userName);
    $("#" + type + "Tiles").css("display", "none"); 
}

function disable(num){
  $('#btn' + num).addClass("disabled");
  $("#circle" + num).addClass("disabled");
}

window.setInterval(function(){
  $.ajax( {
    // url: "http://127.0.0.1:5000/users", 
    url: "jsonData.js", 
    success: function(data) {
      console.log(testData);
      $.each(testData, function(k,v) {
        $("#" + k + " .value.bpm").html(testData[k]['bpm']);
        $("#" + k + " .value.stress").html(testData[k]['eda']);
        $("#" + k + " .machine").html(testData[k]['machine']);

        var statusVal = testData[k]['status'];
        if (statusVal == "2"){ 
          status="red";
        }
        else if (statusVal == "1"){
          status="yellow";
        }
        else status="green"

        $("#"+ k + " .status").addClass(status);

      })
    }
  }); 
}, 1000);



