var mysql= require("mysql")

var con =mysql.createConnection({
host:"127.0.0.1",
port: "3306",
user:"root",
password:"ravi",
//database:"kprojectdb"
database:"sih_finale"
});

//let text1= " select * from twitterdata where index>1;";
module.exports = con;