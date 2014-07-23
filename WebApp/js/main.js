
offline = false

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
  });

  $(".circle").on('click', '.redButton', function(){
    num = $(this).parents('.circle').attr('id').slice(6)
    if (offline) {
      disable(num);
    } else {
      disabling(num);
      requestDisable()
    }
  });

  $(".circle").on('hover', function(e) {
    if ($(e.target).hasClass("disabled") && $(e.target).hasClass("circle")) {
      $btn = $("#btn" + $(e.target).attr("id").slice(6))
      setTimeout(function() {
        $btn.addClass("disabled")
        $btn.html("Disabled")
      }, 1)
    }
  });

});

function getData(type, userName){
    $("#" + type).css("display", "block");
    $("#" + type + " h2").html(userName);
    $("#" + type + "Tiles").css("display", "none"); 
}

function requestDisable(num) {
  $.ajax({
    url: "http://127.0.0.1:5000/stop",
    type: "POST",
    data: JSON.stringify({"stopped": "true"}),
    success: function() {
      disable(num);
    },
    contentType: "application/json",
    dataType: "json"
  })
}
function disabling(num) {
  $("#btn" + num).html("Disabling..");
}

function disable(num){
  $('#btn' + num).addClass("disabled");
  $("#btn" + num).html("Disabled");
  $("#circle" + num).addClass("disabled");
}

function enable(num) {
  $('#btn' + num).removeClass("disabled");
  $("#btn" + num).html("Disable");
  $("#circle" + num).removeClass("disabled");
}

window.setInterval(function(){
  // $.ajax( {
  //   // url: "http://127.0.0.1:5000/users", 
  //   url: "jsonData.json", 
  //   success: function(data) {
  //     console.log(testData);
  //     $.each(testData, function(k,v) {
  //       $("#" + k + " .value.bpm").html(testData[k]['bpm']);
  //       $("#" + k + " .value.stress").html(testData[k]['eda']);
  //       $("#" + k + " .machine").html(testData[k]['machine']);

  //       var statusVal = testData[k]['status'];
  //       if (statusVal == "2"){ 
  //         status="red";
  //       }
  //       else if (statusVal == "1"){
  //         status="yellow";
  //       }
  //       else status="green"

  //       $("#"+ k + " .status").addClass(status);

  //     })
  //   }
  // }); 
  // $.ajax( {
  //   url: "http://127.0.0.1:5000/stop",
  //   success: function(data) {
  //     if (data=="false"){
  //       enable(4);
  //     } else if (data=="true"){
  //       disable(4);
  //     }
  //   }
  // });
}, 100);



