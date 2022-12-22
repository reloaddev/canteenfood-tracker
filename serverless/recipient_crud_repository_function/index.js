const AWS = require("aws-sdk");
const dynamo = new AWS.DynamoDB.DocumentClient();
// const allowedOrigins = [
//   "http://localhost:5173",
//   "https://canteenfoodtrackerbucketno1.s3.eu-central-1.amazonaws.com",
// ];

exports.handler = async (event) => {
  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  if (event.routeKey != undefined && event.routeKey.startsWith("OPTIONS ")) {
    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin":
          "https://canteenfoodtrackerbucketno1.s3.eu-central-1.amazonaws.com",
        "Access-Control-Allow-Headers": "Authorization",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      },
    };
  }

  try {
    switch (event.routeKey) {
      case "GET /recipients/{email}":
        body = await dynamo
          .get({
            TableName: "Recipient",
            Key: {
              Email: event.pathParameters.email,
            },
          })
          .promise();
        if (!body || !body.Item || !body.Item.Meals) {
          body = [];
        } else {
          body = body.Item.Meals;
        }
        break;
      case "GET /recipients":
        body = await dynamo.scan({ TableName: "Recipient" }).promise();
        break;
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }
  return {
    statusCode,
    headers,
    body,
  };
};
