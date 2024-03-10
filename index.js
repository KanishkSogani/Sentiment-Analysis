const express = require("express");
const db = require('./db');
const bodyparser = require("body-parser");
const path = require("path");
const fsPromises = require('fs/promises');
const axios = require("axios");
const multer = require("multer");
// const request = require("request-promise");
const cors = require("cors");
const app = express();
// const ejs = require("ejs");
// import {} from "@kurkle/color";
const port = process.env.PORT || 3000;

app.use(cors());

// app.set("view engine","ejs");
const upload = multer({ dest: "uploads/" });
app.use("/public", express.static(path.join(__dirname, "public")));
app.use(bodyparser.urlencoded({ extended: true }));


var answer = "";
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname + "/HTML/index.html"));
});

const apiURL = "http://127.0.0.1:5000";

app.post('/predict', async (req,res)=>{
  try {
    // console.log("req.body : ", req.body);
    const data0 = { inputData: req.body.search2 };
    // console.log("apiURL : ", apiURL);
    console.log("Data : ", data0);
    const result0 = await axios.post(apiURL + "/predict", data0);
    // console.log("result : ", result);
    bert0 = result0.data.bert;
    barGraph0 = result0.data.word_bargraph;
    countGraph0 = result0.data.count_bargraph;
    percentage0 = result0.data.percentage;
    res.sendFile(path.join(__dirname + "/HTML/Result_predict.html"));
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.get('/predict', (req,res)=>{
  res.send({bert0, barGraph0, countGraph0, percentage0});
})

app.post("/twitter", async (req, res) => {
  try {
    // console.log("req.body : ", req.body);
    const data = { inputData: req.body.search2 };
    // console.log("apiURL : ", apiURL);
    // console.log("Data : ", data);
    const result = await axios.post(apiURL + "/predict_twitter", data);
    // console.log("result : ", result);
    bert = result.data.bert;
    barGraph = result.data.word_bargraph;
    countGraph = result.data.count_bargraph;
    percentage = result.data.percentage;
    res.sendFile(path.join(__dirname + "/HTML/result.html"));
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.get('/graphs', (req,res)=>{
  console.log(barGraph, countGraph, percentage)
  res.send({barGraph, countGraph, percentage});
})

app.get('/result', (req, res) => {
  res.send({ bert });
});

app.get('/comments_twitter', async (req,res)=>{
  try {
    const result2 = await axios.get('http://127.0.0.1:5000/comments_twitter');
    bert2 = result2.data.bert;
    barGraph2 = result2.data.words;
    countGraph2 = result2.data.counts;
    percentage2 = result2.data.percentage;
    res.sendFile(path.join(__dirname + "/HTML/comments.html"));
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
})

app.get('/parts', (req, res)=>{
  res.send({bert2, percentage2, barGraph2, countGraph2});
})

app.post('/youtube', async (req, res)=>{
  try {
    // console.log("req.body : ", req.body);
    const data3 = { inputData: req.body.search2 };
    // console.log("apiURL : ", apiURL);
    // console.log("Data : ", data);
    const result3 = await axios.post(apiURL + "/youtube", data3);
    // console.log("result : ", result);
    bert3 = result3.data.bert; 
    barGraph3 = result3.data.word_bargraph;
    countGraph3 = result3.data.count_bargraph;
    percentage3 = result3.data.percentage;
    res.sendFile(path.join(__dirname + "/HTML/result_youtube.html"));
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.get('/youtube', (req, res)=>{
  res.send({bert3, countGraph3, barGraph3, percentage3});
})

app.post('/upload-excel', upload.single("excelfile"), async (req, res) => {
  try {
    const uploadedFile = req.file;
    if (!uploadedFile) {
      return res.status(400).send('No file uploaded.');
    }

    const originalFilename = uploadedFile.originalname;
    const destinationPath = uploadedFile.path;
    const newFilename = "stock.csv";
    const newFilePath = path.join(__dirname, newFilename);

    await fsPromises.rename(destinationPath, newFilePath); // Use async version

    console.log("File uploaded Successfully!");

    const result2 = await axios.get('http://127.0.0.1:5000/excel');
    bert_excel = result2.data.bert;
    barGraph_excel = result2.data.word_bargraph;
    countGraph_excel = result2.data.count_bargraph;
    percentage_excel = result2.data.percentage;
    res.sendFile(path.join(__dirname + "/HTML/excel.html"));
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.get('/excel', (req, res)=>{
  res.send({bert_excel, countGraph_excel, barGraph_excel, percentage_excel});
})3

app.post('/reddit', async(req,res)=>{
  try {
    console.log("req.body : ", req.body);
    const data5 = { inputData: req.body.search2 };
    // console.log("apiURL : ", apiURL);
    console.log("Data : ", data5);
    const result5 = await axios.post(apiURL + "/reddit", data5);
    // console.log("result : ", result);
    bert5 = result5.data.bert; 
    barGraph5 = result5.data.word_bargraph;
    countGraph5 = result5.data.count_bargraph;
    percentage5 = result5.data.percentage;
    res.sendFile(path.join(__dirname + "/HTML/result_reddit.html"));
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
})

app.get('/reddit', (req, res)=>{
  res.send({bert5, countGraph5, barGraph5, percentage5})
});

//let text1= " select * from twitterdata where index>1;";
// con.connect(mysql,function(error){
//     if(error) throw error;
//    console.log("connect");
// //con.query("SELECT * FROM twitterdata " , function(error,result)
// con.query("SELECT Text, Sentiment,Date_time FROM sentiment_analysis ORDER BY  Index_value DESC  LIMIT 10" , function(error,result)
// {
//  if(error) throw error;
// console.log(result);

// });
// });;

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});