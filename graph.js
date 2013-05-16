$(function() {
	
	
	var a=document.URL;
	var n=a.split("/");
	var c=n[2];
	var d=c.split(":")[0];
	 
        var ws = new WebSocket("ws://"+d+":9999/test");
	var datalen=10;
	var datasets={};
	var field_array=["Building","Floor","Wing","Meter","Time","VA","W","VAR","PF","VLL","VLN","A","F","VA1","W1","VAR1","PF1","V12","V1","A1","VA2","W2","VAR2","PF2","V23","V2","A2","VA3","W3","VAR3","PF3","V31","V3","A3","FwdVAh","FwdWh","FwdVARh","FwdVARh"]
	var required_field_array_numbers=[6,10,35];
	for (i=0;i<required_field_array_numbers.length;i++)
	{
		var j=required_field_array_numbers[i];
		datasets[field_array[i]]={};
		datasets[field_array[i]]["label"]=field_array[j];
		datasets[field_array[i]]["data"]=[];
		datasets[field_array[i]]["dataindex"]=j;
	
	}
	  // hard-code color indices to prevent them from shifting as
    var i = 0;
    $.each(datasets, function(key, val) {
        val.color = i;
        ++i;
    });
    
    // insert checkboxes 
    var choiceContainer = $("#choices");
							    //meterContainer = $("#meters");
    var numberOfMeters = 4    
    var kt = 1
    while(kt <= numberOfMeters)
    {
    	$("#meters").append("<option value = '"+kt+"'>"+"Meter: "+kt+"</option>")
        kt = kt + 1;
    }    

    $.each(datasets, function(key, val) {
        choiceContainer.append('<br/><input type="checkbox" name="' + key +
                               '" checked="checked" id="id' + key + '">' +
                               '<label for="id' + key + '">'
                                + val.label + '</label>');
    });
    choiceContainer.find("input").click(cleanOlderData);
    
    function cleanOlderData()
    {

		
    }
    
    var $placeholder = $('#placeholder');
    
    ws.onmessage = function(evt) {
		console.log(evt.data);
		var data_list=evt.data.split(",")
		
		if(data_list[3] == $("#meters option:selected").attr("value"))
		{
		
		var x=(parseFloat(data_list[4])+19800000)*1000;
		//x = parseInt(data_list[4])+19800000;
		console.log(x)
		var data = [];
		choiceContainer.find("input:checked").each(function () {
            	var key = $(this).attr("name");
            
    									//console.log(JSON.stringify(datasets[key]));
		datasets[key].data.push([x,parseFloat(data_list[datasets[key]["dataindex"]])]);
		while (datasets[key].data.length > datalen) {
			datasets[key].data.shift();
		}
		data.push(datasets[key]);
									//console.log(datasets[key]);
				if (data.length > 0){

	           			 $.plot($("#placeholder"), data, {
        	        		 	
               				 	xaxis:{
                    					mode: "time",
             					        timeformat: "%H:%M:%S",
                         				minTickSize: [1, "second"],
                			      	       },
						yaxis: { }
            			 });
                							//data.push(datasets[key]);	
				  	  

	 		 }		
       		});
	}
		
    }
    ws.onopen = function(evt) {
        $('#conn_status').html('<b>Connected</b>');
    }
    ws.onerror = function(evt) {
        $('#conn_status').html('<b>Error</b>');
    }
    ws.onclose = function(evt) {
        $('#conn_status').html('<b>Closed</b>');
    }
});
