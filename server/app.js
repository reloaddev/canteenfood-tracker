const express = require("express");
const app = express();
const port = 3000;

app.get("/meals/henrik", (req, res) => {
  res.send(["Test 1", "Test 2", "Test 3"]);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
