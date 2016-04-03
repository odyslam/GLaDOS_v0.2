
 webiopi().ready(function() {
                        /* MAKE FUNCION THAT READS HEATER STATUS,change HTML*/
                        console.log("ksekinisa");
                        webiopi().refreshGPIO(true);
                        HeaterStatus();

        });             
                        
                        function OpenDoors(){
                            webiopi().callMacro("OpenDoors","knock");
                            console.log("Open-Doors");

                        }

                        function LeaveHouse(){
                           webiopi().callMacro("LeavEHouse");
                           console.log("LeaveHouse");
                       }

                        function HouseEntry(){
                            webiopi().callMacro("HouseEnter");
            
                            console.log("house"); 
                        }
                        function PcOn(){
                            webiopi().callMacro("PCON","0");
                            console.log("mpika");
                        }


                        
                        
                        function Heater() {
                            webiopi().callMacro("OffHeater",HeaterStatus());
                            console.log("PAnic");
                            location.reload();
                        } 

                        var DisplayStatus = function(macro,args,response){
                            var heater = JSON.parse(response);
                            console.log(heater[0])

                          if (heater[0] == 1){

                            /* $("#div1").load("demo_test.txt");   dokimase auto anti gia innter.html mipos to kanei dinamika */
                            
                                 document.getElementById("heaterstatus").innerHTML = "Burning-House..";
                                 $("#heaterstatus").css("font-color","#FF0000");
                          }
                          else {
                                document.getElementById("heaterstatus").innerHTML = "You are safe" ;
                                $("#heaterstatus").css("font-color","#00ff00");
                          }
                        }

                        function HeaterStatus() {
                            console.log("heaterstatus");
                            webiopi().callMacro("HeaterStatus",[],DisplayStatus);

}

                        function getdata(){
                            console.log("get-data");
                            var time =  $("#inputOff").val();
                            webiopi().callMacro("OnHeater",time,HeaterStatus());
                            location.reload();
                        }
                        