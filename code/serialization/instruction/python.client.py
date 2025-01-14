from borsh_construct import *
from enum import IntEnum
from solana.rpc.types import RPCResponse
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.rpc.api import Client


# Instruction variants for target program
class InstructionVariant(IntEnum):
    INITIALIZE = 0,
    MINT = 1,
    TRANSFER = 2,
    BURN = 3


# Schema for sending instructionVariants to on-chain sample program
payloadSchema = CStruct(
    "initialized" / U8,
    "key" / String,
    "value" / String
)


def construct_payload(instructionVariant: InstructionVariant, key: str, value: str):
    """Generate a serialized instructionVariant"""
    return payloadSchema.build({'instructionVariant_id': instructionVariant, 'key': key, 'value': value})


def mintKv(
        client: Client,
        program_pk: PublicKey,
        account_pk: PublicKey,
        wallet_kp: Keypair,
        mintKey: str,
        mintValue: str) -> RPCResponse:
    """Mint with a key/vaue pair to an account"""
    # Construct the program payload for Mint invariant
    payload_ser = construct_payload(
        InstructionVariant.MINT, mintKey, mintValue)

    # print(payload_ser)
    # => b'\x01\n\x00\x00\x00python key\x0c\x00\x00\x00python value'
    # mint_payload_copy = payloadSchema.parse(payload_ser)
    # print(mint_payload_copy)
    # => Container:
    # =>     initialized = 1
    # =>     key = u'python key' (total 10)
    # =>     value = u'python value' (total 12)

    # Construct the transaction with instructionVariant
    txn = Transaction().add(TransactionInstruction(
        [AccountMeta(account_pk, False, True)],
        program_pk,
        payload_ser))
    return client.send_transaction(txn, wallet_kp)
    # => {'jsonrpc': '2.0', 'result': '4ZdpWNdovdVaLextWSiqEBWp67k9rNTTUaX3qviHDXWY9c98bVtaRt5sasPhYzMVXHqhex78gzNKytcBnVH5CSTZ', 'id': 2}
