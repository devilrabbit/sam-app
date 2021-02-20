// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
const { v4: uuidv4 } = require('uuid');
const base64url = require('base64url');

let response;

function encode_lib(uuid)
{
    let hex = uuid.split('-').join("");
    let binary = Buffer.from(hex, 'hex');
    return base64url(binary);
}

function decode_lib(shortid)
{
    let binary = base64url.toBuffer(shortid);
    let hex = binary.toString('hex');
    let phases = [
        hex.substring(0, 8),
        hex.substring(8, 12),
        hex.substring(12, 16),
        hex.substring(16, 20),
        hex.substring(20, 32)
    ]
    return phases.join('-');
}

function encode(uuid)
{
    const hex = uuid.split('-').join("");
    const base64 = Buffer.from(hex, 'hex').toString('base64');
    return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

function decode(shortid)
{
    const base64 = shortid.replace(/-/g, '+').replace(/_/g, '/') + '==';
    const binary = Buffer.from(base64, 'base64');
    const hex = binary.toString('hex');
    const phases = [
        hex.substring(0, 8),
        hex.substring(8, 12),
        hex.substring(12, 16),
        hex.substring(16, 20),
        hex.substring(20, 32)
    ]
    return phases.join('-');
}

/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html 
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 * 
 */
exports.lambdaHandler = async (event, context) => {
    try {
        let uuid = uuidv4();
        let shortid = encode(uuid);
        let decoded = decode(shortid);

        // const ret = await axios(url);
        response = {
            'statusCode': 200,
            'body': JSON.stringify({
                message: 'hello world',
                uuid: uuid,
                short_id: shortid,
                decoded: decoded
                // location: ret.data.trim()
            })
        }
    } catch (err) {
        console.log(err);
        return err;
    }

    return response
};
