var pc_status,l_light_status,r_light_status,o_light_status,heater_status,inside,el_time;

webiopi().ready(function() {
    console.log("ksekinisa");
    w().refreshGPIO(true);
    $(".door_icons").click(function(){
    $(this).toggleClass("down");})
    get_status();
});

function get_status(){
     webiopi().callMacro("status",[],store_status);}

function get_status_test(){
    webiopi().callMacro("status_test",[],store_status_test);}

function store_status(macro,args,data){
    console.log(data);
    status_dict = JSON.parse(data);
    console.log(status_dict)
    o_light_status = status_dict['o_light'];
    r_light_status = status_dict['r_light'];
    l_light_status = status_dict['l_light'];
    inside = status_dict['inside'];
    heater_status = status_dict['he_status'];
    el_time = status_dict['el_time']
    pc_status = ['pc_status']
    
    set_status();
    countdown_clock(el_time);
    console.log("el_time"+ el_time);

}

function set_status(){
    document.getElementById("myonoffswitch").checked = pc_status;
    document.getElementById("myonoffswitch1").checked = l_light_status;
    document.getElementById("myonoffswitch2").checked = r_light_status;
    document.getElementById("myonoffswitch3").checked = o_light_status;
    document.getElementById("myonoffswitch4").checked = heater_status;
    document.getElementById("myonoffswitch5").checked = heater_status;}
 function house(enter){
    var i = confirm ("Oppening Doors, please confirm")
    if (i==true){
        webiopi().callMacro("house",[enter]);
    }
    else{
        location.reload();
    }
     
 }

function doors(door){
    var i = confirm ("Oppening Doors, please confirm")
    if (i==true){
        webiopi().callMacro("open_door",[door]);
    }
    else{
        location.reload();
    }

}
function time_day(gday){
    var i = confirm ("Morning Routine,please confirm")
    if(i==true){
        if(gday == 1){
            webiopi().callMacro("gday");
        }
        else {
            webiopi().callMacro("gnight");
        }
    }
}

function pc() {
     if (pc_status == 1) {
         webiopi().callMacro("desktop_pc", [0]);
     }
     else {
         webiopi().callMacro("desktop_pc", [1]);
     }
 }
function light(l_group_status,number){
    statuslist = [l_light_status,r_light_status,o_light_status];
    mode = 1 - statuslist[l_group_status]; /*if status = 1 (on) mode = 0 , turn off the light and vice versa */
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

    webiopi().callMacro("lights",[number,mode]);}

function heater(time){
    time = time * 60; /* convert min to sec */
    var mode = 1 - heater_status;
    console.log("mode "+ mode) ;/* will switch between 1 and 0, if status = 0 (off) mode = 1 so it turns it on */
    webiopi().callMacro("heater",[mode,time]);
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
    var intervalID = window.setInterval(pin_return, 500);
    
}
function pin_return(){
    console.log(webiopi().digitalRead(22))
}
