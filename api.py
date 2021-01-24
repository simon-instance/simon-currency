import json
import base64
import ecdsa

from flask import Flask, request, Response

from api_conf import LIVE_CHAIN_OUT, PENDING_NODE_TRANSACTIONS, MINER_ADDRESS


node = Flask(__name__)


@node.route('/all-blocks', methods=['GET'])
def all_blocks():
    pass

@node.route('/transactions', methods=['GET', 'POST'])
def transactions():
    transaction_body = request.json()
    if request.method == 'POST':
        if validate_signature(transaction_body['sender'], transaction_body['signature'], transaction_body['message']):
            PENDING_NODE_TRANSACTIONS.append(transaction_body)

            print('Transaction added to queue')
            return Response('Transaction succeeded', status=200, mimetype='text/plain')
        else:
            return Response('Transaction failed', status=500, mimetype='text/plain')

    if request.method == 'GET' and request.args.get('update_miner') == MINER_ADDRESS:
        response_data = json.dumps(LIVE_CHAIN_OUT)
        return Response(response_data, status=200, mimetype='application/json')

    return Response('Whoops, that request doesn\'t exist', status=501, mimetype='text/plain')

def validate_signature(public_key, signature, message):
    public_key = (base64.b64decode(public_key)).hex().decode('hex')
    signature = base64.b64decode(signature)

    key = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.SECP256k1)

    try:
        return key.verify(signature, message.encode())
    except:
        return False