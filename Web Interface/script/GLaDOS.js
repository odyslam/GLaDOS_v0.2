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

function store_status(macro,args,data) {
    console.log("data:"+ data)
     o_light_status = parseInt(data[1]);
     pc_status = parseInt(data[9]);
     l_light_status = parseInt(data[5]);
     r_light_status = parseInt(data[7]);
     inside = parseInt(data[11]);
     heater_status = parseInt(data[13]);
     time_str = data.substring(15, 20);
     el_time = parseInt(time_str);
     set_status();
     console.log("el_time"+ el_time)
     countdown_clock(el_time)
 }
function set_status(peos){

    document.getElementById("myonoffswitch").checked = pc_status;
    document.getElementById("myonoffswitch1").checked = l_light_status;
    document.getElementById("myonoffswitch2").checked = r_light_status;
    document.getElementById("myonoffswitch3").checked = o_light_status;
    document.getElementById("myonoffswitch4").checked = heater_status;
    document.getElementById("myonoffswitch5").checked = heater_status;}
 function house(enter){
     webiopi().callMacro("house",[enter]);
 }

function doors(door){
    webiopi().callMacro("open_door",[door]);

}
function time_day(gday){
    if(gday == 1){
        webiopi().callMacro("gday");
    }
    else {
        webiopi().callMacro("gnight");
    }
}

function pc() {
     if (pc_status == 1) {
         webiopi().callMacro("desktop_pc", "off");
     }
     else {
         webiopi().callMacro("desktop_pc", "on");
     }
 }
function light(l_group_status,number){
    statuslist = [l_light_status,r_light_status,o_light_status];
    mode = 1 - statuslist[l_group_status]; /*if status = 1 (on) mode = 0 , turn off the light and vice versa */
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