var Client = require('node-rest-client').Client;
var client = new Client();

// Provide API token in HTTP Authorization header:
var args = {
   headers: { "Authorization": "Bearer <your-token>" }
};

// Call /v1/jobs
client.get("http://api.kiso.io/v1/jobs", args, function (data, response) {
   if (response.statusCode != 200) {
       console.log(response.statusCode + " " + response.statusMessage);
       return;
   }
   // `data` contains response parsed as JavaScript
   console.log("Job list:");
   for (var i = data.length - 1; i >= 0; i--) {
       console.log(data[i].name + " (" + data[i].uuid + ")");
   }
});
