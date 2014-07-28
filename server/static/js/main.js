
OFFLINE = false

//visual colour states
MACHINE_DISABLED = "green"
MACHINE_STOPPED = "disabled"
MACHINE_ENABLED = "red"
USER_FIT = "green"
USER_UNFIT_UNCERTAIN = "yellow"
USER_UNFIT_CERTAIN = "red"

SPECIAL_NUMBER = 4

_userReq = null;
_machineReq = null;

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

  $(".settingsTile").click(function(){
    if ($(this).hasClass("unselected")){
      $(this).removeClass("unselected");
    }
    else
      $(this).addClass("unselected");
  });

  $(".circle").on('click', '.redButton', function(){
    num = $(this).parents('.circle').attr('id').slice(6)
    if (OFFLINE) {
      disable(num);
    } else if (!$(this).hasClass(MACHINE_STOPPED) && num == SPECIAL_NUMBER) {
      if ($(this).hasClass(MACHINE_DISABLED)) {
        machine.enabling(num);
        if (num==SPECIAL_NUMBER){
          requestState(num, "false");
        }
      } else {
        machine.disabling(num);
        if (num==SPECIAL_NUMBER){
          requestState(num, "true")
        }
      }
    }
  });

  $(".circle").on('hover', function(e) {
    if ($(e.target).hasClass("circle")) {
      num = $(e.target).attr("id").slice(6)
      if (num == SPECIAL_NUMBER) machine.setState(num, machine.state);
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
      machine.progress = false;
      buttonReq();
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
  this.el = $("#bandSaw")
  this.progress = false
}

Machine.prototype = {
  disable: function(num) {
    changeColour($('#btn' + num), MACHINE_DISABLED)
    changeColour($("#bandSaw .status"), MACHINE_DISABLED);
    $("#btn" + num).html("Enable");
    this.progress = false;
    this.el.addClass("machineDisabled")
    user.showDisabled(num);
  },
  disabling: function(num) {
    $("#btn" + num).html("Disabling..");
    this.progress = true;
  },
  enabling: function(num) {
    $("#btn" + num).html("Enabling..");
    this.progress = true;
  },
  enable: function(num) {
    changeColour($('#btn' + num), MACHINE_ENABLED);
    changeColour($("#bandSaw .status"), MACHINE_ENABLED);
    $("#btn" + num).html("Disable");
    this.progress = false;
    this.el.removeClass("machineDisabled")
    user.showState(num);
  },
  manualDisable: function(num) {
    changeColour($('#btn' + num), MACHINE_STOPPED);
    changeColour($("#bandSaw .status"), MACHINE_STOPPED);
    $("#btn" + num).html("Stopped");
    this.progress = false;
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
  colours = ["green", "yellow", "red", "disabled"]
  el.addClass(colour)
  colours.map(function(item) {
    if (item != colour) {
      el.removeClass(item)
    }
  });
}

var user = new User(USER_FIT);
var machine = new Machine(MACHINE_ENABLED);

function machineNameToID(name) {
  var words = name.split(" ");
  words[0] = words[0].charAt(0).toLowerCase() + words[0].slice(1)
  words[1] = words[1].charAt(0).toUpperCase() + words[1].slice(1)
  return words.join("")
}

window.setInterval(function() {
  $.ajax( {
    url: "/status", 
    //url: "jsonData.json", 
    success: function(data) {
      $.each(data, function(k,v) {
        $("#" + k + " .value.bpm").html(data[k]['heartrate']);

        $("#" + k + " .machine").html(data[k]['machine']);
        var statusVal = data[k]['state'].toString();
        var statusName = "Normal"
        if (statusVal == "2"){ 
          status=USER_UNFIT_CERTAIN;
          statusName = "Impaired"

        }
        else if (statusVal == "1"){
          status=USER_UNFIT_UNCERTAIN;
          statusName = "Fatigued"
        }
        else{
          status=USER_FIT
        }

        $("#" + k + " .value.stress").html(statusName);

        changeColour($("#"+ k + " .status"), status);
        var circle = $(".circle." + k).attr("id").slice(6)
        user.changeState(circle, status);
      })
    }
  }); 
}, 2000);


function buttonReq() {
  $.ajax({
    url: "/stop",
    success: function(data) {
      if (!machine.progress) {
        machine.interpretState(data);
        return buttonReq();
      }
    }
  });
}; buttonReq();



