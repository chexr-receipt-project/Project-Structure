from function_matching.main import matching_queue_handler
import asyncio


async def test_matching_queue_handler():
    event = {
        'Records': [
            {'body': "transaction_id:6058bc6dff0f57c7346938c9"},
            {'body': "bank_transaction_id:605888047140a20481b7ddd3"}
        ]
    }
    await matching_queue_handler(event, "")


if __name__ == '__main__':
    asyncio.run(test_matching_queue_handler())
