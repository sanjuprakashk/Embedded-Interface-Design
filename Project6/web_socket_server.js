// Node.js WebSocket server script
const http = require('http');
const WebSocketServer = require('websocket').server;
const server = http.createServer();
server.listen(9898);
const wsServer = new WebSocketServer({
    httpServer: server
});
var mysql = require('mysql');

/* Creating connectiong with the db*/
var con = mysql.createConnection({
  host: "localhost",
  user: "srisan",
  password: "srisan1234",
  database: "super_project"
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

/* Accessing db on request from client*/

wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    connection.on('message', function(message) {
    if(message.utf8Data == "getData") {
      console.log('Received Message:', message.utf8Data);
      var ret = [];
      con.query("SELECT * FROM MAGICWAND1", function (err, result, fields) {
      if (err) throw err;
        ret = JSON.stringify(result);
        console.log(ret);
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
