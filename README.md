# jpm-liquidity

Provide liquidity for CEX as a market maker.

## common

common module includes strategies, CEX APIs, and utilities.

## quote

quote module collects order book from other CEX usually by a websocket.

## maker

maker module is responsibility for updating list orders.

## hedger

hedger module is optional, if you don't want hold risk positions, hedger can hedge these positions by another CEX.

## selftrade

selftrade module is optional, it is used if you want to tune your k-charts.