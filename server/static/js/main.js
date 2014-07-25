
OFFLINE = false

MACHINE_DISABLED = "green"
MACHINE_STOPPED = "yellow"
MACHINE_ENABLED = "red"
USER_FIT = "green"
USER_UNFIT_UNCERTAIN = "yellow"
USER_UNFIT_CERTAIN = "red"

SPECIAL_NUMBER = 4

$(document).ready(function() {
  //$("body").css("height", window.innerHeight);
  $('.tip').tipr();

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
    if (OFFLINE) {
      disable(num);
    } else if (!$(this).hasClass(MACHINE_STOPPED)) {
      if ($(this).hasClass(MACHINE_DISABLED)) {
        machine.enabling(num);
        requestState(num, "false");
      } else {
        machine.disabling(num);
        requestState(num, "true")
      }
    }
  });

  $(".circle").on('hover', function(e) {
    if ($(e.target).hasClass("circle")) {
      num = $(e.target).attr("id").slice(6)
      machine.setState(num, machine.state);
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
    success: function(data) {
      resp = machine.interpretState(data);
    },
    contentType: "application/json",
    dataType: "json"
  })
}

//User Class
function User(state) {
  this.state = state
  this.isDisabled = false
}
User.prototype = {
  showDisabled: function(num) {
    $("#circle" + num).addClass("disabled");
    this.isDisabled = true
  },
  showState: function(num) {
    $("#circle" + num).removeClass("disabled");
    this.isDisabled = false
  },
  changeState: function(num, state) {
    if (!this.isDisabled) {
      changeColour($("#circle" + num), state)
    }
    this.state = state
  }
}


function Machine(state) {
  this.state=state
}

Machine.prototype = {
  disable: function(num) {
    changeColour($('#btn' + num), MACHINE_DISABLED)
    $("#btn" + num).html("Enable");
    $("#btn" + num).removeClass("progress");
    user.showDisabled(num);
  },
  disabling: function(num) {
    $("#btn" + num).html("Disabling..");
    $("#btn" + num).addClass("progress");
  },
  enabling: function(num) {
    $("#btn" + num).html("Enabling..");
    $("#btn" + num).addClass("progress");
  },
  enable: function(num) {
    changeColour($('#btn' + num), MACHINE_ENABLED);
    $("#btn" + num).html("Disable");
    $("#btn" + num).removeClass("progress");
    user.showState(num);
  },
  manualDisable: function(num) {
    changeColour($('#btn' + num), MACHINE_STOPPED);
    $("#btn" + num).html("Stopped");
    $("#btn" + num).removeClass("progress");
    user.showDisabled(num);
  },
  setState: function(num, state) {
    this.state=state
    //console.log("Setting state to", state)
    //console.log("State set to ", this.state)
    switch(state) {
      case MACHINE_DISABLED:
        this.disable(num);
        break;
      case MACHINE_STOPPED:
        this.manualDisable(num);
        break;
      case MACHINE_ENABLED:
        this.enable(num);
        break;
    }
  },
  interpretState: function(data){
    if (data["solenoid"] == 0 && data["killswitch"] == 1) {
      this.setState(SPECIAL_NUMBER, MACHINE_STOPPED);
      return MACHINE_STOPPED
    } else if (data["solenoid"] == data["killswitch"]) {
      if (data["killswitch"]==0){
        this.setState(SPECIAL_NUMBER, MACHINE_ENABLED);
        return MACHINE_ENABLED
      } else if (data["killswitch"]==1){
        this.setState(SPECIAL_NUMBER, MACHINE_DISABLED);
        return MACHINE_DISABLED
      }
    }
  }
}

function changeColour(el, colour) {
  colours = ["green", "yellow", "red"]
  el.addClass(colour)
  colours.map(function(item) {
    if (item != colour) {
      el.removeClass(item)
    }
  });
}

var user = new User(USER_FIT);
var machine = new Machine(MACHINE_ENABLED);

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
          status=USER_UNFIT_CERTAIN;
        }
        else if (statusVal == "1"){
          status=USER_UNFIT_UNCERTAIN;
        }
        else{
          status=USER_FIT
        }
        changeColour($("#"+ k + " .status"), status);
        if (k=="adam") {
          user.changeState(SPECIAL_NUMBER, status);
        }
      })
    }
  }); 

  $.ajax( {
    url: "/stop",
    success: function(data) {
      if (!$("#btn4").hasClass("progress")) {
        machine.interpretState(data);
      }
    }
  });
}, 2000);



