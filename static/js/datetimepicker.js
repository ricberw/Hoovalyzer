$('#starttimebutton').click( function() {
  $("#starttime").AnyTime_picker(
      { format: "%Y-%m-%dT%H:%i:%sZ%#MINUTES",
        formatUtcOffset: "%: (%@)" } ).focus();
  $('#starttimebutton').hide();
  $('#starttime').css('background-image','url("/static/images/calendar.png")');
  $('#starttime').css('background-position','right center');
  $('#starttime').css('background-repeat','no-repeat');
  $('#starttime').css('width','230px');
});

$('#endtimebutton').click( function() {
  $("#endtime").AnyTime_picker(
      { format: "%Y-%m-%dT%H:%i:%sZ%#MINUTES",
        formatUtcOffset: "%: (%@)" } ).focus();
  $('#endtimebutton').hide();
  $('#endtime').css('background-image','url("/static/images/calendar.png")');
  $('#endtime').css('background-position','right center');
  $('#endtime').css('background-repeat','no-repeat');
  $('#endtime').css('width','230px');
});
