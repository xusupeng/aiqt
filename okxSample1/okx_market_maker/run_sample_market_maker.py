import websocket
import json
import sys
sys.path.append('/aiqt/aiqtEnv/lib/python3.12/site-packages/okx/')
# sys.path.append('/aiqt/aiqtEnv/lib/site-packages/okx_api')
# sys.path.append('/aiqt/aiqtEnv/lib/site-packages/okx_candle')
# sys.path.append('/aiqt/aiqtEnv/lib/site-packages/okx_trade')
# sys.path.append('/aiqt/okxSample1/')

import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../okx_api')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../okx_candle')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../okx_trade')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))



from okx_market_maker.strategy.SampleMM import SampleMM


if __name__ == "__main__":
    strategy = SampleMM()
    strategy.run()

