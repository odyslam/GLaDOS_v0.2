
var pc_status,l_light_status,r_light_status,o_light_status,heater_status,inside,el_time;

webiopi().ready(function() {
    console.log("ksekinisa");
    webiopi().refreshGPIO(true);
    get_status();
    countdown_clock(el_time)
    set_status();});
function get_status(){
     webiopi.callMacro("status",[],store_status);}
function store_status(macro,args,data) {
     o_light_status = data[0];
     l_light_status = data[2];
     r_light_status = data[3];
     inside = data[4];
     heater_status = data[5];
     el_time = data[6];}
function set_status(){
    document.getElementById("myonoffswitch").checked = pc_status;
    document.getElementById("myonoffswitch1").checked = l_light_status;
    document.getElementById("myonoffswitch2").checked = r_light_status_status;
    document.getElementById("myonoffswitch3").checked = o_light_status;
    document.getElementById("myonoffswitch4").checked = heater_status;
    document.getElementById("myonoffswitch5").checked = heater_status;}
 function house(enter){
     webiopi.callMacro("house",[enter]);}

function time_day(gday){
    if(gday == 1){
        webiopi.callMacro("gday");
    }
    else {
        webiopi.callMacro("gnight");
    }
}

function pc() {
     if (pc_status == 1) {
         webiopi.callMacro("desktop_pc", "off");
     }
     else {
         webiopi.callMacro("desktop_pc", "on");
     }
 }
function light(number,l_group_status){
    statuslist = [l_light_status,r_light_status,o_light_status];
    mode = 1 - statuslist[l_group_status]; /*if status = 1 (on) mode = 0 , turn off the light and vice versa */
    webiopi.callMacro("lights",[number,mode]);}
function heater(time){
         time = time * 60; /* convert min to sec */
         var mode = 1 - heater_status; /* will switch between 1 and 0, if status = 0 (off) mode = 1 so it turns it on */
         webiopi.callMacro("heater",[mode,time]);
         countdown_clock(time);}

function heater_ctime(){
    var heat_time = document.getElementbyId("time");
    heater(heater_time.value);
}


function countdown_clock(seconds){
    var clock;
    clock = new FlipClock($('.clock'), seconds, {
        clockFace: 'MinuteCounter',
        autoStart: true,
        countdown: true
    });
}