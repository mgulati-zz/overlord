
offline = false

$(document).ready(function() {
  //$("body").css("height", window.innerHeight);
  $('.tip').tipr();

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
      if ($(this).hasClass('greenButton')) {
        enabling(num);
        requestState(num, "false");
      } else {
        disabling(num);
        requestState(num, "true")
      }
    }
  });

  $(".circle").on('hover', function(e) {
    if ($(e.target).hasClass("disabled") && $(e.target).hasClass("circle")) {
      num = $(e.target).attr("id").slice(6)
      disable(num)
    }
  });

});

function getData(type, userName){
    $("#" + type).css("display", "block");
    $("#" + type + " h2").html(userName);
    $("#" + type + "Tiles").css("display", "none"); 
}

function requestState(num, state) {
  $.ajax({
    url: "/stop",
    type: "POST",
    data: JSON.stringify({"stopped": state}),
    success: function() {
      if (state=="true") {
        disable(num);
      } else if (state=="false") {
        enable(num);
      }
    },
    contentType: "application/json",
    dataType: "json"
  })
}

function disabling(num) {
  $("#btn" + num).html("Disabling..");
}

function disable(num){
  $('#btn' + num).addClass("greenButton");
  $("#btn" + num).html("Enable");
  $("#circle" + num).addClass("disabled");
}

function enable(num) {
  $('#btn' + num).removeClass("greenButton");
  $("#btn" + num).html("Disable");
  $("#circle" + num).removeClass("disabled");
}

function enabling(num) {
  $("#btn" + num).html("Enabling..");
}

function changeStatus(el, status) {
  statuses = ["green", "yellow", "red"]
  el.addClass(status)
  statuses.map(function(item) {
    if (item != status) {
      el.removeClass(item)
    }
  })
}

window.setInterval(function(){
  $.ajax( {
    url: "/status", 
    //url: "jsonData.json", 
    success: function(data) {
      $.each(data, function(k,v) {
        $("#" + k + " .value.bpm").html(data[k]['heartbeat']);
        $("#" + k + " .value.stress").html(data[k]['state']);
        $("#" + k + " .machine").html(data[k]['machine']);

        var statusVal = data[k]['state'].toString();
        if (statusVal == "2"){ 
          status="red";
        }
        else if (statusVal == "1"){
          status="yellow";
        }
        else {
          status="green"
        }

        changeStatus($("#"+ k + " .status"), status);
        changeStatus($("#circle4"), status);

      })
    }
  }); 

  $.ajax( {
    url: "/stop",
    success: function(data) {
      if (data=="false"){
        enable(4);
      } else if (data=="true"){
        disable(4);
      }
    }
  });
}, 100);



