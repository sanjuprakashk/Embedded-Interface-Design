// Node.js WebSocket server script
const http = require('http');
const WebSocketServer = require('websocket').server;
const server = http.createServer();
server.listen(9898);
const wsServer = new WebSocketServer({
    httpServer: server
});
var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "sansri",
  password: "sansri1234",
  database: "eid_project1"
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    connection.on('message', function(message) {
    if(message.utf8Data == "GetImmediateHumVal") {
      console.log('Received Message:', message.utf8Data);
      var ret = [];
      con.query("SELECT Humd FROM HUMID ORDER BY id DESC LIMIT 1", function (err, result, fields) {
      if (err) throw err;
        ret = JSON.stringify(result);
        console.log(ret);
        connection.sendUTF(ret);
    
      });
    }
    var ret_hum;
    var ret_temp;
    var readings;
    const hum_temp_join ={};
    
    if(message.utf8Data == "getReadings") {
      //console.log('Received Message:', message.utf8Data);
      
      con.query("SELECT Humd FROM HUMID ORDER BY id DESC LIMIT 1", function (err, result_hum, fields) {
      if (err) throw err;
        ret_hum = result_hum[0].Humd
        console.log('ret_hum:', result_hum[0].Humd);

      });
      
      con.query("SELECT Temp FROM TEMP ORDER BY id DESC LIMIT 1", function (err, result_temp, fields) {
      if (err) throw err;
        ret_temp = result_temp[0].Temp
        console.log('ret_temp:', result_temp[0].Temp);
        
        readings = {temp:ret_temp, hum:ret_hum};
        console.log('ret:', readings);
        
        connection.sendUTF(JSON.stringify(readings));

      });
       
       
    }
    
    if(message.utf8Data == "GetLast10HumVal") {
      //console.log('Received Message:', message.utf8Data);
      var ret = [];
      con.query("SELECT Humd FROM HUMID ORDER BY id DESC LIMIT 3", function (err, result, fields) {
      if (err) throw err;
        ret = JSON.stringify(result);
        //console.log(ret);
        connection.sendUTF(ret);
      });
    }
    
    else {
      console.log('Received Message: NULL');
    }
      connection.sendUTF('Hi this is WebSocket server!');
    });
    connection.on('close', function(reasonCode, description) {
        console.log('Client has disconnected.');
    });
});
