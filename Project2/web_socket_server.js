// Node.js WebSocket server script
const http = require('http');
const WebSocketServer = require('websocket').server;
const server = http.createServer(); // WebSocket to process HTTP request
server.listen(9898);  // Sever listens on port 9898

// Creating the server
const wsServer = new WebSocketServer({
    httpServer: server
});
var mysql = require('mysql');

// Creating connection to DB
var con = mysql.createConnection({
  host: "localhost",
  user: "sansri",
  password: "sansri1234",
  database: "eid_project1"
});

// CHecking the connection with DB
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

// WebSocket Server to handle requests from client
wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    connection.on('message', function(message) {
    
    var ret_hum;
    var ret_temp;
    var readings;
    const hum_temp_join ={};
    
    // Getting the Immediate reading from the DB
    if(message.utf8Data == "getReadings") {
  
      con.query("SELECT Humd FROM HUMID ORDER BY id DESC LIMIT 1", function (err, result_hum, fields) {
      if (err) throw err;
        ret_hum = result_hum[0].Humd

      });
      
      con.query("SELECT Temp FROM TEMP ORDER BY id DESC LIMIT 1", function (err, result_temp, fields) {
      if (err) throw err;
        ret_temp = result_temp[0].Temp
        
        const readings = { "temp" : ret_temp, "hum" : ret_hum };
        console.log('ret:', readings);
        
        connection.sendUTF(JSON.stringify(readings));

      });
       
       
    }
    
    // Getting the latest 10 values from DB
    if(message.utf8Data == "GetLast10HumVal") {
      var ret = [];
      var hum_readings = [];
      var hum_readings_arr = [];
      con.query("SELECT Humd FROM HUMID ORDER BY id DESC LIMIT 10", function (err, result, fields) {
      if (err) throw err;
        var ret_10hum = [];
        var ReverseArray = [];
        var length = result.length;
        for(var i = length-1;i>=0;i--){
            ReverseArray.push(result[i]);
        }
        console.log("Last 10 Values of Humidity is");
        console.log(JSON.stringify(ReverseArray));
        connection.sendUTF(JSON.stringify(ReverseArray));
      });
    }
    
    
    else {
      console.log('Received Message: NULL');
    }
      connection.sendUTF('Hi this is WebSocket server!');
    });
    // Closing the user connection
    connection.on('close', function(reasonCode, description) {
        console.log('Client has disconnected.');
    });
});
