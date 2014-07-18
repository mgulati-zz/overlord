
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

