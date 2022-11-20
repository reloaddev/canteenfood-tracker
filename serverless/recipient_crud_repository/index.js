const AWS = require("aws-sdk");
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    let body;
    let statusCode = 200;
    const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "https://canteenfoodtrackerbucketno1.s3.eu-central-1.amazonaws.com"
    };


    try {
        let requestJSON
        switch (event.routeKey) {
            case "GET /recipients/{email}":
                let requestBody = event.body
                body = await dynamo.get({
                    TableName: "Recipient",
                    Key: {
                        Email: event.pathParameters.email
                    }
                }).promise();
                break;
            case "GET /recipients":
                body = await dynamo.scan({ TableName: "Recipient" }).promise();
                break;
            default:
                throw new Error(`Unsupported route: "${event.routeKey}"`);
        }
    }
    catch (err) {
        statusCode = 400;
        body = err.message;
    }
    finally {
        body = JSON.stringify(body);
    }
    return {
        statusCode,
        body,
        headers
    };
};

