var pc_status, l_light_status, r_light_status, o_light_status, heater_status, inside, el_time;

//Change status vars to status_obj, it is passed via reference. When a value changes in a function
//it will automatically change in the object, maybe cleaner
$( document ).ready(function() {
    console.log( "ready!" );
    get_status();
});
function get_status(){
     call_macro("status",[],store_status);
}
function store_status(macro,args,data){
    status_dict = JSON.parse(data);
    console.log(status_dict)
    o_light_status = status_dict['o_light'];
    r_light_status = status_dict['r_light'];
    l_light_status = status_dict['l_light'];
    inside = status_dict['inside'];
    heater_status = status_dict['he_status'];
    el_time = status_dict['el_time'];
    pc_status = status_dict['pc_status'];
    set_status();
    countdown_clock(el_time);
}
function set_status(){
    document.getElementById("myonoffswitch").checked = pc_status;
    document.getElementById("myonoffswitch1").checked = l_light_status;
    document.getElementById("myonoffswitch2").checked = r_light_status;
    document.getElementById("myonoffswitch3").checked = o_light_status;
    document.getElementById("myonoffswitch4").checked = heater_status;
    document.getElementById("myonoffswitch5").checked = heater_status;}
 function house(enter){
    var i = confirm ("Enter/Leave House Routine, please confirm")
    if (i == true){
        call_macro("house",[enter],get_status);
    }    
 }
function doors(door){
    var i = confirm ("Oppening Doors Routine, please confirm")
    if (i == true){
        call_macro("open_door",[door]);
        $(".door_icons").toggleClass("down");
    }
}
function time_day(gday){
    var i = confirm ("Morning/Night Routine,please confirm")
    if(i == true){
        if(gday == 1){
            call_macro("gday");
        }
        else {
            call_macro("gnight");
        }
    get_status();
    }
}
function pc() {
     if (pc_status == 1) {
         call_macro("desktop_pc", [0]);
     }
     else {
         call_macro("desktop_pc", [1]);
     }
 }
function light(l_group_status,number){
    var statuslist = [l_light_status,r_light_status,o_light_status];
    var mode = 1 - statuslist[l_group_status]; /*if status = 1 (on) mode = 0 , turn off the light and vice versa */
    switch(l_group_status){
        case 0:
            l_light_status = mode;
            break;
        case 1:
            r_light_status = mode;
            break;
        case 2:
            o_light_status = mode;
            break;
    }
    call_macro("lights",[number,mode]);
}
function heater(time){
    time = time * 60; /* convert min to sec */
    var mode = 1 - heater_status;
    console.log("mode "+ mode) ;/* will switch between 1 and 0, if status = 0 (off) mode = 1 so it turns it on */
    call_macro("heater",[mode,time]);
        if (mode == 1){
            countdown_clock(time);
            console.log("clock started for: " +time)
            heater_status = 1;
        }
        else{
            countdown_clock(0)
            heater_status = 0;
        }
     }
function heater_ctime(){
    var heat_time = document.getElementById("time");
    heater(heat_time.value);
}
function countdown_clock(seconds){
    var clock;
    clock = new FlipClock($('.clock'), seconds, {
        clockFace: 'MinuteCounter',
        autoStart: true,
        countdown: true
    });
}
function test_door(){
    var intervalID = window.setInterval(
    function(){digital_read(22,console.log);}
    , 500);
}
call_macro = function (macro, args, callback) {
	if (args == undefined) {
		args = "";
	}
	$.post('/macros/' + macro + "/" + args, function(data) {
		if (callback != undefined) {
			callback(macro, args, data);
		}
	});
}
digital_read = function (gpio, callback) {
	if (callback != undefined) {
		$.get('/GPIO/' + gpio + "/value", function(data) {
			callback(data);  
		});
	}
	
}