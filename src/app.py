from web3 import Web3

class PolygonRPC():    
    def test_block_number(self):
        url = 'https://rpc.ankr.com/polygon_zkevm/ec2159070bc430950775b36f11d6a78ae27b75bb79d45965c37b950a587ee000'  # url string
        
        web3 = Web3(Web3.HTTPProvider(url))

        print(web3.eth.block_number)

test_instance = PolygonRPC()
test_instance.test_block_number()